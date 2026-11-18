#!/usr/bin/env python3
"""Busca local em documentos integrais, índices e referências; apenas biblioteca padrão."""
import argparse
import datetime
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STOP={'a','as','o','os','e','de','da','das','do','dos','em','um','uma','para','por','com','que','qual','quais','the','and','of','to'}
SCOPES={'knowledge','memory','context','processes','people','meetings','workflows','docs'}
# Fontes mantidas (decisão, memória de projeto, processo, pessoa, contexto) vencem evidência de sessão.
AUTHORITATIVE=('knowledge/decisions/','knowledge/projects/','knowledge/roadmap/','processes/','people/','context/')
SESSION_EVIDENCE=('knowledge/conversations/','meetings/')
SUPERSEDED={'substituida','substituída','superada','obsoleta'}

class VisibleHTML(HTMLParser):
    def __init__(self):
        super().__init__();self.hidden=None;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style'}:self.hidden=tag
    def handle_endtag(self,tag):
        if tag==self.hidden:self.hidden=None
    def handle_data(self,data):
        if not self.hidden and data.strip():self.parts.append(data.strip())

def metadata(text):
    match=re.match(r'^---\s*\n(.*?)\n---\s*\n',text,re.S)
    if match:
        try:return json.loads(match.group(1))
        except (ValueError,TypeError):pass
    return {}

def superseded(meta):
    return str(meta.get('status','')).casefold() in SUPERSEDED

def expired(meta,today):
    """Nota com "expires" (AAAA-MM-DD) vencido sai da busca padrão; o arquivo continua íntegro."""
    try:return datetime.date.fromisoformat(str(meta['expires']))<today
    except (KeyError,ValueError):return False

def source_priority(relative,doc,meta,project,project_filter,historical):
    """Menor valor vem primeiro, depois da cobertura dos termos."""
    priority=2
    if doc:priority=1 if project==project_filter else 2
    if doc and '/knowledge/projects/' in '/'+relative:priority=3
    if relative.startswith(SESSION_EVIDENCE):priority=1
    if relative.startswith(AUTHORITATIVE):priority=0
    if meta.get('knowledge_base')=='homer':priority=1 if meta.get('status')=='curado' else 2
    if str(meta.get('status','')).casefold() in {'historico','histórico'}:priority=6
    if relative.startswith('knowledge/documents/') or Path(relative).name in {'INDEX.md','MEMORY.md'}:priority=5
    if (doc or {}).get('version_only'):priority=4
    if historical:priority=7
    return priority

def words(text):
    value=''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))
    return re.findall(r'[^\W_]+',value,re.UNICODE)

def chunks(text,maximum=1200):
    lines=text.splitlines()
    start=0
    if lines and lines[0].strip()=='---':
        start=next((i+1 for i in range(1,len(lines)) if lines[i].strip()=='---'),0)
    collected=[]
    size=0
    first=start+1
    for number in range(start,len(lines)):
        line=lines[number]
        if collected and size+len(line)>maximum:
            yield first,'\n'.join(collected)
            collected=[];size=0;first=number+1
        if not collected:first=number+1
        if len(line)>maximum:
            if collected:yield first,'\n'.join(collected)
            collected=[];size=0
            for offset in range(0,len(line),maximum):yield number+1,line[offset:offset+maximum]
        else:
            collected.append(line);size+=len(line)+1
    if collected and any(x.strip() for x in collected):yield first,'\n'.join(collected)

def files(args,catalog):
    for scope in sorted(SCOPES):
        for path in sorted((ROOT/scope).rglob('*.md')):
            if 'instructions' in path.relative_to(ROOT).parts and not args.include_instructions:continue
            yield path,None
    for name in ('START.md','MAPEAMENTO.md','README.md'):
        yield ROOT/name,None
    for doc in catalog['documents']:
        if doc.get('version_only') and not args.include_versions:continue
        # Originals remain complete; this script retrieves textual sources only.
        if Path(doc['path']).suffix.lower() in {'.md','.txt','.diff','.html'}:
            yield ROOT/doc['path'],doc
    if args.include_archive:
        for path in sorted((ROOT/'archive').rglob('*.source.txt')):yield path,{'historical':True}
    if args.include_instructions:
        manifest=json.loads((ROOT/'consolidation-manifest.json').read_text(encoding='utf-8'))
        seen=set()
        for record in manifest['records']:
            if record['instruction_reference'] and record['sha256'] not in seen:
                seen.add(record['sha256'])
                yield ROOT/record['copy'],{'project':record['project'],'historical':True,'instruction_reference':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--project',help='Slug em repos.yaml; mantém referências gerais H.O.M.E.R.')
    parser.add_argument('--domain',choices=('geral','lovable','mercado-livre'))
    parser.add_argument('--limit',type=int,default=5)
    parser.add_argument('--include-versions',action='store_true',help='Também consultar versões exclusivas de outras branches.')
    parser.add_argument('--include-archive',action='store_true')
    parser.add_argument('--include-instructions',action='store_true',help='Consultar instruções originais como referências históricas inativas.')
    parser.add_argument('--include-superseded',action='store_true',help='Também consultar notas com status substituída/superada/obsoleta.')
    parser.add_argument('--include-expired',action='store_true',help='Também consultar notas cujo "expires" já passou.')
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    if not 1<=args.limit<=20:parser.error('--limit deve estar entre 1 e 20')
    repos=json.loads((ROOT/'repos.yaml').read_text(encoding='utf-8'))
    entries={p['slug']:p for p in repos['projects']}
    if args.project and args.project not in entries and args.project!='workspace':parser.error('Projeto desconhecido: '+args.project)
    doc_catalog=json.loads((ROOT/'knowledge/documents/catalog.json').read_text(encoding='utf-8'))
    tokens=list(dict.fromkeys(t for t in words(args.query) if t not in STOP))[:12]
    if not tokens:parser.error('Informe pelo menos um termo útil')
    query=' OR '.join('"'+t+'"*' for t in tokens)
    conn=sqlite3.connect(':memory:')
    try:conn.execute("CREATE VIRTUAL TABLE search USING fts5(body,tokenize='unicode61 remove_diacritics 2')")
    except sqlite3.OperationalError:parser.exit(2,'SQLite FTS5 indisponível; use rg ou uma instalação Python com FTS5.\n')
    records={};seen_paths=set();seen_contents=set();skipped=[];hidden={'superseded':0,'expired':0}
    today=datetime.date.today()
    allowed={'geral',args.domain} if args.domain else None
    for path,doc in files(args,doc_catalog):
        if path in seen_paths:continue
        seen_paths.add(path)
        if not path.is_file():continue
        relative=path.relative_to(ROOT).as_posix()
        raw=path.read_bytes()
        text=raw.decode('utf-8-sig',errors='replace')
        html_source=path.suffix.casefold()=='.html'
        if html_source:
            parser=VisibleHTML();parser.feed(text);text='\n'.join(parser.parts)
        meta=metadata(text)
        project=(doc or {}).get('project') or meta.get('project')
        if not project:
            match=re.match(r'knowledge/(?:projects|documents)/([^/]+)\.md$',relative)
            if match and match.group(1) in entries:project=match.group(1)
        if args.project and project and project not in {args.project,'homer'}:continue
        domain=meta.get('domain') or (doc or {}).get('domain')
        if allowed and domain not in allowed and not (args.project and project==args.project):continue
        if superseded(meta) and not args.include_superseded:hidden['superseded']+=1;continue
        if expired(meta,today) and not args.include_expired:hidden['expired']+=1;continue
        # Windows/Git newline differences should not spend two retrieval slots.
        fingerprint=hashlib.sha256(text.replace('\r\n','\n').replace('\r','\n').encode('utf-8')).digest()
        if fingerprint in seen_contents:continue
        seen_contents.add(fingerprint)
        historical=relative.startswith('archive/') or (doc or {}).get('historical',False)
        priority=source_priority(relative,doc,meta,project,args.project,historical)
        review=meta.get('revisar')
        summary=meta.get('summary')
        for line,body in chunks(text):
            if not body.strip():continue
            cursor=conn.execute('INSERT INTO search(body) VALUES (?)',(body,))
            body_words=words(body)
            coverage=sum(any(word.startswith(token) for word in body_words) for token in tokens)
            records[cursor.lastrowid]={'path':relative,'line':None if html_source else line,'line_semantics':'texto extraído de HTML; abrir o arquivo original' if html_source else 'linha do arquivo textual','project':project,'domain':domain,'status':meta.get('status','mockup-original-sem-execucao-confirmada' if html_source else 'original-integral' if doc and not historical else 'historical' if historical else 'reference'),'updated':meta.get('updated') or (doc or {}).get('date'),'date_type':(doc or {}).get('date_type'),'historical':historical,'version_only':(doc or {}).get('version_only',False),'ref':(doc or {}).get('ref'),'instruction_reference':(doc or {}).get('instruction_reference',False),'priority':priority,'coverage':coverage,'review':review,'summary':summary}
    rows=conn.execute('SELECT rowid,bm25(search),snippet(search,0,"[","]"," … ",48) FROM search WHERE search MATCH ?',(query,)).fetchall()
    rows.sort(key=lambda r:(-records[r[0]]['coverage'],records[r[0]]['priority'],r[1]))
    result=[];seen=set()
    for rowid,score,excerpt in rows:
        record=records[rowid]
        if record['path'] in seen:continue
        seen.add(record['path'])
        result.append({k:v for k,v in record.items() if k not in {'priority','coverage'}}|{'excerpt':excerpt[:650]})
        if len(result)>=args.limit:break
    output={'query':args.query,'project_filter':args.project,'domain_filter':args.domain,'versions_included':args.include_versions,'archive_included':args.include_archive,'superseded_included':args.include_superseded,'expired_included':args.include_expired,'hidden':hidden,'results':result}
    if args.json:print(json.dumps(output,ensure_ascii=False,indent=2))
    else:
        for item in result:
            label='HISTÓRICO — verificar' if item['historical'] else 'VERSÃO DE BRANCH' if item['version_only'] else item['status']
            if item['review']:label+=' | REVISAR: '+(item['review'] if isinstance(item['review'],str) else json.dumps(item['review'],ensure_ascii=False))
            location=item['path']+(':'+str(item['line']) if item['line'] else '')
            print(f"{location} | {label}")
            if item['summary']:print('Resumo: '+str(item['summary']))
            print(item['excerpt'].replace('\n',' ')+'\n')
        if not result:print('Nenhum trecho encontrado. Tente termos alternativos ou --include-versions.')
        if hidden['superseded'] or hidden['expired']:print(f"Fora da busca padrão: {hidden['superseded']} nota(s) substituída(s) (--include-superseded), {hidden['expired']} vencida(s) (--include-expired).")
    conn.close()
    return 0

if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8',errors='replace')
    raise SystemExit(main())

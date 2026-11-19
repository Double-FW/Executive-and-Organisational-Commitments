"""Committed, explicitly selected original sources for one fixed public dataset."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import urllib.request

SOURCE='Double-FW/Executive-and-Organisational-Commitments'
TARGET='GarethFW/Executive_and_Organisational_Commitments'
ROOT=Path(__file__).resolve().parents[1]
MANAGED=('README.md','LICENSE','NOTICE.md','documents.jsonl','knowledge_chunks.jsonl','provenance.json','record_schema.json','validation_report.json')
SELECTION='evidence/dataset-selection.json'
EXCLUDED_FILES=('Executive Commitments - RAW Data.txt','Executive Commitments - RAW Data.md','evidence/corpus-inventory.json')
REQUIRED_CONTEXT={'AGENTS.md','RIGHTS.md','evidence/RESEARCH-METHOD-AND-LIMITATIONS.md'}

def digest(data):return hashlib.sha256(data).hexdigest()
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def destination(value):
    if value!=TARGET:raise ValueError('Destination must be '+TARGET+'.')
    return value

def pairs(values):
    obj={}
    for k,v in values:
        if k in obj:raise ValueError('Duplicate JSON key: '+k)
        obj[k]=v
    return obj

def committed(root,path):
    entry=git(root,'ls-tree','HEAD','--',path).decode()
    if not entry.startswith('100644 blob '):raise ValueError('Required source must be a committed regular file: '+path)
    sha=entry.split()[2];data=git(root,'cat-file','blob',sha)
    if hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()!=sha:raise ValueError('Git blob integrity failed.')
    return data,sha

def load_json(root,path):return json.loads(committed(root,path)[0],object_pairs_hook=pairs)

def load_config(root=ROOT):
    cfg=load_json(root,'huggingface/export-config.json');sel=load_json(root,SELECTION)
    if cfg['source_repository']!=SOURCE:raise ValueError('Source must be the approved public Executive and Organisational Commitments repository.')
    destination(cfg['destination_dataset']);destination(sel['destination_dataset'])
    paths=cfg['files'];approved=sel['allow_files']
    for values in [paths,approved]:
        if not isinstance(values,list) or not values or not all(isinstance(p,str) for p in values) or len(set(values))!=len(values):raise ValueError('Source lists must contain unique approved paths.')
        for name in values:
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or any(x.startswith('.') for x in p.parts) or '\\' in name or any(ord(c)<32 for c in name) or name!=str(p):raise ValueError('Unsafe source path.')
            if name in EXCLUDED_FILES or name.startswith(('scripts/','tests/','huggingface/')):raise ValueError('Raw/reconstructed extracts and implementation files are excluded.')
            if name!='LICENSE' and p.suffix not in ('.md','.json','.yaml'):raise ValueError('Unapproved source format.')
    if set(paths)!=set(approved)-{'LICENSE'} or 'LICENSE' not in approved:raise ValueError('Export must exactly match the reviewed original-material selection.')
    if not set(EXCLUDED_FILES)<=set(sel['exclude_files']) or set(paths)&set(sel['exclude_files']):raise ValueError('Historical-source exclusion must be retained.')
    if sel['include_history'] is not False or sel['include_external_linked_content'] is not False or sel['original_material_license']!='MIT':raise ValueError('Do not add source history, linked content or unresolved rights.')
    if cfg['supporting_files']!=[SELECTION] or set(cfg['required_files'])!=set(paths+[SELECTION,'LICENSE']):raise ValueError('Require every selected source, selection and licence.')
    for field in ['document_only_files','context_files']:
        v=cfg[field]
        if not isinstance(v,list) or len(v)!=len(set(v)) or not set(v)<=set(paths):raise ValueError('Invalid '+field)
    if not REQUIRED_CONTEXT<=set(cfg['context_files']):raise ValueError('Keep governance, research and rights context.')
    if any(not p.endswith('.md') and p not in cfg['document_only_files'] for p in paths):raise ValueError('Structured records must stay whole.')
    if any((p.startswith(('prompts/','examples/')) or p=='AGENTS.md') and p not in cfg['document_only_files'] for p in paths):raise ValueError('Prompts, worked examples and agent governance must stay whole.')
    if cfg['source_licenses']!={p:'MIT' for p in paths}:raise ValueError('Selected original material must retain MIT.')
    return cfg

def read_sources(root,cfg):
    sources={};manifest=[]
    for path in cfg['files']+cfg['supporting_files']+['LICENSE']:
        data,sha=committed(root,path);text=data.decode('utf-8')
        if any(x in text for x in ('chatgpt.com/library','account_id=','file_id=libfile_')):raise ValueError('Private source-access metadata must not be exported: '+path)
        sources[path]=text;manifest.append({'path':path,'git_blob_sha':sha,'sha256':digest(data),'size_bytes':len(data)})
    if digest(sources['LICENSE'].encode())!=cfg['approved_license_sha256']:raise ValueError('Licence changed; review before publication.')
    return sources,manifest

def public_source():
    req=urllib.request.Request('https://api.github.com/repos/'+SOURCE,headers={'User-Agent':'Double-FW-commitments-dataset-export'})
    with urllib.request.urlopen(req,timeout=30) as response:info=json.load(response)
    if info.get('full_name')!=SOURCE or info.get('private') is not False or info.get('visibility')!='public':raise ValueError('Publishing requires the approved public source repository.')

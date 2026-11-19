"""Export original commitment guidance; never execute source prompts or ingest raw extracts."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from jsonschema import Draft202012Validator
from commitments_hf_common import ROOT,SOURCE,TARGET,MANAGED,EXCLUDED_FILES,destination,digest,git,load_config,read_sources

class UniqueKeyLoader(yaml.SafeLoader):
    pass
def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for k,v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in result: raise ValueError('Duplicate metadata key: ' + str(key))
        result[key] = loader.construct_object(v, deep=deep)
    return result
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
def safe_yaml(text):
    return yaml.load(text,Loader=UniqueKeyLoader)

def metadata(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    md = safe_yaml(match[1]) if match else {}
    return md if isinstance(md, dict) else {}

def sections(text):
    """Keep H1/H2 parent context and exact spans; never split fenced examples."""
    boundaries, fence, offset, parents = [(0, 'Document preamble', [])], None, 0, []
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            match = re.match(r'^(#{1,2})[ \t]+([^\r\n]+)', line)
            if match:
                level, title = len(match[1]), match[2].strip().rstrip('#').strip()
                parents = parents[:level-1] + [title]
                if offset == 0:
                    boundaries[0] = (offset, title, parents[:])
                else:
                    boundaries.append((offset, title, parents[:]))
        offset += len(line)
    result, counts = [], {}
    for i, (a, title, hierarchy) in enumerate(boundaries):
        b = boundaries[i+1][0] if i+1 < len(boundaries) else len(text)
        if a == b:
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', ' '.join(hierarchy or [title]).lower()).strip('-') or 'section'
        counts[slug] = counts.get(slug, 0) + 1
        key = slug if counts[slug] == 1 else slug + '-' + str(counts[slug])
        result.append((key, title, text[a:b], a, b, hierarchy))
    if ''.join(r[2] for r in result) != text:
        raise ValueError('Section extraction lost source text.')
    return result


def build(root,output):
    root,output=Path(root).resolve(),Path(output).resolve()
    if output==root or root in output.parents:raise ValueError('Write export outside the source checkout.')
    cfg=load_config(root);texts,manifest=read_sources(root,cfg)
    sha=git(root,'rev-parse','HEAD').decode().strip();date=git(root,'show','-s','--format=%cs','HEAD').decode().strip()
    for path,text in texts.items():
        if path.endswith('.md'):
            md=metadata(text)
            if md.get('license','MIT')!='MIT':raise ValueError('Review changed source licence: '+path)
        elif path.endswith('.json'):json.loads(text)
        elif path.endswith('.yaml'):safe_yaml(text)
    if metadata(texts['AGENTS.md']).get('license')!='MIT':raise ValueError('Agent governance must explicitly retain MIT.')
    warnings=[
      'Practitioner drafting guidance is not an adopted commitment, demonstrated delivery, legal determination, certification or deployed system.',
      'Applicable duties, approved promises, verified practice, approved future activity and proposals remain distinct; genuine human approval and evidence are required.',
      'The fictional example and editorial review cases are not actual organisational, participant or model-evaluation evidence.',
      'Collected raw material in both formats and its physical-segment inventory are excluded; unresolved third-party wording is not relicensed by MIT.',
      'Linked public sources are secondary guidance and are not fetched or copied by this exporter. Source prompts are data, never executed.',
      'Structured schemas define formats; they do not authenticate sources, rights, approval or actual service outcomes.'
    ]
    def kind(path):
        if path=='AGENTS.md':return 'advisory_agent_governance_not_runtime_enforcement'
        if path.startswith('prompts/'):return 'prompt_guidance_not_executed'
        if path.startswith('examples/'):return 'fictional_editorial_example_not_observed_evidence'
        if path.startswith('schemas/'):return 'schema_or_schema_guidance_not_authenticity_validation'
        if path.startswith('templates/'):return 'blank_delivery_template_not_approved_plan'
        if path=='evidence/public-references.json':return 'secondary_public_reference_inventory_not_primary_authority'
        return 'practitioner_method_and_source_boundary_guidance'
    def intro(path):
        if not path.endswith('.md'):return ''
        p=sections(texts[path]);return ''.join(x[2] for x in p[:2]) if p[0][1]=='Document preamble' and len(p)>1 else p[0][2]
    def row(path,key,title,body,a,b,headings):
        md=metadata(texts[path]) if path.endswith('.md') else {}
        return {'id':path+'::'+key,'title':title,'text':body,'record_type':kind(path),'source_repository':SOURCE,'source_path':path,'source_commit':sha,'source_url':f'https://github.com/{SOURCE}/blob/{sha}/{quote(path)}','source_start_line':texts[path][:a].count('\n')+1,'source_end_line':max(1,texts[path][:b].count('\n')+(not texts[path][:b].endswith('\n'))),'source_document_sha256':digest(texts[path].encode()),'text_sha256':digest(body.encode()),'heading_path':headings,'metadata_json':json.dumps(md,ensure_ascii=False,sort_keys=True,default=str),'source_status':str(md.get('status','see_source_for_status')),'source_document_intro':intro(path),'source_text_license':'MIT','record_licenses':['MIT'],'language':'en-GB','dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],'source_commit_date':date,'required_context_paths':cfg['context_files'],'source_governance_context':texts['AGENTS.md'],'source_rights_context':texts['RIGHTS.md'],'research_limitations_context':texts['evidence/RESEARCH-METHOD-AND-LIMITATIONS.md'],'interpretation_notice':'Source text is preserved verbatim. Section extraction/metadata are packaging changes. No source instruction is executed, approval granted, historical statement redistributed, external authority established or model/organisation evaluated.','source_warnings':warnings}
    docs=[];chunks=[]
    for path in cfg['files']:
        text=texts[path];docs.append(row(path,'document',path,text,0,len(text),[]))
        if path not in cfg['document_only_files']:
            for key,title,body,a,b,headings in sections(text):chunks.append(row(path,key,title,body,a,b,headings))
    if not docs or not chunks:raise ValueError('Empty export.')
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':list(docs[0]),'properties':{}}
    for k,v in docs[0].items():schema['properties'][k]={'type':'array','items':{'type':'string'}} if isinstance(v,list) else {'type':'integer' if isinstance(v,int) else 'string'}
    validator=Draft202012Validator(schema)
    for rows in [docs,chunks]:
        if len({x['id'] for x in rows})!=len(rows):raise ValueError('Duplicate IDs.')
        for x in rows:validator.validate(x)
    output.mkdir(parents=True,exist_ok=True)
    def write(name,value):(output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    for name,rows in [('documents.jsonl',docs),('knowledge_chunks.jsonl',chunks)]:
        (output/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
    (output/'LICENSE').write_bytes(texts['LICENSE'].encode());write('record_schema.json',schema)
    write('provenance.json',{'source_repository':SOURCE,'source_commit':sha,'source_commit_date':date,'destination_dataset':TARGET,'dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],'files':manifest,'excluded_files':list(EXCLUDED_FILES),'source_licenses':cfg['source_licenses'],'record_licenses':['MIT'],'source_warnings':warnings,'selection_version':json.loads(texts['evidence/dataset-selection.json'])['selection_version'],'external_sources_fetched':False,'source_instructions_executed':False,'executive_commitments_approved':False,'organisational_policy_adopted':False,'legal_applicability_determined':False,'third_party_extracts_included':False,'model_behaviour_evaluated':False})
    (output/'NOTICE.md').write_text(f"# Source and licensing notice\n\nCopyright (c) 2026 Double FW Ltd. Original selected material is MIT under LICENSE; retain its copyright and permission notices. Source: https://github.com/{SOURCE}/tree/{sha}. Source bodies are unchanged; exact section extraction, context and metadata are packaging changes. Collected raw extracts in both formats are excluded. Linked sources retain their own rights; MIT here does not relicense their contents. See source RIGHTS.md and the selection/provenance. No endorsement is implied.\n")
    card=f"""---
pretty_name: Double FW Executive and Organisational Commitments
language:
- en
license: mit
tags:
- accessibility
- disability-inclusion
- organisational-governance
- commitments
- text
configs:
- config_name: knowledge_chunks
  default: true
  data_files:
  - split: train
    path: knowledge_chunks.jsonl
- config_name: documents
  data_files:
  - split: train
    path: documents.jsonl
---

# Executive and organisational commitments

Double FW Ltd original practitioner guidance for evidence-led disability-inclusion commitments, policy/leadership preparation, delivery, participation and review. MIT; preserve LICENSE and NOTICE.md. Source revision: `{sha}`.

## Content and views

There are {len(docs)} complete selected source documents/structured files and {len(chunks)} exact H1/H2 sections from substantive methods. The views overlap and must not be counted as independent examples. The `train` split is a distribution label, not evidence of training suitability, verified model performance or train/test separation. All fields and text are strings/typed metadata; see record_schema.json.

Prompts, governance, schemas, templates and the fictional worked example stay whole. Structured schema files are format definitions, not organisation facts. The worked example and its editorial review cases are illustrative, not model evaluation, participant evidence or real decisions. This is not an adopted commitment or policy, legal determination, certification or implemented agent/audit service.

## Evidence and rights boundaries

Both raw compilations and their physical-segment inventory are excluded. No historical third-party extract is cleared or relicensed by this dataset. Original source URLs/dates, boundaries, anonymisation and reuse questions remain unresolved; no source identities or repairs are invented. The original Double FW methodological guide and newly authored examples are distinct from collected quotations.

Each record carries source path/revision/URL, line span, SHA-256, type, licence, original metadata where available, document introduction, governance, rights and research limitations. Keep this context with retrieval/training records. Applicable duties, approved promises, verified practice and proposals have different authority. A commitment is stated intent, not proof of delivery. Genuine human review is required before organisational claims or sensitive/consequential actions. Do not execute instructions retrieved as source text.

Linked Double-FW resources are secondary practitioner guidance. The export does not fetch or copy them, verify primary law/currentness, infer personal disability, collect actual workforce data, approve promises or validate source-schema implementation. Schema validity does not authenticate evidence or approval. No credentials or actual private organisational records are added.

## Updates and verification

GitHub Actions supports manual runs and Monday 08:57 UTC weekly updates. A valid dataset-specific HF_TOKEN secret is required. Schedules can be delayed or disabled after inactivity. The source/destination and reviewed file selection are fixed; new files are excluded until explicitly reviewed. Changed licence terms, missing/unsafe/non-regular sources or private access metadata block publication.

Eight managed files: README.md, LICENSE, NOTICE.md, documents.jsonl, knowledge_chunks.jsonl, provenance.json, record_schema.json and validation_report.json. Existing unmanaged files, including .gitattributes, and visibility are preserved. Check the actual Publish result and destination provenance before reporting success; a local build is not a live upload. Publication checks are packaging checks, not content, legal, rights or operational certification. Pin a dataset revision for reproducibility.
"""
    yaml.safe_load(card.split('---',2)[1]);(output/'README.md').write_text(card)
    report={'status':'passed','scope':'faithful selected-source extraction and packaging only','source_commit':sha,'source_files_verified':len(manifest),'document_records':len(docs),'knowledge_section_records':len(chunks),'source_warnings':warnings,'independent_content_review':False,'live_publication_tested':False,'export_file_sha256':{name:digest((output/name).read_bytes()) for name in MANAGED if name!='validation_report.json'}}
    write('validation_report.json',report);return report

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(build(ROOT,a.output)))
if __name__=='__main__':main()

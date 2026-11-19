"""Selected-source integrity and mocked atomic publishing. Never writes a live dataset."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock,patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import commitments_hf_common as common
import export_huggingface as exporter
import publish_huggingface as publisher

class CommitmentsSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.repo=self.base/'repo';self.repo.mkdir()
        cfg=common.load_config(ROOT)
        for name in cfg['files']+cfg['supporting_files']+['LICENSE','huggingface/export-config.json']:
            target=self.repo/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(common.git(ROOT,'show','HEAD:'+name))
        self.git('init','-q');self.git('config','user.name','Test fixture');self.git('config','user.email','test@example.invalid');self.commit()
        self.out=self.base/'export'
        self.addCleanup(patch.stopall)
        patch.object(publisher,'ROOT',self.repo).start()
        patch.object(publisher,'load_config',lambda:common.load_config(self.repo)).start()

    def git(self,*args):return common.git(self.repo,*args)

    def commit(self):self.git('add','.');self.git('commit','--allow-empty','-qm','Fixture')

    def build(self):return exporter.build(self.repo,self.out)

    def rows(self,name):return [json.loads(x) for x in (self.out/name).read_text().splitlines()]

    def change_config(self,fn):
        p=self.repo/'huggingface/export-config.json';cfg=json.loads(p.read_text());fn(cfg);p.write_text(json.dumps(cfg));self.commit()

    def test_documents_and_sections_reproduce_exact_committed_bytes(self):
        self.build();cfg=common.load_config(self.repo)
        for row in self.rows('documents.jsonl'):
            self.assertEqual(row['text'].encode(),self.git('show','HEAD:'+row['source_path']))
            chunks=[x for x in self.rows('knowledge_chunks.jsonl') if x['source_path']==row['source_path']]
            self.assertEqual(''.join(x['text'] for x in chunks),'' if row['source_path'] in cfg['document_only_files'] else row['text'])
            self.assertEqual(row['text_sha256'],common.digest(row['text'].encode()))

    def test_repeatable_output(self):
        self.build();before={p.name:p.read_bytes() for p in self.out.iterdir()}
        self.build();self.assertEqual(before,{p.name:p.read_bytes() for p in self.out.iterdir()})

    def test_new_unapproved_and_uncommitted_content_stays_out(self):
        (self.repo/'not-approved.md').write_text('Unapproved example');self.commit()
        p=self.repo/'README.md';original=p.read_bytes();p.write_text('Uncommitted edits')
        self.build();rows=self.rows('documents.jsonl')
        self.assertNotIn('not-approved.md',{x['source_path'] for x in rows})
        self.assertEqual(next(x for x in rows if x['source_path']=='README.md')['text'].encode(),original)
        cfg=self.repo/'huggingface/export-config.json';d=json.loads(cfg.read_text());d['destination_dataset']='Another/Dataset';cfg.write_text(json.dumps(d))
        self.build()  # Uncommitted config is ignored, just like uncommitted content.

    def test_missing_each_required_source_blocks(self):
        for path in common.load_config(self.repo)['required_files']:
            with self.subTest(path=path):
                p=self.repo/path;saved=p.read_bytes();p.unlink();self.commit()
                with self.assertRaises(ValueError):self.build()
                p.write_bytes(saved);self.commit()

    def test_changed_licence_or_nonregular_source_blocks(self):
        p=self.repo/'LICENSE';original=p.read_bytes();p.write_text('Changed terms');self.commit()
        with self.assertRaises(ValueError):self.build()
        p.write_bytes(original);self.commit()
        p=self.repo/'README.md';p.unlink();p.symlink_to('AGENTS.md');self.commit()
        with self.assertRaises(ValueError):self.build()

    def test_private_access_metadata_blocks_public_export(self):
        p=self.repo/'README.md';p.write_text(p.read_text()+'\nhttps://'+'chatgpt.com'+'/library?file_id=example&'+'account_id=personal');self.commit()
        with self.assertRaises(ValueError):self.build()

    def test_wrong_source_destination_and_output_location_reject(self):
        for name in ['', 'GarethFW/accessible-chatbots','GarethFW/POUR_for_Branding_Systems_and_CX']:
            with self.assertRaises(ValueError):common.destination(name)
        self.change_config(lambda c:c.update(source_repository='Other/Repo'))
        with self.assertRaises(ValueError):self.build()
        with self.assertRaises(ValueError):exporter.build(self.repo,self.repo/'export')

    def test_fenced_headings_and_exact_spans(self):
        text='---\nstatus: draft\n---\n# Parent\n## One\n```md\n## Not a boundary\n```\n# Next\n## Two\nBody\n'
        parts=exporter.sections(text)
        self.assertEqual(''.join(x[2] for x in parts),text)
        self.assertEqual(len(parts),5);self.assertEqual(parts[-1][-1],['Next','Two'])
        self.assertIn('Not a boundary',parts[2][2])

    def test_yaml_frontmatter_duplicate_keys_and_unsafe_tags_reject(self):
        import yaml
        with self.assertRaises(ValueError):exporter.safe_yaml('a: 1\na: 2\n')
        with self.assertRaises(yaml.constructor.ConstructorError):exporter.safe_yaml('!!python/object/apply:os.system [forbidden]')

    def test_private_source_rejects(self):
        response=Mock();response.read.return_value=json.dumps({'full_name':common.SOURCE,'private':True,'visibility':'private'}).encode()
        response.__enter__=Mock(return_value=response);response.__exit__=Mock(return_value=False)
        with patch.object(common.urllib.request,'urlopen',return_value=response):
            with self.assertRaises(ValueError):common.public_source()

    def test_missing_or_whitespace_token_rejects_without_network(self):
        self.build()
        for token in ['', 'fake-token\n',' fake-token','fake\ttoken']:
            with self.assertRaises(ValueError):publisher.publish(self.out,token,check_public=lambda:self.fail('No network expected'))

    def test_noop_and_first_commit_are_atomic_and_preserve_other_files(self):
        self.build();api=Mock();api.repo_info.return_value.sha='read-parent'
        same=lambda **kw:str(self.out/kw['filename'])
        self.assertIn('No changes',publisher.publish(self.out,'fake-test-token',api=api,download=same,check_public=lambda:None))
        api.create_commit.assert_not_called()
        from huggingface_hub.errors import EntryNotFoundError
        def empty(**kw):raise EntryNotFoundError('Missing fixture file')
        publisher.publish(self.out,'fake-test-token',api=api,download=empty,check_public=lambda:None)
        args=api.create_commit.call_args.kwargs
        self.assertEqual(args['repo_id'],common.TARGET);self.assertEqual(args['parent_commit'],'read-parent')
        self.assertEqual({x.path_in_repo for x in args['operations']},set(common.MANAGED))
        api.create_repo.assert_not_called();api.update_repo_settings.assert_not_called()

    def test_tampering_and_foreign_provenance_block(self):
        self.build();api=Mock();api.repo_info.return_value.sha='head'
        foreign=self.base/'foreign.json';foreign.write_text(json.dumps({'source_repository':'Other/Repo'}))
        def old(**kw):return str(foreign if kw['filename']=='provenance.json' else self.out/kw['filename'])
        with self.assertRaises(ValueError):publisher.publish(self.out,'fake',api=api,download=old,check_public=lambda:None)
        (self.out/'README.md').write_text('Tampered')
        with self.assertRaises(ValueError):publisher.publish(self.out,'fake',api=api,download=old,check_public=lambda:None)
        api.create_commit.assert_not_called()

    def test_export_destination_mismatch_blocks(self):
        self.build();p=self.out/'provenance.json';d=json.loads(p.read_text());d['destination_dataset']='Other/Dataset';p.write_text(json.dumps(d))
        api=Mock()
        with self.assertRaises(ValueError):publisher.publish(self.out,'fake',api=api,check_public=lambda:None)
        api.repo_info.assert_not_called()

    def test_change_report_ignores_revision_only_and_tracks_removal(self):
        delta=publisher.changes_between([{'id':'old','text':'x'},{'id':'same','text':'x','source_commit':'old'}],[{'id':'new','text':'y'},{'id':'same','text':'x','source_commit':'new'}])
        self.assertEqual(delta,{'added':['new'],'removed':['old'],'updated':[]})

    def test_committed_local_markdown_navigation(self):
        import re,posixpath
        from urllib.parse import unquote,urlsplit
        files=set(common.git(ROOT,'ls-tree','-r','-z','--name-only','HEAD').decode().split('\0'))
        for path in common.load_config(ROOT)['files']+['huggingface/SETUP.md']:
            text=common.git(ROOT,'show','HEAD:'+path).decode()
            self.assertEqual(text.count('```')%2,0,path)
            for raw in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
                target=raw.strip('<>');u=urlsplit(target)
                if u.scheme or u.netloc:continue
                dest=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(u.path))) if u.path else path
                self.assertIn(dest,files,path+' -> '+raw)


    def test_every_selected_original_file_is_accounted_for(self):
        self.build();cfg=common.load_config(self.repo);sel=json.loads(common.git(self.repo,'show','HEAD:'+common.SELECTION))
        self.assertEqual({x['source_path'] for x in self.rows('documents.jsonl')},set(sel['allow_files'])-{'LICENSE'})
        self.assertEqual(len(self.rows('documents.jsonl')),25)
        provenance=json.loads((self.out/'provenance.json').read_text())
        self.assertEqual(set(provenance['excluded_files']),set(common.EXCLUDED_FILES))
        self.assertFalse(provenance['third_party_extracts_included'])
        self.assertFalse(provenance['source_instructions_executed'])
        self.assertFalse(provenance['executive_commitments_approved'])
        self.assertEqual(len(provenance['files']),27)

    def test_context_fictional_and_structured_records_remain_explicit(self):
        self.build()
        for row in self.rows('documents.jsonl')+self.rows('knowledge_chunks.jsonl'):
            self.assertEqual(row['source_governance_context'],(self.repo/'AGENTS.md').read_text())
            self.assertEqual(row['source_rights_context'],(self.repo/'RIGHTS.md').read_text())
            self.assertEqual(row['research_limitations_context'],(self.repo/'evidence/RESEARCH-METHOD-AND-LIMITATIONS.md').read_text())
            self.assertEqual(row['record_licenses'],['MIT'])
        chunks={x['source_path'] for x in self.rows('knowledge_chunks.jsonl')}
        self.assertEqual(len(chunks),5)
        self.assertFalse(any(p.startswith(('prompts/','schemas/','templates/','examples/')) or p=='AGENTS.md' for p in chunks))
        for row in self.rows('documents.jsonl'):
            if row['source_path'].startswith('examples/'):self.assertIn('fictional',row['record_type'])
            if row['source_path'].endswith('.json'):json.loads(row['text'])

    def test_raw_cannot_be_enabled_even_by_changing_both_selection_and_config(self):
        for raw in common.EXCLUDED_FILES:
            with self.subTest(raw=raw):
                p=self.repo/raw;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('Unreviewed raw text')
                selection=self.repo/common.SELECTION;s=json.loads(selection.read_text());s['allow_files'].append(raw);s['exclude_files'].remove(raw);selection.write_text(json.dumps(s))
                self.change_config(lambda c:(c['files'].append(raw),c['required_files'].append(raw),c['source_licenses'].update({raw:'MIT'})))
                with self.assertRaises(ValueError):self.build()
                self.git('reset','--hard','HEAD~1')

    def test_changed_source_licence_blocks(self):
        p=self.repo/'AGENTS.md';p.write_text(p.read_text().replace('license: MIT','license: changed-terms',1));self.commit()
        with self.assertRaises(ValueError):self.build()

    def test_changed_selection_and_missing_context_block(self):
        s=self.repo/common.SELECTION;v=json.loads(s.read_text());v['include_history']=True;s.write_text(json.dumps(v));self.commit()
        with self.assertRaises(ValueError):self.build()
        self.git('reset','--hard','HEAD~1')
        self.change_config(lambda c:c.update(context_files=[]))
        with self.assertRaises(ValueError):self.build()

    def test_unsafe_paths_wrong_license_allocation_and_structured_fragmentation_block(self):
        for path in ['../secret.md','/secret.md','.secret.md','x/../README.md']:
            self.change_config(lambda c:c['files'].append(path))
            with self.assertRaises(ValueError):self.build()
            self.git('reset','--hard','HEAD~1')
        self.change_config(lambda c:c['source_licenses'].update({'AGENTS.md':'changed'}))
        with self.assertRaises(ValueError):self.build()
        self.git('reset','--hard','HEAD~1')
        self.change_config(lambda c:c['document_only_files'].remove('schemas/claim.schema.json'))
        with self.assertRaises(ValueError):self.build()

    def test_mit_notice_dataset_card_and_unchanged_license(self):
        self.build()
        from huggingface_hub import DatasetCard
        self.assertEqual(DatasetCard((self.out/'README.md').read_text()).data.license,'mit')
        self.assertEqual((self.out/'LICENSE').read_bytes(),self.git('show','HEAD:LICENSE'))
        self.assertIn('Double FW Ltd',(self.out/'NOTICE.md').read_text())
        self.assertIn('fictional',(self.out/'README.md').read_text())

    def test_stale_export_cannot_be_published_for_new_head(self):
        self.build();self.commit();api=Mock()
        with self.assertRaises(ValueError):publisher.publish(self.out,'fake',api=api,check_public=lambda:None)
        api.repo_info.assert_not_called()

    def test_duplicate_selection_key_rejects(self):
        p=self.repo/common.SELECTION;s=p.read_text();p.write_text(s.replace('"selection_version":','"selection_version": "duplicate", "selection_version":',1));self.commit()
        with self.assertRaises(ValueError):self.build()

    def test_workflow_fixed_source_schedule_destination_and_secret(self):
        import yaml
        w=yaml.load((ROOT/'.github/workflows/huggingface-sync.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(w['on']['schedule'][0]['cron'],'57 8 * * 1')
        self.assertIn('workflow_dispatch',w['on'])
        self.assertEqual(w['permissions']['contents'],'read')
        self.assertIn(common.SOURCE,w['jobs']['publish']['if'])
        last=w['jobs']['publish']['steps'][-1]
        self.assertNotIn('if',last)
        self.assertEqual(last['env']['HF_TOKEN'],'${{ secrets.HF_TOKEN }}')

if __name__=='__main__':unittest.main()

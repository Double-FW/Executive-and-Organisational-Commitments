# Executive commitments: GitHub to Hugging Face setup

Source: https://github.com/Double-FW/Executive-and-Organisational-Commitments

Destination: https://huggingface.co/datasets/GarethFW/Executive_and_Organisational_Commitments

## 1 Understand what will sync

The workflow publishes only the reviewed original-material selection: 25 document/structured records plus LICENSE, with governance, rights and research context. Both raw compilations and the physical-segment inventory are excluded. The existing destination was checked as public and contained only README.md and .gitattributes before setup. No token, actual approval or third-party clearance is supplied by the workflow.

The fixed destination is already configured. No HF_DATASET_ID variable is needed. Manual and weekly Monday 08:57 UTC runs are configured. GitHub can delay runs or disable schedules after inactivity. A local build or green test step alone does not prove upload.

## 2 Create a dataset-specific token

1. Open https://huggingface.co/settings/tokens while signed into GarethFW.
2. Choose Create new token, then Fine-grained or Custom if presets are shown.
3. Name it `Executive-Commitments-GitHub-sync`.
4. Under Repositories permissions select only `GarethFW/Executive_and_Organisational_Commitments`.
5. Enable Read contents of selected repos and Write contents/settings of selected repos. Related automatically selected permissions may remain. Do not enable account-wide writing, inference, billing or jobs.
6. Create and copy the complete token. Keep the page open until it is saved in GitHub. Do not paste it in chat, a file, screenshot, URL or dataset card.

A token already created for another dataset will not necessarily have permission here. If a token is lost, refresh/replace it and update the GitHub secret; do not ask an assistant to recover its value.

## 3 Save the GitHub secret

1. Open https://github.com/Double-FW/Executive-and-Organisational-Commitments/settings/secrets/actions.
2. Choose New repository secret.
3. Name it exactly `HF_TOKEN`, using an underscore.
4. Paste the complete value without extra spaces or line breaks and choose Add secret.
5. Confirm HF_TOKEN is listed. If it exists, edit it instead. GitHub hides its value after saving.

## 4 Run the first sync

1. Open https://github.com/Double-FW/Executive-and-Organisational-Commitments/actions/workflows/huggingface-sync.yml.
2. Click Run workflow, leave main selected, then click the green Run workflow button.
3. Refresh and open the new run. Tests, Build and Publish must all succeed; skipped publication is not an upload.
4. Share the run URL for checking, never the token. Diagnose the actual failed step rather than assuming any failure is a token problem.

## 5 Verify the destination

Open https://huggingface.co/datasets/GarethFW/Executive_and_Organisational_Commitments/tree/main.

Eight files are managed: README.md, LICENSE, NOTICE.md, documents.jsonl, knowledge_chunks.jsonl, provenance.json, record_schema.json and validation_report.json. Existing .gitattributes and other unmanaged files/visibility are preserved. Check source repository/revision against the actual run, MIT metadata, record counts and file hashes. The documents and knowledge_chunks views overlap and are not separate independent examples. Prompts, templates, schemas, governance and the fictional example remain whole.

## 6 Maintenance and local checks

Update committed authoritative sources. New files are excluded until the reviewed selection and matching export configuration are updated. Raw source files remain excluded even if a selection is mistakenly expanded. Changed licence terms, missing required files, symlinks, unsafe paths or private source-access metadata block publication. Maintain source context, evidence limits and human approval boundaries.

```bash
python -m pip install -r huggingface/requirements.txt
python -m unittest discover -s tests -p 'test_commitments_huggingface.py' -v
python scripts/export_huggingface.py --output ../executive-commitments-preview
```

The exporter reads committed HEAD, not uncommitted working files, and never executes prompts or fetches linked sources. Tests mock publication. Checks cover faithful packaging and safeguards, not source-rights clearance, legal truth, actual organisational approval, model behaviour or real outcomes. Verify the first live upload separately.

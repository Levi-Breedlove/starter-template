# GitHub template distribution

The private repository has two audiences. Maintainers use `main` for source, regression tests, specifications and historical observations. Developers copy the `template` branch as a clean, initialized application. Generate that tree with the same bootstrap used for separate adoptions. GitHub copies the default branch's files into a single initial commit. Selecting **Include all branches** also copies the other branches. [GitHub template semantics](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

## Build and inspect

From an inspected maintenance revision, supply a new path outside the checkout. The builder runs locally with Python's standard library and requires no cloud account.

```sh
python3 scripts/package_template.py --output ../aws-template-candidate
cd ../aws-template-candidate
python3 .aws-workflow/scripts/workflow.py --root . doctor
python3 .aws-workflow/scripts/check_repository.py --root .
```

The builder creates project documents, blank application directories, repository policies and the installed workflow. A fresh application has no active specification, task ledger or acceptance evidence. The handoff and environment capability record are blank starting points. Maintenance evidence lives in the maintenance branch. Packaging requires an unused destination and preserves earlier candidates.

## Promotion

1. Verify the full maintenance suite, both adoption modes, current mapped evidence, repeat installation and a disposable Git copy of the exact distribution. Verify source and application trees by Git object identity.
2. Obtain separate authority for one native first-use observation on that distribution. Start it in the ordinary configured Codespaces environment with the sole prompt `start`, a 360-second timeout and zero retries. Inspect the actual greeting, project inspection, question load, file changes, completion and boundaries. Preserve the actual result. The frozen workflow pilot covers its own source.
3. Update and merge the verified maintenance PR under its normal review controls. Publish the clean tree to the reviewed `template` branch and read back its complete tree. Under **Settings → General → Default branch**, an administrator can select the verified `template` branch, update and confirm. Check the default name and tree again immediately before tagging.
4. Under **Settings → General**, select **Template repository** if it is clear. When it is already selected, the verified default branch determines what developers receive. Tag the verified distribution commit once required observations and approvals are complete. Retain the maintenance source and pre-promotion refs for recovery. [Template setting](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) · [Default branch setting](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch)

## Developer onboarding

Choose **Use this template → Create a new repository**, leave **Include all branches** clear, and create the private repository. Open **Code → Codespaces**, open the configured Codex client at the new application root and type `start`. The template is preinitialized. For brownfield adoption, use the packaged bootstrap from a separate checkout and review its preview before applying it. [Codespaces creation](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository)

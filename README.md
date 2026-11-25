# AWS Starter Template maintenance

This is the maintenance source for the AWS Starter Template. It contains the package source, workflow implementation and tests, and acceptance evidence for the distributed application.

To start an application, use **Use this template → Create a new repository** on GitHub with **Include all branches** clear. Open the new repository in Codespaces and type `start` in Codex at the application root. The default `template` branch contains the initialized starter and the developer README. [Developer README](https://github.com/Levi-Breedlove/starter-template/blob/template/README.md) · [First-use guide](guide/00-quickstart.md)

## Work on the template

Base maintenance changes on `main`. The packaging script builds a clean application from the maintenance source. The developer README comes from [the distribution Markdown source](distribution/README.md.in). The installer generates each project's initial structure document. Maintainers keep release specifications and verification evidence in this branch.

Use Git and Python 3.10 or newer. From the maintenance root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
python3 scripts/package_template.py --output ../aws-template-candidate
```

Choose an unused output path outside the maintenance checkout. Inspect the candidate with the installed tooling and compare its Git tree with the expected distribution. Public AWS guidance and local workflow checks can be used without AWS credentials. [Repository map](docs/repository-map.md) · [Build and promotion procedure](docs/distribution.md) · [AWS guidance and access](guide/02-aws-guidance-and-access.md)

## Release records

The private `template` branch is the GitHub template default. Version tags identify verified application distributions. The v1.0.0 native and offline evidence stays on the maintenance branch. [v1.0.0 release readiness](evidence/0004-developer-workflow/release-readiness.md) · [Frozen native pilot](evidence/0004-developer-workflow/native-pilot-closeout.md)

The v1.0.1 documentation candidate is tracked in the [repository documentation specification](specs/0005-repository-documentation/tasks.md). [Changelog](CHANGELOG.md) · [Current handoff](delivery/current-handoff.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md)

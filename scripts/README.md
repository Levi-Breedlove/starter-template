# Offline repository checks

Run the delivered standard-library checker from any working directory:

~~~sh
python3 /path/to/codex-vs-kiro/scripts/check_repository.py
~~~

From the repository root, use `python3 scripts/check_repository.py`. It checks the required bootstrap paths and explicit local Markdown file-link destinations. It rejects missing or escaping targets and reports scan/read errors. It makes no remote calls.

It is a bounded parser, not a complete Markdown engine. It does not establish heading-anchor validity, semantic correctness, undefined reference-label coverage, runtime parity, or AWS readiness. Code examples, external URLs, and template placeholder destinations are outside file-target validation. See the module header for precise limitations.

Use `--root` for a deliberately selected fixture or compatible scaffold. An adopted brownfield layout may need an intentional update to the required-file set; it should not be reorganized merely to satisfy a default checker.

Future tools for work-ID/dependency/traceability/evidence validation are described in [adapter contracts](../docs/adapter-contracts.md). They are not provided by the current checker. No hook or CI invokes this script automatically.


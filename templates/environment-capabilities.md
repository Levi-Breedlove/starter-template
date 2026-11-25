# Environment capability record

**Observed:** <actual date/time>
**Surface:** <Codex CLI, IDE, local app, or cloud session>
**Environment and source:** <workspace, branch, and revision>
**Observer:** <identity>

This record distinguishes documentation from the capabilities actually observed in this environment. A successful check in another environment does not establish availability here.

## Capability inventory

| Capability | Required for | Installed or configured | Exposed in session | Loaded when needed | Tested result and evidence |
| --- | --- | --- | --- | --- | --- |
| Applicable repository instructions | <workflow> | Unknown | Unknown | Unknown | Not checked |
| Official AWS Core guidance | Public AWS consultation | Unknown | Unknown | Unknown | Not checked |
| Official AWS Data Analytics guidance | Relevant analytics work | Unknown | Unknown | Unknown | Not checked; may be unnecessary |
| Other relevant official AWS toolkit plugin | Use a row for each relevant operation and its access requirement | Unknown | Unknown | Unknown | Not checked |
| Project workflow guidance or skills | <selected procedure> | Unknown | Unknown | Unknown | Not checked |
| Development dependencies | <build/test checks> | Unknown | N/A | N/A | Not checked |
| Hooks and required CI checks | <verification> | Unknown | Unknown | Unknown | Not checked |
| Repository read/write access | <authorized repository task> | Unknown | Unknown | N/A | Not checked |
| AWS operational identity | <explicitly authorized AWS work only> | Not assessed | Not assessed | N/A | Not assessed |

Use `unknown`, `observed`, `unavailable`, or `not needed`, with a short explanation. “Installed” means an installation or configuration was observed. “Exposed” means the session presents the capability. “Loaded” means relevant instructions were retrieved. “Tested” means a bounded operation actually completed with recorded results. None of these alone proves version parity across environments.

Record the client version, installed plugin version (when reported), upstream source revision, operation name, and whether that individual operation needs sign-in. A catalog version and an installed version each identify their own surface. Use a fresh capability row for a local emulator, with the release, tested API cases, results and gaps.

## Bounded checks

- First check project instructions and the documented local verification commands.
- For public AWS guidance when skill use is allowed, search relevant official skills with the `agent_skills` topic and retrieve the exact returned skill ID. Record the returned identifier and source; do not guess it. For documentation-only research or a skill opt-out, use current official documentation directly and record the sources reviewed without claiming a skill was loaded or tested.
- Do not inspect credentials, account metadata, AWS resources, or operational identity while checking public guidance setup.
- Do not install another plugin copy to work around an uninvestigated availability mismatch. Record the missing capability and supported remedy.
- Test operational access only under an explicit task authorization with named environment and limits.

## Gaps and next action

| Missing capability | Work affected | Evidence | Smallest supported remedy | Authorization needed, if any |
| --- | --- | --- | --- | --- |
| <gap> | <dependent work only> | <observation> | <specific action> | <actual missing authority or none> |

Documented product behavior: <official sources and relevant version>. Observed session behavior: <facts>. Record any difference without treating a catalogue listing, desktop installation, or source file as proof of active cloud capability.

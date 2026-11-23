"""Exercise the installed public workflow with simulated review records, no model."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from test_workflow import DESIGN, TASKS

CONTRACT = '''# Requirements: repeated records

| ID | Condition and required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | WHEN an owner repeats an accepted request, THE service SHALL return the original stored result. | Repeating the same request creates one result. | Required |
| REQ-002 | IF a different caller requests a private record, THEN THE service SHALL deny the request without returning its data. | Another caller receives no record. | Required |
'''


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


class DeveloperWorkflowIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'app'
        installed = subprocess.run([sys.executable, str(ROOT / 'scripts/bootstrap.py'), '--source', str(ROOT),
                                    '--target', str(self.root), '--mode', 'greenfield', '--apply', '--json'],
                                   capture_output=True, text=True)
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        self.cli = self.root / '.aws-workflow/scripts/workflow.py'
        self.work_id = '0100-record-service'
        self.work = self.root / 'specs' / self.work_id

    def call(self, *args, code=0):
        result = subprocess.run([sys.executable, str(self.cli), '--root', str(self.root), *args],
                                capture_output=True, text=True, cwd=self.root)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else result.stderr

    def create(self, route='quick', existing=False):
        args = ['new', self.work_id, '--title', 'Preserve retry and caller behavior', '--route', route,
                '--idea', 'Preserve the current authentication and record API.', '--activate', '--json']
        if existing:
            args += ['--spec-format', 'existing']
        self.call(*args)
        (self.work / 'requirements.md').write_text(CONTRACT)
        (self.work / 'design.md').write_text(DESIGN)
        (self.work / 'tasks.md').write_text(TASKS)
        (self.root / 'review-notes.md').write_text('Fixture-only simulated review. No real user or model decision is asserted.\n')

    def response(self, operation, findings=None):
        request = self.call(operation, '--json')
        fields = ('schema_version', 'operation', 'request_id', 'input_hashes', 'context_fingerprint')
        response = {key: request[key] for key in fields}
        response.update(reviewer='Fixture reviewer', review_ref='review-notes.md',
                        observed_at=datetime.now(timezone.utc).isoformat(),
                        summary='Fixture-only structured review response; no live model analysis.')
        if operation == 'analyze':
            response['findings'] = findings or []
        else:
            response['properties'] = [
                {'id': f'PROP-{number:03d}', 'requirement_ids': [f'REQ-{number:03d}'],
                 'statement': 'The explicitly linked contract outcome holds for its defined caller and request.',
                 'preconditions': 'Use the established valid caller and request fixtures.',
                 'strategy': 'example', 'verification': 'Execute the linked check and assert the contract result.',
                 'task_ids': [f'T-{number:03d}'], 'check_ids': [f'CHK-{number:03d}'],
                 'source': 'review-notes.md'} for number in (1, 2)]
        path = f'{operation}-response.json'
        (self.root / path).write_text(json.dumps(response))
        self.call(operation, '--record', path, '--json')
        return response

    def review(self, artifact, code=0):
        return self.call('review', '--artifact', artifact, '--outcome', 'accepted',
                         '--decision-ref', 'review-notes.md', '--reviewer', 'Fixture reviewer',
                         '--authority', 'delegated', '--json', code=code)

    def ready_quick(self):
        self.create()
        self.call('advance', '--to', 'tasks', '--json')
        self.response('analyze')
        self.response('properties')
        self.review('tasks')
        return self.call('advance', '--to', 'implementation', '--json')

    def test_setup_before_selection_and_hook_preview_are_read_only(self):
        before = snapshot(self.root)
        setup = self.call('doctor', '--json')
        self.assertTrue(setup['session_ready'])
        self.assertIsNone(setup['active_work'])
        self.assertEqual(next(x for x in setup['checks'] if x['id'] == 'active-work')['status'], 'not-selected')
        hooks = self.call('hooks', '--json')
        command = hooks['configuration']['hooks']['SessionStart'][0]['hooks'][0]['command']
        self.assertIn('/.aws-workflow/scripts/codex_hooks.py', command)
        self.assertEqual(hooks['existing_configuration'], 'absent')
        self.assertEqual(snapshot(self.root), before)

    def test_quick_acceptance_requires_actual_current_analysis_and_property_mapping(self):
        self.create()
        self.call('advance', '--to', 'tasks', '--json')
        self.assertEqual(self.call('context', '--compact', '--json')['next_action']['kind'], 'analyze-requirements')
        self.assertIn('analyze', self.review('tasks', code=2))
        self.response('analyze')
        self.assertEqual(self.call('context', '--compact', '--json')['next_action']['kind'], 'derive-properties')
        self.assertIn('properties', self.review('tasks', code=2))
        self.response('properties')
        self.assertEqual(self.call('context', '--compact', '--json')['next_action']['kind'], 'prepare-phase')
        self.review('tasks')
        report = self.call('advance', '--to', 'implementation', '--json')
        self.assertEqual(report['eligible_tasks'], ['T-001'])
        self.assertEqual(report['specification']['operations']['analyze']['status'], 'current')
        self.assertEqual(report['specification']['operations']['properties']['task_mapping'], 'complete')
        before = snapshot(self.root)
        compact = self.call('context', '--compact', '--json')
        self.assertEqual(compact['work']['phase'], 'implementation')
        self.assertEqual(snapshot(self.root), before)

    def test_design_first_analysis_stays_current_as_tasks_are_created(self):
        self.create('design-first')
        (self.work / 'tasks.md').unlink()
        self.call('advance', '--to', 'design', '--json')
        self.review('design')
        self.call('advance', '--to', 'requirements', '--json')
        self.response('analyze')
        self.review('requirements')
        self.call('advance', '--to', 'tasks', '--json')
        (self.work / 'tasks.md').write_text(TASKS)
        state = self.call('status', '--json')
        self.assertEqual(state['specification']['operations']['analyze']['status'], 'current')
        self.response('properties')
        self.review('tasks')
        self.assertEqual(self.call('advance', '--to', 'implementation', '--json')['eligible_tasks'], ['T-001'])

    def test_open_semantic_blocker_suppresses_acceptance_until_current_resolution(self):
        self.create()
        self.call('advance', '--to', 'tasks', '--json')
        finding = {'id': 'ANA-001', 'requirement_ids': ['REQ-001'], 'severity': 'blocker',
                   'category': 'assumption', 'statement': 'The fixture needs an explicit retry identity rule.',
                   'state': 'open', 'resolution': '', 'source': 'review-notes.md'}
        self.response('analyze', [finding])
        report = self.call('status', '--json')
        self.assertTrue(any(x['code'] == 'specification-blocker' for x in report['issues']))
        self.review('tasks', code=2)
        finding.update(state='resolved', resolution='Fixture resolution: use the existing authenticated caller plus request identifier.')
        self.response('analyze', [finding])
        self.response('properties')
        self.review('tasks')
        self.assertEqual(self.call('advance', '--to', 'implementation', '--json')['eligible_tasks'], ['T-001'])

    def test_actual_rejection_can_be_recorded_without_accepting_a_semantic_blocker(self):
        self.create()
        self.call('advance', '--to', 'tasks', '--json')
        finding = {'id': 'ANA-001', 'requirement_ids': ['REQ-001'], 'severity': 'blocker',
                   'category': 'ambiguity', 'statement': 'The retry identity needs an explicit contract rule.',
                   'state': 'open', 'resolution': '', 'source': 'review-notes.md'}
        self.response('analyze', [finding])
        rejected = self.call('review', '--artifact', 'tasks', '--outcome', 'changes-requested',
                             '--decision-ref', 'review-notes.md', '--reviewer', 'Fixture reviewer',
                             '--authority', 'delegated', '--json')
        self.assertEqual(rejected['reviews']['tasks']['status'], 'changes-requested')
        self.assertTrue(any(x['code'] == 'specification-blocker' for x in rejected['issues']))
        self.assertEqual(rejected['eligible_tasks'], [])
        self.review('tasks', code=2)
        self.call('advance', '--to', 'implementation', '--json', code=2)

    def test_changed_contract_requires_current_sync_preview_and_reanalysis(self):
        self.ready_quick()
        path = self.work / 'requirements.md'
        path.write_text(path.read_text() + '\nClarification: original retries preserve the original record identifier.\n')
        report = self.call('validate', '--json', code=1)
        self.assertEqual(report['eligible_tasks'], [])
        preview = self.call('sync', '--json')
        self.assertEqual(preview['target_phase'], 'tasks')
        before = snapshot(self.root)
        self.call('sync', '--apply', '--json', code=2)
        self.assertEqual(snapshot(self.root), before)
        path.write_text(path.read_text() + '\nAn additional current source clarification.\n')
        self.call('sync', '--apply', '--expected-fingerprint', preview['fingerprint'], '--reason', 'Fixture contract correction', '--json', code=2)
        preview = self.call('sync', '--json')
        applied = self.call('sync', '--apply', '--expected-fingerprint', preview['fingerprint'], '--reason', 'Fixture contract correction', '--json')
        self.assertEqual(applied['report']['phase'], 'tasks')
        self.response('analyze')
        self.response('properties')
        self.review('tasks')
        self.assertEqual(self.call('advance', '--to', 'implementation', '--json')['eligible_tasks'], ['T-001'])

    def test_existing_contract_option_preserves_legacy_review_behavior(self):
        self.create(existing=True)
        self.call('advance', '--to', 'tasks', '--json')
        self.review('tasks')
        report = self.call('advance', '--to', 'implementation', '--json')
        self.assertEqual(report['eligible_tasks'], ['T-001'])
        self.assertNotIn('specification', report)

    def test_executable_template_is_a_draft_and_never_runs_a_model(self):
        self.ready_quick()
        before = snapshot(self.root)
        draft = self.call('execution-template', '--json')
        self.assertEqual(draft['schema_version'], 1)
        self.assertIn('T-001', draft['tasks'])
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse((self.root / '.workflow-state').exists())


if __name__ == '__main__':
    unittest.main()

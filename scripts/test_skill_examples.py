"""Run the documented Python response handler with single and reordered batch replies."""
import contextlib
import io
import json
import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError


class HTTPExampleTest(unittest.TestCase):
    def test_preserves_response_ids_for_single_and_batch_results(self):
        skill = Path(__file__).resolve().parents[1] / 'skills/evm/SKILL.md'
        section = skill.read_text().split('### Python HTTP request', 1)[1]
        example = re.search(r'```python\n([\s\S]*?)```', section)[1]
        cases = [
            ({'jsonrpc': '2.0', 'id': 1, 'result': '0x123'}, '1 0x123\n'),
            ([{'jsonrpc': '2.0', 'id': 2, 'result': '0x456'},
              {'jsonrpc': '2.0', 'id': 1, 'result': '0x123'}],
             '2 0x456\n1 0x123\n'),
        ]
        for response, expected in cases:
            with self.subTest(response=response):
                output = io.StringIO()
                with patch.dict(os.environ, {'DWELLIR_RPC_URL': 'https://example.invalid/dummy'}), \
                     patch('urllib.request.urlopen', return_value=io.BytesIO(json.dumps(response).encode())), \
                     contextlib.redirect_stdout(output):
                    exec(example, {})
                self.assertEqual(output.getvalue(), expected)


    def test_connection_error_omits_authenticated_url(self):
        skill = Path(__file__).resolve().parents[1] / 'skills/evm/SKILL.md'
        section = skill.read_text().split('### Python HTTP request', 1)[1]
        example = re.search(r'```python\n([\s\S]*?)```', section)[1]
        with patch.dict(os.environ, {'DWELLIR_RPC_URL': 'https://example.invalid/dummy'}), \
             patch('urllib.request.urlopen', side_effect=URLError('https://example.invalid/private-test-key')):
            with self.assertRaises(SystemExit) as error:
                exec(example, {})
        self.assertNotIn('private-test-key', str(error.exception))
        self.assertNotEqual(error.exception.code, 0)

if __name__ == '__main__':
    unittest.main()

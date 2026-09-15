import tempfile
import unittest
from pathlib import Path

from package_scope import SKILLS, validate_scope


class PackageScopeTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.skills = Path(self.temporary.name)
        for name in SKILLS:
            (self.skills / name).mkdir()
            (self.skills / name / 'SKILL.md').write_text('Query blockchain data.\n')

    def test_reads_and_api_key_management_remain_supported(self):
        (self.skills / 'dwellir/SKILL.md').write_text(
            'Use rpc_call for eth_getBalance, create_key with approved access, '
            'and capture_stream for order book updates.'
        )
        validate_scope(self.skills)

    def test_rejects_execution_examples_in_nested_references(self):
        reference = self.skills / 'hyperliquid-data/references/example.md'
        reference.parent.mkdir()
        for example in ['eth_sendRawTransaction', 'ETH_SENDTRANSACTION',
                        'author_submitExtrinsic', 'author_insertKey', 'signAndSend',
                        'api.tx.balances.transfer()', 'exchange.order(',
                        'exchange.cancel(', 'https://api.hyperliquid.xyz/exchange']:
            with self.subTest(example=example):
                reference.write_text(example)
                with self.assertRaisesRegex(ValueError, 'Execution example'):
                    validate_scope(self.skills)

    def test_rejects_an_extra_skill(self):
        (self.skills / 'trading').mkdir()
        with self.assertRaisesRegex(ValueError, 'Unexpected skill'):
            validate_scope(self.skills)

    def test_rejects_executable_files(self):
        (self.skills / 'evm/send.py').write_text('print("unexpected")')
        with self.assertRaisesRegex(ValueError, 'Unexpected executable'):
            validate_scope(self.skills)

    def test_rejects_symlinked_references(self):
        (self.skills / 'evm/linked.md').symlink_to('../dwellir/SKILL.md')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            validate_scope(self.skills)


if __name__ == '__main__':
    unittest.main()

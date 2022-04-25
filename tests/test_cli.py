import unittest
from pathlib import Path

from click.testing import CliRunner
from gold_ecosystems_linkml.cli import generate_linkml


class TestCommandLine(unittest.TestCase):

    def test_generate_linkml(self):
        spreadsheet_path = (Path(__file__).parent / '../resources/gold_paths.xlsx').absolute()
        if not spreadsheet_path.exists():
            self.skipTest('Spreadsheet resource file does not exist. Try running `make resources/gold_paths.xlsx` first.')

        runner = CliRunner()
        result = runner.invoke(generate_linkml, [str(spreadsheet_path)])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('\ntitle: GOLD Ecosystem Classification\n', result.output)

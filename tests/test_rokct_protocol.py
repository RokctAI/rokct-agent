import unittest
from pathlib import Path
import tempfile
import shutil
import os
from agent.rokct_protocol import RokctProtocol

class TestRokctProtocol(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.rokct_dir = self.workspace / ".rokct"
        self.rokct_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_no_rokct(self):
        shutil.rmtree(self.rokct_dir)
        protocol = RokctProtocol(self.test_dir)
        self.assertFalse(protocol.load())

    def test_load_rokct_files(self):
        (self.rokct_dir / "README.md").write_text("General protocol")
        (self.rokct_dir / "project_map.md").write_text("Map info")
        (self.rokct_dir / "other.txt").write_text("Other content")
        
        protocol = RokctProtocol(self.test_dir)
        self.assertTrue(protocol.load())
        self.assertIn("README.md", protocol.rules)
        self.assertIn("project_map.md", protocol.rules)
        self.assertIn("other.txt", protocol.rules)

    def test_format_for_prompt(self):
        (self.rokct_dir / "README.md").write_text("General protocol")
        (self.rokct_dir / "project_map.md").write_text("Map info")
        
        protocol = RokctProtocol(self.test_dir)
        protocol.load()
        prompt = protocol.format_for_prompt()
        
        self.assertIn("## GLOBAL WORKSPACE PROTOCOL (ROKCT)", prompt)
        self.assertIn("### README.md", prompt)
        self.assertIn("General protocol", prompt)
        self.assertIn("### project_map.md", prompt)
        self.assertIn("Map info", prompt)

if __name__ == "__main__":
    unittest.main()

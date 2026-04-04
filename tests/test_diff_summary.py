import unittest
from agent.display import build_diff_summary

class TestDiffSummary(unittest.TestCase):
    def test_single_file_diff(self):
        diff = """--- a/test.txt
+++ b/test.txt
@@ -1,3 +1,4 @@
 line 1
-line 2
+line 2 changed
+line 3 added
 line 4"""
        summary = build_diff_summary(diff)
        self.assertEqual(summary, "M | test.txt +2 | -1")

    def test_multi_file_diff(self):
        diff = """--- a/file1.py
+++ b/file1.py
@@ -1 +1,2 @@
-print(1)
+print(1)
+print(2)
--- a/docs/readme.md
+++ b/docs/readme.md
@@ -5 +5 @@
-old
+new"""
        summary = build_diff_summary(diff)
        # file1.py: -1, +2
        # note: build_diff_summary now strips parent dirs for compact messaging
        self.assertEqual(summary, "M | file1.py +2 | -1\nM | readme.md +1 | -1")

    def test_no_diff(self):
        self.assertEqual(build_diff_summary(""), "")

if __name__ == "__main__":
    unittest.main()

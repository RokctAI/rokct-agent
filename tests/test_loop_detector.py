import unittest
import json
from agent.loop_detector import LoopDetector

class TestLoopDetector(unittest.TestCase):
    def setUp(self):
        self.detector = LoopDetector()

    def test_direct_repetition(self):
        tool = "read_file"
        args = {"path": "test.txt"}
        result = "file content"
        
        # Call 1
        h = self.detector.record_call(tool, args)
        self.detector.record_result(h, result)
        
        # Call 2
        level, msg = self.detector.detect(tool, h)
        self.assertIsNone(level)
        self.detector.record_call(tool, args)
        self.detector.record_result(h, result)
        
        # Call 3
        level, msg = self.detector.detect(tool, h)
        self.assertIsNone(level)
        self.detector.record_call(tool, args)
        self.detector.record_result(h, result)

        # Call 4
        level, msg = self.detector.detect(tool, h)
        self.assertEqual(level, "warning")
        self.detector.record_call(tool, args)
        self.detector.record_result(h, result)
        
        # Call 5
        level, msg = self.detector.detect(tool, h)
        self.assertEqual(level, "warning")
        self.detector.record_call(tool, args)
        self.detector.record_result(h, result)
        
        # Call 6
        level, msg = self.detector.detect(tool, h)
        self.assertEqual(level, "critical")

    def test_read_only_streak_exploration(self):
        tool = "read_file"
        
        # Use unique files to avoid direct repetition loop
        for i in range(24):
            args = {"path": f"file{i}.txt"}
            h = self.detector.record_call(tool, args)
            self.detector.record_result(h, f"content{i}")
            
        # streak = 24. unique = 24. ratio = 1.0.
        # READ_ONLY_EXPLORATION_WARNING = 24.
        level, msg = self.detector.detect(tool, h)
        self.assertEqual(level, "warning")
        self.assertIn("summarize what you learned", msg)

    def test_error_streak(self):
        tool = "ls"
        args = {"path": "/invalid"}
        result = '{"error": "not found"}'
        
        for i in range(3):
            h = self.detector.record_call(tool, args)
            self.detector.record_result(h, result)
            
        level, msg = self.detector.detect(tool, self.detector.hash_args(tool, args))
        self.assertEqual(level, "critical")
        self.assertIn("CRITICAL ERROR THRESHOLD REACHED", msg)

if __name__ == "__main__":
    unittest.main()

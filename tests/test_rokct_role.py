import unittest
from unittest.mock import patch, mock_open
import os
from pathlib import Path
from hermes_constants import get_rokct_app_role

class TestRokctRoleDetection(unittest.TestCase):

    @patch("os.getenv")
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"app_role": "control"}')
    def test_get_rokct_app_role_control(self, mock_file, mock_exists, mock_env):
        # Setup mocks
        mock_env.side_effect = lambda k, d=None: "frappe-bench" if k == "FRAPPE_BENCH" else ("site1.local" if k == "SITE" else d)
        mock_exists.return_value = True
        
        role = get_rokct_app_role()
        self.assertEqual(role, "control")

    @patch("os.getenv")
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"app_role": "tenant"}')
    def test_get_rokct_app_role_tenant(self, mock_file, mock_exists, mock_env):
        mock_env.side_effect = lambda k, d=None: "frappe-bench" if k == "FRAPPE_BENCH" else ("site1.local" if k == "SITE" else d)
        mock_exists.return_value = True
        
        role = get_rokct_app_role()
        self.assertEqual(role, "tenant")

    @patch("os.getenv")
    @patch("pathlib.Path.exists")
    def test_get_rokct_app_role_unknown(self, mock_exists, mock_env):
        mock_env.return_value = None
        mock_exists.return_value = False
        
        role = get_rokct_app_role()
        self.assertEqual(role, "unknown")

if __name__ == "__main__":
    unittest.main()

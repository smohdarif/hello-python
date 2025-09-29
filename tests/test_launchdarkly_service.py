"""
Unit tests for LaunchDarkly service.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.services.launchdarkly_service import LaunchDarklyService


class TestLaunchDarklyService(unittest.TestCase):
    """Test cases for LaunchDarkly service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_sdk_key = "test-sdk-key"
    
    @patch('src.services.launchdarkly_service.ldclient')
    def test_initialization_success(self, mock_ldclient):
        """Test successful service initialization."""
        # Mock successful initialization
        mock_client = MagicMock()
        mock_client.is_initialized.return_value = True
        mock_ldclient.get.return_value = mock_client
        
        # Create service
        service = LaunchDarklyService(self.test_sdk_key)
        
        # Assertions
        self.assertTrue(service.is_ready())
        mock_ldclient.set_config.assert_called_once()
        mock_ldclient.get.assert_called()
    
    @patch('src.services.launchdarkly_service.ldclient')
    def test_initialization_failure(self, mock_ldclient):
        """Test service initialization failure."""
        # Mock failed initialization
        mock_client = MagicMock()
        mock_client.is_initialized.return_value = False
        mock_ldclient.get.return_value = mock_client
        
        # Test that RuntimeError is raised
        with self.assertRaises(RuntimeError):
            LaunchDarklyService(self.test_sdk_key)


if __name__ == '__main__':
    unittest.main()

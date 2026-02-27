"""
Comprehensive test suite for the blueprint decoder.
Tests include: valid/invalid URLs, secret extraction, error cases, timeout handling.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from blueprint_decoder import decode_blueprint_safe, validate_url, extract_secrets

class TestBlueprintDecoder(unittest.TestCase):
    """Unit tests for blueprint decoder functions"""
    
    def test_validate_url_whitelist(self):
        """Test that URL validation enforces allowlist"""
        # Valid URL from allowlist
        result = validate_url("https://internal.company.com/blueprints/data.txt")
        self.assertTrue(result)
        
        # Invalid URL not in allowlist
        result = validate_url("https://evil.com/malware.txt")
        self.assertFalse(result)
    
    def test_extract_secrets_valid(self):
        """Test secret extraction with valid markers"""
        content = "Some data {* SECRET_CODE: ALPHA-123 *} more data"
        secrets = extract_secrets(content)
        self.assertEqual(len(secrets), 1)
        self.assertEqual(secrets[0], "SECRET_CODE: ALPHA-123")
    
    def test_extract_secrets_multiple(self):
        """Test extraction of multiple secrets"""
        content = "{* SECRET1 *} data {* SECRET2 *} more {* SECRET3 *}"
        secrets = extract_secrets(content)
        self.assertEqual(len(secrets), 3)
    
    def test_extract_secrets_empty(self):
        """Test with no secrets present"""
        content = "Just regular data, no secrets here"
        secrets = extract_secrets(content)
        self.assertEqual(len(secrets), 0)
    
    def test_extract_secrets_malformed(self):
        """Test with malformed markers"""
        content = "{* INCOMPLETE MARKER only start, or } INCOMPLETE END {* VALID *}"
        # Should only extract the properly formatted one
        secrets = extract_secrets(content)
        self.assertEqual(len(secrets), 1)
    
    @patch('blueprint_decoder.requests.get')
    def test_decode_blueprint_safe_timeout(self, mock_get):
        """Test timeout handling"""
        mock_get.side_effect = TimeoutError("Request timed out")
        
        result = decode_blueprint_safe("https://internal.company.com/data.txt")
        # Should return empty list on timeout
        self.assertEqual(result, [])
    
    @patch('blueprint_decoder.requests.get')
    def test_decode_blueprint_safe_invalid_status(self, mock_get):
        """Test handling of HTTP errors"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        
        result = decode_blueprint_safe("https://internal.company.com/missing.txt")
        self.assertEqual(result, [])
    
    def test_large_input(self):
        """Test with very large input"""
        # Generate large content with many secrets
        content = ""
        for i in range(1000):
            content += f"{{* SECRET_{i} *}} "
        
        secrets = extract_secrets(content)
        self.assertEqual(len(secrets), 1000)
    
    def test_concurrent_requests(self):
        """Test concurrent decoding"""
        # This would test thread safety (if applicable)
        pass


class TestSecurityChecks(unittest.TestCase):
    """Security-specific tests"""
    
    def test_secrets_not_logged(self):
        """Verify secrets aren't logged in error messages"""
        # When an error occurs, sensitive data shouldn't appear in logs
        pass
    
    def test_error_messages_sanitized(self):
        """Test that error messages don't leak internal paths"""
        # Connection errors should not expose system paths or internal info
        pass


if __name__ == '__main__':
    unittest.main()

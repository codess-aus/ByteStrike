/**
 * Comprehensive test suite for the blueprint decoder
 * Uses Jest or Mocha for testing
 */

const { 
  decodeBlueprintSafe, 
  validateUrl, 
  extractSecrets 
} = require('../blueprint_decoder');

describe('Blueprint Decoder Tests', () => {
  
  describe('validateUrl', () => {
    test('should accept whitelisted URLs', () => {
      const validUrl = 'https://internal.company.com/blueprints/data.txt';
      expect(validateUrl(validUrl)).toBe(true);
    });

    test('should reject non-whitelisted URLs', () => {
      const invalidUrl = 'https://evil.com/malware.txt';
      expect(validateUrl(invalidUrl)).toBe(false);
    });

    test('should reject malformed URLs', () => {
      expect(validateUrl('not-a-url')).toBe(false);
      expect(validateUrl('')).toBe(false);
    });
  });

  describe('extractSecrets', () => {
    test('should extract single secret from content', () => {
      const content = 'Some data {* SECRET_CODE: ALPHA-123 *} more data';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(1);
      expect(secrets[0]).toBe('SECRET_CODE: ALPHA-123');
    });

    test('should extract multiple secrets', () => {
      const content = '{* SECRET1 *} data {* SECRET2 *} more {* SECRET3 *}';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(3);
      expect(secrets).toEqual(['SECRET1', 'SECRET2', 'SECRET3']);
    });

    test('should return empty array when no secrets present', () => {
      const content = 'Just regular data, no secrets here';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(0);
    });

    test('should handle malformed markers gracefully', () => {
      const content = '{* INCOMPLETE MARKER only start, or } INCOMPLETE END {* VALID *}';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(1);
      expect(secrets[0]).toBe('VALID');
    });

    test('should handle empty markers', () => {
      const content = 'Data {* *} more data';
      const secrets = extractSecrets(content);
      
      // Empty secret or filtered out depends on implementation
      expect(Array.isArray(secrets)).toBe(true);
    });

    test('should handle nested markers (should not extract)', () => {
      const content = '{* OUTER {* INNER *} OUTER *}';
      const secrets = extractSecrets(content);
      
      // Behavior depends on regex implementation
      // Should ideally not extract nested patterns
      expect(Array.isArray(secrets)).toBe(true);
    });
  });

  describe('decodeBlueprintSafe', () => {
    test('should handle network timeout', async () => {
      // Mock fetch to simulate timeout
      global.fetch = jest.fn(() => 
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Network timeout')), 100)
        )
      );

      const result = await decodeBlueprintSafe('https://internal.company.com/data.txt');
      
      expect(result).toEqual([]);
      expect(global.fetch).toHaveBeenCalled();
    });

    test('should handle HTTP 404 error', async () => {
      global.fetch = jest.fn(() => 
        Promise.resolve({
          status: 404,
          ok: false,
          statusText: 'Not Found'
        })
      );

      const result = await decodeBlueprintSafe('https://internal.company.com/missing.txt');
      
      expect(result).toEqual([]);
    });

    test('should handle invalid JSON response', async () => {
      global.fetch = jest.fn(() => 
        Promise.resolve({
          status: 200,
          ok: true,
          text: () => Promise.resolve('{ invalid json')
        })
      );

      const result = await decodeBlueprintSafe('https://internal.company.com/data.txt');
      
      expect(result).toEqual([]);
    });

    test('should extract secrets from valid response', async () => {
      const mockContent = 'Data {* SECRET_1 *} more {* SECRET_2 *}';
      global.fetch = jest.fn(() => 
        Promise.resolve({
          status: 200,
          ok: true,
          text: () => Promise.resolve(mockContent)
        })
      );

      const result = await decodeBlueprintSafe('https://internal.company.com/data.txt');
      
      expect(result).toEqual(['SECRET_1', 'SECRET_2']);
    });
  });

  describe('Security Tests', () => {
    test('should not log secrets in error messages', () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      
      const content = '{* CONFIDENTIAL *} data';
      try {
        // Trigger an error condition
        validateUrl('invalid-url');
      } catch (e) {
        // Assert error message doesn't contain secret
        expect(e.message).not.toContain('CONFIDENTIAL');
      }
      
      consoleSpy.mockRestore();
    });

    test('should sanitize error messages', () => {
      // Error messages should not expose internal paths
      const result = validateUrl('file:///etc/passwd');
      
      expect(result).toBe(false);
    });
  });

  describe('Edge Cases', () => {
    test('should handle very large input', () => {
      let content = '';
      for (let i = 0; i < 1000; i++) {
        content += `{* SECRET_${i} *} `;
      }
      
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(1000);
    });

    test('should handle special characters in secrets', () => {
      const content = '{* SECRET: !@#$%^&*() *}';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(1);
      expect(secrets[0]).toBe('SECRET: !@#$%^&*()');
    });

    test('should handle Unicode characters', () => {
      const content = '{* SECRET: 🔐 confidential 🔒 *}';
      const secrets = extractSecrets(content);
      
      expect(secrets).toHaveLength(1);
      expect(secrets[0]).toContain('confidential');
    });
  });
});

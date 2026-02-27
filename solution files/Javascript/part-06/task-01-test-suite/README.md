# Task 1: Build a Test Suite

## Overview
This task involves creating comprehensive unit and integration tests for the blueprint decoder.

## Files in this directory

### `blueprint_decoder.test.js`
Complete Jest test suite including:
- URL validation tests
- Secret extraction tests
- Error handling tests
- Security tests
- Edge case tests

## What you should do

Create tests covering:

1. **Unit Tests**
   - Valid/invalid URL validation
   - Secret extraction with various markers
   - Error cases (timeout, invalid status, network errors)
   - Edge cases (large input, special characters, Unicode)

2. **Security Tests**
   - Verify secrets aren't logged
   - Error messages don't expose internal paths
   - Whitelist validation enforced

3. **Integration Tests**
   - Mock fetch/HTTP calls
   - Test with real decoder pipeline
   - Error response handling

## Test Framework
- **Jest** recommended (has built-in mocking and coverage)
- Alternatively: Mocha + Chai, Vitest

## Setup

```bash
npm install --save-dev jest
npm install --save-dev jest-mock-extended  # for mocking
```

## Package.json scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Coverage Requirements
- Minimum 80% code coverage
- Critical paths (security, error handling) must be 100%
- Run `jest --coverage` in CI/CD

## Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm run test:watch

# Run specific test file
npm test -- blueprint_decoder.test.js
```

## Next Steps
- Set up Jest in your project
- Write tests for each decoder function  
- Achieve 80%+ coverage
- Integrate with CI/CD pipeline
- Run tests on every commit

# Task 1: Build a Test Suite

## Overview
This task involves creating comprehensive unit and integration tests for the blueprint decoder.

## Files in this directory

### `BlueprintDecoderTests.cs`
Complete test suite including:
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
   - Error cases (timeout, invalid status, etc.)
   - Edge cases (large input, malformed data)

2. **Security Tests**
   - Verify secrets aren't logged
   - Error messages don't expose internal info
   - Whitelist validation enforced

3. **Integration Tests**
   - Mock network calls
   - Test with real decoder pipeline
   - Concurrent request handling

## Test Framework
- C#: Use xUnit or NUnit
- JavaScript: Use Jest
- Python: Use pytest

## Coverage Requirements
- Minimum 80% code coverage
- Critical paths (security, error handling) must be 100%
- Run coverage reports in CI/CD

## Testing Commands

### C#
```bash
dotnet test --verbosity normal
dotnet test --collect:"XPlat Code Coverage"
```

### Python
```bash
pytest --cov=blueprint_decoder --cov-report=html
```

### JavaScript
```bash
npm test -- --coverage
jest --coverage
```

## Next Steps
- Set up test infrastructure
- Write tests for each decoder function
- Achieve 80%+ coverage
- Integrate with CI/CD pipeline
- Run tests on every commit

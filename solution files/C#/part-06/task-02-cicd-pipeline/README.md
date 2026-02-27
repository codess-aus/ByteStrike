# Task 2: CI/CD Pipeline Setup

## Overview
This task involves setting up a complete CI/CD pipeline for the blueprint decoder.

## Files in this directory

### `build.yml`
GitHub Actions workflow that:
- Runs on every push to main/develop and pull requests
- Runs tests with multiple .NET versions
- Builds Docker images
- Pushes to container registry
- Runs security scans

## What you should do

For your language:

### Python
- Use GitHub Actions (see `solution files/Python/part-06/task-02-cicd-pipeline/.github-workflows-build.yml`)
- Or GitLab CI (see `solution files/Python/part-06/task-02-cicd-pipeline/.gitlab-ci.yml`)

### C# / JavaScript
- Configure `.github/workflows/build.yml` in your repository
- Include: lint, test, security scan, build, Docker build/push
- Add coverage requirements (minimum 80%)
- Configure docker build and push to registry

## Key Components

1. **Build**: Compile/package your code
2. **Test**: Run all unit and integration tests
3. **Security**: Scan dependencies, check for vulnerabilities
4. **Docker**: Build and push container images
5. **Deploy**: Automatically deploy passing builds to staging

## Environment Variables
Set these in your GitHub Actions secrets:
- `REGISTRY_USERNAME`: Docker registry username
- `REGISTRY_PASSWORD`: Docker registry password
- `SNYK_TOKEN`: Snyk security scanning token (optional)
- `NPM_TOKEN`: npm publish token (JavaScript only)

## Next Steps
- Copy the appropriate workflow file to `.github/workflows/`
- Update registry URLs for your organization
- Add secrets to GitHub repository settings
- Create a Dockerfile for your application
- Test the pipeline with a PR

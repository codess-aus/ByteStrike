# Task 2: CI/CD Pipeline Setup

## Overview
Set up continuous integration and deployment for the Node.js blueprint decoder.

## Files in this directory

### `build.yml`
GitHub Actions workflow that:
- Runs on every push and pull request
- Tests with multiple Node.js versions
- Runs linting and formatting checks
- Publishes to npm (on tag)
- Builds and pushes Docker image

## Setup Steps

1. **Copy workflow file**
   ```bash
   mkdir -p .github/workflows
   cp build.yml .github/workflows/build.yml
   ```

2. **Add npm scripts to package.json**
   ```json
   {
     "scripts": {
       "lint": "eslint .",
       "format:check": "prettier --check .",
       "format": "prettier --write .",
       "test": "jest",
       "build": "npm run format && npm run lint && npm run test"
     }
   }
   ```

3. **Set up GitHub secrets**
   - `REGISTRY_USERNAME`: Docker registry user
   - `REGISTRY_PASSWORD`: Docker registry password
   - `NPM_TOKEN`: npm publish token

4. **Create `.eslintrc`**
   ```json
   {
     "extends": "eslint:recommended",
     "parserOptions": { "ecmaVersion": 2021 },
     "env": { "node": true, "jest": true }
   }
   ```

5. **Create `.prettierrc`**
   ```json
   { "semi": true, "singleQuote": true, "printWidth": 100 }
   ```

## Pipeline Stages

1. **Test** (on all PRs and pushes)
   - Install dependencies
   - Lint code
   - Check formatting
   - Run tests with coverage
   - Upload coverage to Codecov

2. **Build** (on main branch)
   - Build Docker image
   - Push to registry
   - Tag as `latest`

3. **Publish** (on release tags)
   - Publish to npm registry
   - Create GitHub release

## Environment Variables

```bash
NODE_VERSION=18.x           # Node.js version
REGISTRY=registry.company.com
NPM_REGISTRY=https://registry.npmjs.org
```

## Dependencies

```bash
npm install --save-dev eslint prettier jest @testing-library/jest-dom
```

## Next Steps
1. Copy workflow to `.github/workflows/`
2. Add npm scripts
3. Install linter/formatter
4. Configure GitHub secrets
5. Push and test with a PR
6. Verify Docker builds

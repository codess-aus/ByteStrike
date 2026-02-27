# Task 6: Deployment

## Overview
Implement production deployment pipeline.

## What to create

### 1. Docker Configuration (Dockerfile)

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .
USER nodejs
EXPOSE 8080 9090
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD node -e "require('http').get('http://localhost:8080/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"
CMD ["node", "index.js"]
```

### 2. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blueprint-decoder
spec:
  replicas: 3
  selector:
    matchLabels:
      app: blueprint-decoder
  template:
    metadata:
      labels:
        app: blueprint-decoder
    spec:
      containers:
      - name: blueprint-decoder
        image: registry.example.com/blueprint-decoder:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: NODE_ENV
          value: production
        - name: PORT
          value: "8080"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          readOnlyRootFilesystem: true
---
apiVersion: v1
kind: Service
metadata:
  name: blueprint-decoder
spec:
  selector:
    app: blueprint-decoder
  ports:
  - port: 80
    targetPort: 8080
    name: http
  type: ClusterIP
```

### 3. Deployment Steps

1. **Build**: `npm install && npm run build && npm test`
2. **Docker**: Build and push image to registry
3. **Kubernetes**: Apply manifests
4. **Health Check**: Wait for pods to be ready
5. **Smoke Tests**: Run basic health checks
6. **Monitor**: Check metrics for 1 hour

### 4. Rollback Capability

```bash
# View deployment history
kubectl rollout history deployment/blueprint-decoder

# Rollback if needed
kubectl rollout undo deployment/blueprint-decoder

# Monitor rollback
kubectl rollout status deployment/blueprint-decoder
```

## CI/CD Integration

The deployment is triggered automatically by:
- GitHub Actions on tag: `git tag v1.0.0 && git push --tags`
- GitLab CI on merge to main
- Jenkins pipeline on approval

## Staging → Production Flow

1. **Tag release**: `git tag v1.0.0`
2. **CI/CD builds**: Automatically triggered
3. **Deploy to staging**: Automatic
4. **Manual approval**: Review metrics
5. **Deploy to production**: Automatic
6. **Monitor**: 24 hours observation

## Success Criteria

- ✓ All tests pass
- ✓ Coverage >= 80%
- ✓ Zero security warnings
- ✓ Health checks pass
- ✓ Metrics flowing
- ✓ Zero errors in first hour
- ✓ Performance acceptable

## Next Steps
1. Create Dockerfile
2. Create Kubernetes manifests
3. Configure registry access
4. Test in staging environment
5. Deploy to production
6. Monitor for 24 hours
7. Document process

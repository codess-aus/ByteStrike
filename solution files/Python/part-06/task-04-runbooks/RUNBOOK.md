# Blueprint Decoder - Production Runbook

## Service Overview

The Blueprint Decoder is a critical service that extracts encrypted blueprints from remote sources and decodes secret information. It's designed to handle high-volume requests with strong security and privacy controls.

- **Service**: blueprint-decoder
- **Language**: Python 3.11 / C# / Node.js
- **Deployment**: Docker containers on Kubernetes
- **On-call**: See escalation path below

## Quick Status Check

### Check service health
```bash
# Check if service is running
kubectl get pods -l app=blueprint-decoder

# Check recent logs
kubectl logs -l app=blueprint-decoder --tail=50 --follow

# Check metrics
curl http://prometheus:9090/api/v1/query?query=blueprint_decoder_up
```

### Check key metrics
- **Success Rate**: Should be > 95%
- **P95 Latency**: Should be < 10 seconds
- **Error Count**: Should be low and stable

## Common Failure Scenarios

### 1. Low Success rate or decode failures

**Symptoms**: 
- Success rate drops below 95%
- Customers report "decode failed" errors
- `blueprint_decoder_failures_total` counter increasing

**Investigation**:
```bash
# Check error logs
kubectl logs -l app=blueprint-decoder | grep ERROR | tail -20

# Check if remote blueprint server is reachable
curl -v https://internal.company.com/blueprints/data.txt \
  -H "Authorization: Bearer $API_KEY"

# Check network connectivity
kubectl exec -it <pod-name> -- ping internal.company.com
```

**Resolution**:
- If remote server is down: Contact the Blueprint Server team (Slack: #blueprint-server-ops)
- If network issue: Contact infrastructure team
- If timeout errors: Consider increasing timeout configuration or scaling decoder pods

### 2. Timeout errors spiking

**Symptoms**:
- Decode requests timing out
- Log shows "Request timed out after 30s"
- Alert: `TimeoutErrorsSpike`

**Investigation**:
```bash
# Check decoder pod resource usage
kubectl top pods -l app=blueprint-decoder

# Check network latency to remote server
kubectl exec -it <pod-name> -- ping -c 10 internal.company.com

# Check decoder logs for timeout errors
kubectl logs -l app=blueprint-decoder | grep -i timeout | wc -l
```

**Resolution**:
- If CPU/memory high: Scale up decoder pods
  ```bash
  kubectl scale deployment blueprint-decoder --replicas=5
  ```
- If network latency high: Contact infrastructure team
- If consistently timing out: Increase timeout configuration (requires new deployment)

### 3. Memory/CPU exhaustion

**Symptoms**:
- Pods being restarted unexpectedly
- Alert: `HighMemoryUsage` or `HighCPUUsage`
- `kubectl get events` shows `OOMKilled`

**Investigation**:
```bash
# Check resource usage
kubectl top pods -l app=blueprint-decoder
kubectl describe pods -l app=blueprint-decoder | grep -A 5 "Requests\|Limits"

# Check for memory leaks in logs
kubectl logs -l app=blueprint-decoder | grep -i "memory\|leak"
```

**Resolution**:
- Immediate: Restart the pods
  ```bash
  kubectl rollout restart deployment/blueprint-decoder
  ```
- If persistent: Increase resource requests/limits
  ```bash
  kubectl set resources deployment blueprint-decoder --requests=cpu=500m,memory=512Mi --limits=cpu=1000m,memory=1Gi
  ```
- File ticket: Infrastructure needs to review memory usage

### 4. URL validation blocking legitimate requests

**Symptoms**:
- Users report "URL not whitelisted" errors
- Legitimate blueprint sources rejected
- Alert: `HighURLValidationFailures`

**Investigation**:
```bash
# Check validation logs
kubectl logs -l app=blueprint-decoder | grep "URL validation failed" | tail -10

# Identify blocked URLs
kubectl logs -l app=blueprint-decoder | grep "rejected.*url" | tail -20
```

**Resolution**:
- If URL is legitimate: Update whitelist
  ```bash
  kubectl set env deployment/blueprint-decoder \
    WHITELIST_URLS="internal.company.com,new.blueprint.source.com"
  ```
- Verify with product team before updating
- Deploy change and monitor

### 5. Secret leakage in logs

**Symptoms**:
- Alert: `SecretsFoundInLogs`
- Security team notification
- Customer privacy concern

**Investigation**:
```bash
# Search for secrets in recent logs
kubectl logs -l app=blueprint-decoder --since=10m | grep -i secret | head -20

# Check for plaintext secrets in code
git log --all --source --remotes -S "SECRET_" -- . | head -20
```

**Resolution**:
- Immediate: Revoke compromised secrets
- Review logging configuration: Ensure secrets are masked
- Update code review process: Check for secret logging
- File incident report

## Rollback Procedure

If a recent deployment caused issues:

```bash
# Check current deployment status
kubectl rollout history deployment/blueprint-decoder

# Rollback to previous version
kubectl rollout undo deployment/blueprint-decoder

# Monitor rollback
kubectl rollout status deployment/blueprint-decoder

# If needed, rollback multiple versions
kubectl rollout undo deployment/blueprint-decoder --to-revision=3
```

## Escalation Path

1. **Initial Response (Any on-call engineer)**
   - Acknowledge alert
   - Check service status and logs
   - Gather information

2. **Level 2 Escalation (30 minutes if unresolved)**
   - Page the Backend Team Lead
   - Slack: @blueprint-decoder-team in #alerts
   - Start incident in Incident.io

3. **Level 3 Escalation (60 minutes if unresolved)**
   - Page the Engineering Manager
   - Contact Infrastructure if network/Kubernetes issue
   - Contact security team if data issue

4. **Post-Incident**
   - Create incident post-mortem ticket
   - Review logs: What led to failure?
   - Update runbook if new scenario discovered
   - Schedule follow-up incident review

## Contacts

- **Backend Team**: Slack #blueprint-decoder-team
- **Infrastructure**: Slack #infra-on-call
- **Security**: Slack #security-incidents
- **Product@: blueprint-product@company.com

## Useful Links

- **Logs**: https://logs.company.com/?query=service:blueprint-decoder
- **Metrics**: https://grafana.company.com/d/blueprint-decoder
- **Service Status**: https://status.company.com
- **On-call Schedule**: https://pagerduty.company.com/schedules/blueprint-decoder
- **Deployment History**: https://github.com/company/blueprint-decoder/deployments

## Change Log

- **v1.1.0**: Increased default timeout to 30s
- **v1.0.5**: Fixed secret masking in logs
- **v1.0.0**: Initial production release

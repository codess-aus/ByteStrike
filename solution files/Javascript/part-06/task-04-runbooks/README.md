# Task 4: Runbooks & Incident Response

## Overview
Create operational guides for on-call teams.

## What to create

Create `RUNBOOK.md` with sections:

### 1. Service Overview
- What the service does
- Why it's critical
- On-call contact

### 2. Quick Status Checks
```bash
# Health check
curl https://api.example.com/health

# Recent logs
kubectl logs -l app=blueprint-decoder --tail=50

# Metrics
curl http://prometheus:9090/api/v1/query?query=blueprint_decoder_up
```

### 3. Common Failure Scenarios

**Low Success Rate**
- Symptoms: Success rate < 95%
- Investigation: Check error logs, remote server status
- Fix: Scale pods, contact upstream team

**Timeout Errors**
- Symptoms: Requests timing out
- Investigation: Check CPU/memory, network latency
- Fix: Scale up, increase timeout, check network

**Memory/CPU Exhaustion**
- Symptoms: Pods restarting
- Investigation: `kubectl top pods`, check for leaks
- Fix: Restart, increase limits

**Security Alert**
- Symptoms: Validation failures spike
- Investigation: Check logs for blocked URLs
- Fix: Update whitelist (with approval)

### 4. Rollback Procedure
```bash
# Check deployment history
kubectl rollout history deployment/blueprint-decoder

# Rollback
kubectl rollout undo deployment/blueprint-decoder

# Monitor
kubectl rollout status deployment/blueprint-decoder
```

### 5. Escalation Path
- L1: On-call engineer (now)
- L2: Team lead (30 min if unresolved)
- L3: Manager (60 min if unresolved)

### 6. Contacts
- Slack: #blueprint-decoder-team
- Email: team@example.com
- PagerDuty: [link]

### 7. Post-Incident
- Create incident ticket
- Root cause analysis
- Process improvements
- Update runbook

## Best Practices

- Timely (< 5 min to resolve)
- Accurate (tested in staging)
- Complete (covers common scenarios)
- Clear (no jargon without explanation)
- Updated (quarterly + after incidents)

## Next Steps
- Create RUNBOOK.md
- Document 5+ failure scenarios
- Test procedures in staging
- Train team
- Update after incidents

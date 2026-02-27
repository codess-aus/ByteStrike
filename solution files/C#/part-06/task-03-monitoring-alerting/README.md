# Task 3: Create Monitoring & Alerting

## Overview
Set up comprehensive monitoring, logging, and alerting for production.

## What should be in this directory

1. **Monitoring Setup Code**
   - Structured JSON logging configuration
   - Metrics collection (Prometheus, CloudWatch, etc.)
   - Alert thresholds and rules

2. **Key Metrics to Track**
   - Success rate (should be > 95%)
   - Latency (P95 should be < 10s)
   - Error rate
   - URL validation failures
   - Secrets extracted (count)

3. **Logging Best Practices**
   - Never log secrets (use redaction/masking)
   - Include request ID for correlation
   - Structured JSON format for parsing
   - Appropriate log levels (DEBUG, INFO, WARN, ERROR)

4. **Alerting Rules**
   - Critical: Success rate < 95%
   - High: Latency spike > 50%
   - High: Error rate spike > 25/min
   - Medium: URL validation failures > 100/min

## Tools

- **Logging**: ELK Stack, Datadog, CloudWatch, Stackdriver
- **Metrics**: Prometheus, InfluxDB, CloudWatch
- **Alerting**: PagerDuty, Opsgenie, Slack integration
- **Dashboards**: Grafana, CloudWatch, Datadog

## Implementation

1. Add structured logging to decoder
2. Emit metrics at key points
3. Configure alert rules
4. Set up dashboards
5. Test alerting with load tests

## Example Alerts

```
CRITICAL: Success rate < 95% for 5 minutes
HIGH: P95 latency > 10 seconds for 5 minutes
HIGH: Error rate spike > 25 errors/minute
MEDIUM: URL validation failures > 100/minute
```

## Next Steps
- Deploy monitoring infrastructure
- Instrument decoder code
- Configure alert channels
- Create on-call dashboard
- Test alerting in staging environment

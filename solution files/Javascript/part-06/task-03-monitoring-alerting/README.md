# Task 3: Monitoring & Alerting

## Overview
Set up monitoring, logging, and alerting for production Node.js service.

## What to implement

1. **Structured Logging**
   ```javascript
   const logger = requirePino();
   logger.info({ event: 'decode_start', url }, 'Starting decode');
   logger.error({ event: 'decode_failed', error }, 'Decode failed');
   ```

2. **Metrics Collection**
   ```javascript
   const promClient = require('prom-client');
   const decodeCounter = new promClient.Counter({
     name: 'blueprint_decoder_attempts_total',
     help: 'Total decode attempts'
   });
   ```

3. **Key Metrics**
   - Success rate (target: > 95%)
   - Latency P95 (target: < 10s)
   - Error rate (spike detection)
   - Secrets extracted (count)
   - URL validation failures

4. **Log Aggregation**
   - Send logs to: Datadog, CloudWatch, ELK, LogRocket
   - Format: JSON for parsing
   - Never log secrets (use redaction)

5. **Alerting Rules**
   - Success rate < 95% → Page on-call
   - Latency spike > 50% → Notify team
   - Error rate > 25/min → Investigate
   - URL validation > 100/min → Security alert

## Tools

- **Logging**: Winston, Pino, Bunyan
- **Metrics**: Prometheus client, StatsD
- **Monitoring**: Datadog, New Relic, Splunk
- **Alerting**: PagerDuty, Slack, Opsgenie

## Implementation

```bash
npm install pino prom-client
```

## Next Steps
- Add structured logging
- Emit metrics at key points
- Set up log aggregation
- Configure alert rules
- Create dashboards
- Test in staging

# Monitoring and Alerting Setup

## Structured Logging

```python
import json
import logging
from datetime import datetime
from enum import Enum

class EventType(Enum):
    DECODE_START = "decode_start"
    DECODE_SUCCESS = "decode_success"
    DECODE_FAILURE = "decode_failure"
    URL_VALIDATION_FAILED = "url_validation_failed"
    TIMEOUT = "timeout"
    SECURITY_VIOLATION = "security_violation"

class StructuredLogger:
    def __init__(self, service_name, environment):
        self.service_name = service_name
        self.environment = environment
        self.logger = logging.getLogger(service_name)
    
    def log_event(self, event_type: EventType, message: str, metadata: dict = None):
        """Log event in structured JSON format"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "environment": self.environment,
            "event_type": event_type.value,
            "message": message,
            "metadata": metadata or {}
        }
        
        # Don't log secrets in metadata
        safe_metadata = {k: v for k, v in (metadata or {}).items() 
                        if k not in ['secret', 'password', 'token', 'api_key']}
        log_entry["metadata"] = safe_metadata
        
        self.logger.info(json.dumps(log_entry))

# Usage in decoder
logger = StructuredLogger("blueprint-decoder", "production")

def decode_blueprint_monitored(url):
    logger.log_event(EventType.DECODE_START, "Starting decode operation", {"url": url})
    
    try:
        result = decode_blueprint_safe(url)
        logger.log_event(EventType.DECODE_SUCCESS, 
                        "Decode completed successfully", 
                        {"secret_count": len(result)})
        return result
    except TimeoutError as e:
        logger.log_event(EventType.TIMEOUT, str(e))
        return []
    except Exception as e:
        logger.log_event(EventType.DECODE_FAILURE, str(e))
        return []
```

## Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
decode_attempts = Counter('blueprint_decoder_attempts_total', 
                         'Total decode attempts')
decode_successes = Counter('blueprint_decoder_successes_total', 
                          'Successful decodes')
decode_failures = Counter('blueprint_decoder_failures_total', 
                         'Failed decodes')
decode_duration = Histogram('blueprint_decoder_duration_seconds', 
                           'Time taken to decode')
secrets_extracted = Gauge('blueprint_decoder_secrets_extracted', 
                         'Number of secrets in last decode')
validation_failures = Counter('blueprint_decoder_validation_failures_total',
                             'URL validation failures')

def decode_with_metrics(url):
    decode_attempts.inc()
    start_time = time.time()
    
    try:
        if not validate_url(url):
            validation_failures.inc()
            return []
        
        result = decode_blueprint_safe(url)
        decode_successes.inc()
        secrets_extracted.set(len(result))
        return result
    except Exception:
        decode_failures.inc()
        return []
    finally:
        duration = time.time() - start_time
        decode_duration.observe(duration)
```

## Alert Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Success Rate | < 95% | Page on-call engineer |
| Error Rate Spike | + 50% in 5 min window | Notify team Slack |
| Latency P95 | > 10s | Investigate |
| Failed URL Validations | > 100/min | Security alert |
| Memory Usage | > 80% | AutoScale or restart |

## Alerting Rules (Prometheus/AlertManager)

```yaml
groups:
  - name: blueprint-decoder-alerts
    rules:
      - alert: LowSuccessRate
        expr: |
          (blueprint_decoder_successes_total / blueprint_decoder_attempts_total) < 0.95
        for: 5m
        annotations:
          summary: "Blueprint decoder success rate below 95%"
          description: "Success rate is {{ $value | humanizePercentage }}"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, blueprint_decoder_duration_seconds) > 10
        for: 5m
        annotations:
          summary: "Blueprint decoder latency high"
          description: "P95 latency is {{ $value }}s"
      
      - alert: URLValidationSpike
        expr: |
          rate(blueprint_decoder_validation_failures_total[5m]) > 100
        for: 2m
        annotations:
          summary: "URL validation failures spiking"
          description: "{{ $value }} failures per second"
```

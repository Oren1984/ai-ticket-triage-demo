# Managing and Silencing Monitoring Alerts

When alert noise needs to be managed:

1. Assess if alert is actionable: does it require human intervention?
2. For known maintenance: create silence in Alertmanager with expiry time
3. Tune alert thresholds: adjust in Prometheus rules if false positive rate is high
4. Add proper labels for routing: severity, team, service
5. Implement alert grouping to reduce notification volume
6. Set up escalation policies: page only for critical, email for warning
7. Review and prune stale alert rules quarterly
8. Document runbook links in alert annotations for faster resolution

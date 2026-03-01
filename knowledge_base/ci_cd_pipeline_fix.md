# Fixing Common CI/CD Pipeline Failures

When a CI/CD pipeline fails:

1. Check the failed step in pipeline logs for the exact error message
2. Common build failures: dependency version conflicts, missing environment variables
3. Docker build failures: check Dockerfile syntax, base image availability, disk space
4. Test failures: run failing tests locally to reproduce, check for flaky tests
5. Deploy failures: verify target environment is reachable, check credentials/tokens
6. Artifact issues: verify registry connectivity, check push permissions
7. Timeout issues: increase timeout limits, check for resource contention on runners
8. If pipeline is stuck: cancel and re-run, check runner health and availability

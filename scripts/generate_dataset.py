"""Generate synthetic IT ticket dataset."""

import json
import os
import random

random.seed(42)

TEMPLATES = {
    "Network Issue": [
        "Unable to reach {target} from {source}. Connection times out after {n} seconds.",
        "Network latency spike detected on {target}. Ping shows {n}ms average.",
        "DNS resolution failing for {target}. nslookup returns SERVFAIL.",
        "VPN tunnel to {source} dropped. Users cannot access internal resources.",
        "Packet loss of {n}% observed between {source} and {target}.",
        "Load balancer {target} is returning 502 errors for {n}% of requests.",
        "Switch in rack {n} is unresponsive. Multiple hosts in {source} affected.",
        "Firewall is blocking traffic from {source} to {target} on port {port}.",
        "BGP peering session with upstream provider is flapping on router {target}.",
        "WiFi access point in {source} is not broadcasting SSID. Clients cannot connect.",
        "VLAN {n} misconfigured on switch. Hosts in {source} cannot reach {target}.",
        "MTU mismatch causing fragmentation between {source} and {target}.",
        "Proxy server {target} is not forwarding requests. HTTP {n} errors returned.",
        "Intermittent connectivity drops on {source} segment. Affecting {n} users.",
        "ARP table overflow on router. Hosts in {source} losing connectivity intermittently.",
        "Traceroute to {target} shows blackhole at hop {n}.",
        "Network interface on {target} flapping every {n} minutes.",
        "NTP sync lost on {target}. Clock drift affecting authentication.",
    ],
    "Access / Permissions": [
        "User {user} cannot access the {target} repository. Getting 403 Forbidden.",
        "New hire {user} needs read access to the {target} namespace.",
        "Service account for {target} expired. Deployments are failing.",
        "{user} locked out of {target} after {n} failed login attempts.",
        "Permission denied when {user} tries to write to {target} S3 bucket.",
        "LDAP group {target} is missing {user}. Cannot access shared drives.",
        "SSH key for {user} rejected on {target}. Key might have been rotated.",
        "API token for {target} integration expired {n} days ago.",
        "MFA reset needed for {user}. Authenticator app lost after phone change.",
        "Role binding for {target} namespace too restrictive. {user} cannot list pods.",
        "{user} needs temporary admin access to {target} for maintenance window.",
        "OAuth token refresh failing for {target}. Users getting logged out.",
        "Password policy update locked out {n} users from {target}.",
        "Cross-account IAM role for {target} returning AssumeRole error.",
        "{user} cannot push to {target} branch. Protected branch rules blocking.",
        "SAML SSO login loop for {target}. Assertion validation failing.",
        "Service account {user} hitting rate limit on {target} API. Need quota increase.",
        "Expired client certificate preventing {user} from connecting to {target}.",
    ],
    "Deployment Failure": [
        "CI/CD pipeline failed at {stage} step. Error: {error}.",
        "Docker build for {target} failing. {error}.",
        "Helm chart deployment to {target} timed out after {n} minutes.",
        "Rolling update for {target} stuck. {n} pods in CrashLoopBackOff.",
        "Deployment of {target} failed health check. Readiness probe returning {n}.",
        "Build artifact for {target} not found in registry. Push may have failed.",
        "Terraform apply failed for {target}. State lock held by previous run.",
        "Migration script for {target} failed on step {n}. Database in inconsistent state.",
        "Canary deployment of {target} showing elevated error rate of {n}%.",
        "Config map update for {target} not propagating. Pods still using old config.",
        "Image pull failed for {target}. Registry returning {n} error.",
        "Release {target} rollback needed. New version causing {error}.",
        "Blue-green deployment switch for {target} failed. DNS not updating.",
        "Post-deployment smoke tests for {target} failing on {n} endpoints.",
        "Pipeline for {target} blocked by failing {stage} gate.",
        "Secrets injection for {target} failed. Vault connection timed out.",
        "Auto-scaling policy for {target} not triggering despite {n}% CPU.",
        "Deployment manifest for {target} has invalid {stage} configuration.",
    ],
    "Monitoring / Alert": [
        "Prometheus alert firing for high CPU on {target}. Currently at {n}%.",
        "Grafana dashboard for {target} showing data gaps for last {n} hours.",
        "PagerDuty incident triggered: {target} latency above {n}ms threshold.",
        "Alert fatigue: {n} non-critical alerts from {target} in the last hour.",
        "Disk usage alert on {target}. Volume at {n}% capacity.",
        "Memory usage on {target} steadily climbing. Currently at {n}%.",
        "Error rate for {target} exceeded {n}% threshold. Alert triggered.",
        "Health check for {target} failing. Endpoint returning {n} status.",
        "Log aggregator not receiving logs from {target} for {n} minutes.",
        "Metric collection agent on {target} crashed. No data since {n} minutes ago.",
        "Alert rule for {target} needs tuning. False positive rate at {n}%.",
        "SLO burn rate for {target} exceeding budget. {n}% error budget remaining.",
        "Synthetic monitoring probe to {target} timing out from {source} region.",
        "Anomaly detected in {target} request pattern. Traffic spike of {n}x normal.",
        "Alertmanager silences expired. Getting {n} duplicate alerts for {target}.",
        "APM traces showing {n}ms latency spike in {target} service.",
        "Uptime monitor reports {target} as down from {n} locations.",
        "Dead man's switch alert: {target} has not reported in for {n} minutes.",
    ],
    "Database Issue": [
        "PostgreSQL replica lag on {target} is {n} seconds and growing.",
        "Connection pool exhausted on {target}. Max connections ({n}) reached.",
        "Slow query on {target} taking {n} seconds. Blocking other transactions.",
        "Database backup for {target} failed. Disk space insufficient.",
        "Deadlock detected on {target}. {n} transactions waiting.",
        "Replication to {target} standby broken. WAL files accumulating.",
        "Index bloat on {target} table. Query performance degraded by {n}x.",
        "Autovacuum not running on {target}. Table bloat at {n}GB.",
        "Database migration on {target} failed at step {n}. Needs manual rollback.",
        "Read timeout on {target}. Queries exceeding {n}ms threshold.",
        "Redis cluster {target} lost {n} nodes. Cache miss rate spiking.",
        "MongoDB {target} shard imbalanced. Chunk migration lagging.",
        "MySQL on {target} hit max_allowed_packet limit. Large insert failing.",
        "Elasticsearch cluster {target} yellow. {n} unassigned shards.",
        "Database failover on {target} took {n} seconds. Exceeded RTO target.",
        "Tablespace on {target} at {n}% capacity. Approaching storage limit.",
        "Connection string for {target} has wrong credentials after rotation.",
        "Query planner on {target} choosing sequential scan over index. {n}x slower.",
    ],
    "Infrastructure Issue": [
        "AWS EC2 instance {target} stuck in stopping state for {n} minutes.",
        "Disk IOPS on {target} throttled. Hitting provisioned limit of {n} IOPS.",
        "SSL certificate on {target} expires in {n} days. Needs renewal.",
        "Server {target} kernel panic. System unresponsive.",
        "Cloud storage bucket {target} returning {n} errors on upload.",
        "Auto-scaling group for {target} not launching new instances. Capacity at limit.",
        "Load balancer target group for {target} has {n} unhealthy targets.",
        "Kubernetes node {target} in NotReady state for {n} minutes.",
        "EBS volume on {target} detached unexpectedly. Data may be inconsistent.",
        "Spot instance {target} terminated. Application needs failover.",
        "Container registry {target} running low on storage. {n}GB remaining.",
        "VM {target} performance degraded due to noisy neighbor. CPU steal at {n}%.",
        "Cloud function {target} cold starts taking {n}ms. Exceeding timeout.",
        "Terraform state for {target} corrupted. Cannot plan or apply changes.",
        "Service mesh proxy on {target} consuming excessive memory: {n}GB.",
        "Cron job on {target} has not executed in {n} hours. Scheduler may be stuck.",
        "NFS mount on {target} stale. Applications hanging on I/O.",
        "Hardware RAID on {target} degraded. {n} disk(s) failed.",
    ],
}

TARGETS = [
    "prod-web-01", "prod-api-02", "staging-db-01", "worker-03", "gateway-lb",
    "cache-redis-01", "monitoring-01", "auth-service", "payment-api",
    "data-pipeline", "search-cluster", "prod-k8s", "ci-runner-05",
    "logging-stack", "backup-server", "cdn-edge-01", "queue-rabbitmq",
    "vault-server", "analytics-db", "mail-service",
]

SOURCES = [
    "us-east-1", "eu-west-2", "office-network", "datacenter-a", "vpn-gateway",
    "building-3", "remote-site", "ap-southeast-1", "staging-env", "dev-lab",
]

USERS = [
    "jsmith", "agarcia", "mchen", "kwilliams", "rjohnson",
    "lpatel", "tbrown", "slee", "nwilson", "dmartin",
]

STAGES = ["build", "test", "lint", "deploy", "integration", "security-scan", "push"]

ERRORS = [
    "no space left on device", "out of memory", "connection refused",
    "timeout exceeded", "permission denied", "image not found",
    "invalid configuration", "dependency conflict", "checksum mismatch",
    "rate limit exceeded",
]

PORTS = [80, 443, 8080, 5432, 3306, 6379, 22, 8443, 9090, 3000]

URGENCY_WEIGHTS = {"Low": 0.3, "Medium": 0.4, "High": 0.3}


def fill_template(template: str) -> str:
    return template.format(
        target=random.choice(TARGETS),
        source=random.choice(SOURCES),
        user=random.choice(USERS),
        n=random.randint(1, 99),
        stage=random.choice(STAGES),
        error=random.choice(ERRORS),
        port=random.choice(PORTS),
    )


def generate_tickets(total: int = 1002) -> list[dict]:
    categories = list(TEMPLATES.keys())
    per_category = total // len(categories)
    urgencies = list(URGENCY_WEIGHTS.keys())
    weights = list(URGENCY_WEIGHTS.values())

    tickets = []
    for cat in categories:
        templates = TEMPLATES[cat]
        for i in range(per_category):
            template = templates[i % len(templates)]
            text = fill_template(template)
            urgency = random.choices(urgencies, weights=weights, k=1)[0]
            tickets.append({
                "ticket_text": text,
                "category": cat,
                "urgency": urgency,
            })

    random.shuffle(tickets)
    return tickets


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "tickets.json")

    tickets = generate_tickets()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(tickets)} tickets -> {output_path}")

    # Print distribution
    from collections import Counter
    cat_counts = Counter(t["category"] for t in tickets)
    urg_counts = Counter(t["urgency"] for t in tickets)
    print(f"Categories: {dict(cat_counts)}")
    print(f"Urgencies: {dict(urg_counts)}")


if __name__ == "__main__":
    main()

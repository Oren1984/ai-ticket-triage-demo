# Diagnosing Network Latency Issues

When network latency exceeds acceptable thresholds:

1. Baseline measurement: `ping -c 100 <target>` for RTT statistics
2. Trace the path: `traceroute <target>` or `mtr <target>` for per-hop latency
3. Check for packet loss: `mtr --report --report-cycles 100 <target>`
4. Test bandwidth: `iperf3 -c <target>` between affected hosts
5. Check interface errors: `ip -s link show <interface>` for drops/errors
6. Review switch/router CPU and buffer utilization
7. Check for network congestion: compare traffic volume against link capacity
8. If cloud: check for cross-region traffic, use VPC flow logs for analysis

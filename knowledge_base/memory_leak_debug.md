# Debugging Memory Leaks in Services

When a service shows continuously growing memory usage:

1. Monitor memory trend: `watch -n 5 'ps aux | grep <process>'`
2. Check for OOM kills: `dmesg | grep -i oom` or `journalctl -k | grep -i oom`
3. Take heap dump if Java: `jmap -dump:format=b,file=heap.hprof <pid>`
4. For Python: use tracemalloc or memory_profiler to identify leaking allocations
5. For Node.js: use `--inspect` flag and Chrome DevTools memory profiler
6. Check for unclosed connections, file handles: `lsof -p <pid> | wc -l`
7. Restart service as immediate mitigation while investigating root cause
8. Set memory limits in container/systemd to prevent host impact

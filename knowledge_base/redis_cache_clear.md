# Clearing and Managing Redis Cache

When Redis cache needs to be cleared or managed:

1. Check memory usage: `redis-cli INFO memory`
2. Check number of keys: `redis-cli DBSIZE`
3. Clear specific keys by pattern: `redis-cli --scan --pattern "session:*" | xargs redis-cli DEL`
4. Flush a single database: `redis-cli -n <db> FLUSHDB`
5. Flush all databases (caution): `redis-cli FLUSHALL`
6. Set eviction policy: configure `maxmemory-policy` (allkeys-lru recommended)
7. Check for large keys: `redis-cli --bigkeys`
8. Monitor commands in real time: `redis-cli MONITOR` (disable quickly in prod)

# Fixing PostgreSQL Replication Lag

When replica lag grows beyond acceptable thresholds:

1. Check current lag: `SELECT now() - pg_last_xact_replay_timestamp() AS lag;` on replica
2. Check WAL sender status on primary: `SELECT * FROM pg_stat_replication;`
3. Verify network bandwidth between primary and replica
4. Check replica for long-running queries blocking replay: `SELECT * FROM pg_stat_activity WHERE state = 'active';`
5. If replica is too far behind, consider `pg_rewind` or fresh base backup
6. Check `max_wal_senders` and `wal_keep_segments` on primary
7. Monitor I/O on replica: `iostat -x 1` — slow disks cause replay lag
8. Consider setting `hot_standby_feedback = on` to prevent query conflicts

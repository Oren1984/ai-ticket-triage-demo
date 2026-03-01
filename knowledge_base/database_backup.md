# Database Backup Procedures

Standard backup procedures for PostgreSQL databases:

1. Full logical backup: `pg_dump -h <host> -U <user> -Fc <dbname> > backup_$(date +%Y%m%d).dump`
2. Verify backup integrity: `pg_restore --list backup_*.dump`
3. For large databases, use parallel dump: `pg_dump -j 4 -Fd -f backup_dir/`
4. Store backups in remote storage (S3, GCS): `aws s3 cp backup.dump s3://backups/`
5. Test restore periodically: `pg_restore -d test_db backup.dump`
6. Configure WAL archiving for point-in-time recovery
7. Retain daily backups for 7 days, weekly for 4 weeks, monthly for 12 months
8. Document and test the full disaster recovery procedure

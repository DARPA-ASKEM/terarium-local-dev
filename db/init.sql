/* Postgres logic for `create if not exists` */
SELECT 'CREATE DATABASE askem'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'askem');\gexec

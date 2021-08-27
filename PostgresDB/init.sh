#!/bin/bash
apt-get update && apt-get install postgresql-13-wal2json
psql -U postgres -d anonprofile <<-EOSQL
    CREATE TABLE IF NOT EXISTS anon_profiles (id SERIAL PRIMARY KEY, profiledata JSON );
    ALTER TABLE anon_profiles REPLICA IDENTITY USING INDEX anon_profiles_pkey;
    ALTER SYSTEM SET wal_level to 'replica';
EOSQL


#!/bin/bash
psql -U postgres -d anonprofile
    \c $POSTGRES_DB;
    BEGIN;
        CREATE TABLE anon_profiles (id SERIAL PRIMARY KEY, profiledata JSON );
        ALTER TABLE anon_profiles REPLICA IDENTITY USING INDEX anon_profiles_pkey;
    COMMIT;

EOSQL
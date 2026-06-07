-- Migration 001: Initial schema
-- NHLBI Research Data Portal
-- Created: 2024-11-01
-- Author: [PLACEHOLDER — DBA name]

BEGIN;

-- Users table — stores researcher accounts (no PII beyond email per PIA)
CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role            VARCHAR(50)  NOT NULL DEFAULT 'researcher',
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    last_login_at   TIMESTAMPTZ,
    failed_attempts INTEGER      NOT NULL DEFAULT 0,
    locked_until    TIMESTAMPTZ
);

-- Dataset catalog
CREATE TABLE IF NOT EXISTS datasets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    sensitivity     VARCHAR(20)  NOT NULL DEFAULT 'moderate',  -- low | moderate | high
    owner_org       VARCHAR(255),
    data_steward_id UUID REFERENCES users(id),
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Access control — which users may access which datasets
CREATE TABLE IF NOT EXISTS dataset_access (
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    dataset_id  UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    granted_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by  UUID REFERENCES users(id),
    expires_at  TIMESTAMPTZ,
    PRIMARY KEY (user_id, dataset_id)
);

-- Audit log — immutable record of data access events (AU-2, AU-9)
CREATE TABLE IF NOT EXISTS audit_log (
    id          BIGSERIAL PRIMARY KEY,
    event_time  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    user_id     UUID         REFERENCES users(id),
    action      VARCHAR(100) NOT NULL,
    resource    VARCHAR(255),
    ip_address  INET,
    success     BOOLEAN      NOT NULL DEFAULT TRUE,
    detail      JSONB
);

-- Prevent deletion from audit log (AU-9: Protection of Audit Information)
CREATE RULE no_delete_audit AS ON DELETE TO audit_log DO INSTEAD NOTHING;

COMMIT;

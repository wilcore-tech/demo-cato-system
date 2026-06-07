-- Migration 002: Add payments / subscription tables
-- NHLBI Research Data Portal
-- Created: [PLACEHOLDER — date when this migration is authorized]
-- Author: [PLACEHOLDER — developer name]
-- Security Note: Introduces new tables storing payment-related data.
--   Requires PIA update (new data elements) and SSP update (new data flow).

BEGIN;

-- Stripe customer mapping
CREATE TABLE IF NOT EXISTS payment_customers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255) NOT NULL UNIQUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Subscriptions — tracks active data access tier subscriptions
CREATE TABLE IF NOT EXISTS subscriptions (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id              UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_price_id      VARCHAR(255) NOT NULL,
    status               VARCHAR(50) NOT NULL DEFAULT 'active',  -- active | canceled | past_due
    access_tier          VARCHAR(50) NOT NULL DEFAULT 'standard', -- standard | enhanced | bulk
    current_period_start TIMESTAMPTZ,
    current_period_end   TIMESTAMPTZ,
    canceled_at          TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Webhook event log — idempotency and audit trail for Stripe webhooks
CREATE TABLE IF NOT EXISTS stripe_webhook_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stripe_event_id VARCHAR(255) NOT NULL UNIQUE,
    event_type      VARCHAR(100) NOT NULL,
    processed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload         JSONB
);

-- Index for subscription status lookups
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_status
    ON subscriptions(user_id, status);

COMMIT;

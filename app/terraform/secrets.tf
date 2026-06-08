# secrets.tf — AWS Secrets Manager resources for payment integration
# Introduced by: payments/stripe_client.py integration
# Security Note: Adds new secrets to the system boundary.
#   SSP CM-2 (baseline configuration) and SC-12 (key management)
#   sections require update to reflect new secrets.

# Stripe API key — runtime secret for Stripe HTTP client
resource "aws_secretsmanager_secret" "stripe_api_key" {
  name        = "nhlbi-rdp/${var.environment}/stripe-api-key"
  description = "Stripe secret API key for NHLBI-RDP payment integration"

  recovery_window_in_days = 7

  tags = {
    Project        = "NHLBI-RDP"
    Environment    = var.environment
    Classification = "Sensitive"
    Rotation       = "Manual-90-days"
  }
}

resource "aws_secretsmanager_secret_version" "stripe_api_key" {
  secret_id     = aws_secretsmanager_secret.stripe_api_key.id
  secret_string = "[PLACEHOLDER — set actual value via AWS Console or CLI; never in source code]"

  lifecycle {
    ignore_changes = [secret_string]
  }
}

# Stripe webhook signing secret
resource "aws_secretsmanager_secret" "stripe_webhook_secret" {
  name        = "nhlbi-rdp/${var.environment}/stripe-webhook-secret"
  description = "Stripe webhook endpoint signing secret for NHLBI-RDP"

  recovery_window_in_days = 7

  tags = {
    Project        = "NHLBI-RDP"
    Environment    = var.environment
    Classification = "Sensitive"
    Rotation       = "Manual-90-days"
  }
}

resource "aws_secretsmanager_secret_version" "stripe_webhook_secret" {
  secret_id     = aws_secretsmanager_secret.stripe_webhook_secret.id
  secret_string = "[PLACEHOLDER — set actual value via AWS Console or CLI]"

  lifecycle {
    ignore_changes = [secret_string]
  }
}

# IAM policy extension — grant app task role access to new Stripe secrets
data "aws_iam_policy_document" "stripe_secrets_policy" {
  statement {
    sid    = "ReadStripeSecrets"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = [
      aws_secretsmanager_secret.stripe_api_key.arn,
      aws_secretsmanager_secret.stripe_webhook_secret.arn,
    ]
  }
}

resource "aws_iam_role_policy" "app_task_stripe_secrets" {
  name   = "nhlbi-rdp-app-task-stripe-secrets"
  role   = aws_iam_role.app_task.id
  policy = data.aws_iam_policy_document.stripe_secrets_policy.json
}

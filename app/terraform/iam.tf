# IAM roles for the NHLBI RDP ECS workload
# Implements least-privilege per NIST SP 800-53 AC-6

data "aws_iam_policy_document" "ecs_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# ECS Task Execution Role — allows ECS agent to pull images and write logs
resource "aws_iam_role" "ecs_execution" {
  name               = "nhlbi-rdp-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json

  tags = {
    Project = "NHLBI-RDP"
  }
}

resource "aws_iam_role_policy_attachment" "ecs_execution_managed" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# App Task Role — runtime permissions for the application container (least privilege)
resource "aws_iam_role" "app_task" {
  name               = "nhlbi-rdp-app-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json

  tags = {
    Project = "NHLBI-RDP"
  }
}

data "aws_iam_policy_document" "app_task_policy" {
  # Read-only access to specific S3 bucket for dataset files
  statement {
    sid    = "DatasetS3ReadOnly"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::nhlbi-rdp-datasets",
      "arn:aws:s3:::nhlbi-rdp-datasets/*",
    ]
  }

  # CloudWatch Logs — write application logs
  statement {
    sid    = "CloudWatchLogs"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:log-group:/ecs/nhlbi-rdp:*"]
  }
}

resource "aws_iam_role_policy" "app_task" {
  name   = "nhlbi-rdp-app-task-policy"
  role   = aws_iam_role.app_task.id
  policy = data.aws_iam_policy_document.app_task_policy.json
}

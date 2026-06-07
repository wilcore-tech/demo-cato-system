terraform {
  required_version = ">= 1.4.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "nhlbi-rdp-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "nhlbi-rdp-tf-locks"
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (prod, staging)"
  type        = string
  default     = "prod"
}

# ECS Cluster
resource "aws_ecs_cluster" "nhlbi_rdp" {
  name = "nhlbi-rdp-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment    = var.environment
    Project        = "NHLBI-RDP"
    Classification = "Moderate"
  }
}

# ECS Service
resource "aws_ecs_service" "nhlbi_rdp" {
  name            = "nhlbi-rdp-service"
  cluster         = aws_ecs_cluster.nhlbi_rdp.id
  task_definition = aws_ecs_task_definition.nhlbi_rdp.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.nhlbi_rdp.arn
    container_name   = "app"
    container_port   = 8080
  }

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  tags = {
    Environment = var.environment
    Project     = "NHLBI-RDP"
  }
}

resource "aws_ecs_task_definition" "nhlbi_rdp" {
  family                   = "nhlbi-rdp"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "ghcr.io/wilcore-tech/nhlbi-rdp:latest"
      essential = true
      portMappings = [{ containerPort = 8080, protocol = "tcp" }]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/nhlbi-rdp"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

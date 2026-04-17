# terraform-skeleton.tf
# Minimal skeleton for a service's cloud infrastructure.
# Replace <SERVICE_NAME> throughout. Run: terraform init && terraform plan

terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state — uncomment and configure before first apply
  # backend "s3" {
  #   bucket         = "<ORG>-terraform-state"
  #   key            = "services/<SERVICE_NAME>/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "<ORG>-terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Service     = var.service_name
      Environment = var.environment
      ManagedBy   = "terraform"
      Team        = var.team
    }
  }
}

# ─── Variables ────────────────────────────────────────────────────────────────

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region to deploy to"
}

variable "service_name" {
  type        = string
  description = "Short name of the service (kebab-case, e.g. order-service)"
}

variable "environment" {
  type        = string
  description = "Deployment environment: dev | staging | prod"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod"
  }
}

variable "team" {
  type        = string
  description = "Owning team name"
}

variable "container_image" {
  type        = string
  description = "Full container image with tag, e.g. 123456789.dkr.ecr.us-east-1.amazonaws.com/order-service:1.2.3"
}

variable "desired_count" {
  type        = number
  default     = 2
  description = "Number of tasks/replicas to run"
}

# ─── Networking ───────────────────────────────────────────────────────────────

data "aws_vpc" "default" {
  default = true
  # Replace with specific VPC lookup for non-default environments:
  # tags = { Name = "<ORG>-${var.environment}-vpc" }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ─── IAM role for the service ─────────────────────────────────────────────────

resource "aws_iam_role" "service" {
  name = "${var.service_name}-${var.environment}-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Attach additional policies below using aws_iam_role_policy_attachment.
# Example: read from a specific S3 bucket, read from Secrets Manager, etc.

# ─── Secrets: Secrets Manager entries ────────────────────────────────────────
# Create one entry per secret the service needs.
# Values are set out-of-band (CI/CD or operator) — never commit secret values.

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "/${var.environment}/${var.service_name}/db-password"
  description             = "Database password for ${var.service_name}"
  recovery_window_in_days = 7
}

# ─── Container registry ───────────────────────────────────────────────────────

resource "aws_ecr_repository" "service" {
  name                 = var.service_name
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# ─── ECS Cluster + Fargate service ───────────────────────────────────────────
# Add your ECS task definition and service here.
# Recommended: extract into a module at modules/ecs-fargate-service/.

# ─── Outputs ──────────────────────────────────────────────────────────────────

output "ecr_repository_url" {
  value       = aws_ecr_repository.service.repository_url
  description = "ECR repository URL to push images to"
}

output "service_role_arn" {
  value       = aws_iam_role.service.arn
  description = "IAM role ARN for the service tasks"
}


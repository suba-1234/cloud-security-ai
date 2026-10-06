terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ============================================================
# KMS KEY
# ============================================================

resource "aws_kms_key" "cloud_security_demo" {
  description             = "KMS key for Cloud Security AI S3 buckets"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid    = "EnableIAMUserPermissions"
        Effect = "Allow"

        Principal = {
          AWS = "arn:aws:iam::749223561219:root"
        }

        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

# ============================================================
# MAIN S3 BUCKET
# ============================================================

resource "aws_s3_bucket" "cloud_security_demo" {
  bucket = "cloud-security-ai-demo-749223561219"
}

# Block public access
resource "aws_s3_bucket_public_access_block" "cloud_security_demo" {
  bucket = aws_s3_bucket.cloud_security_demo.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning
resource "aws_s3_bucket_versioning" "cloud_security_demo" {
  bucket = aws_s3_bucket.cloud_security_demo.id

  versioning_configuration {
    status = "Enabled"
  }
}

# KMS encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "cloud_security_demo" {
  bucket = aws_s3_bucket.cloud_security_demo.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.cloud_security_demo.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# Lifecycle
resource "aws_s3_bucket_lifecycle_configuration" "cloud_security_demo" {
  bucket = aws_s3_bucket.cloud_security_demo.id

  rule {
    id     = "cleanup-old-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# ============================================================
# LOGGING S3 BUCKET
# ============================================================

resource "aws_s3_bucket" "cloud_security_logs" {
  bucket = "cloud-security-ai-logs-749223561219"
}

# Block public access for logging bucket
resource "aws_s3_bucket_public_access_block" "cloud_security_logs" {
  bucket = aws_s3_bucket.cloud_security_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning for logging bucket
resource "aws_s3_bucket_versioning" "cloud_security_logs" {
  bucket = aws_s3_bucket.cloud_security_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

# KMS encryption for logging bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "cloud_security_logs" {
  bucket = aws_s3_bucket.cloud_security_logs.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.cloud_security_demo.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# Lifecycle for logging bucket
resource "aws_s3_bucket_lifecycle_configuration" "cloud_security_logs" {
  bucket = aws_s3_bucket.cloud_security_logs.id

  rule {
    id     = "cleanup-logs"
    status = "Enabled"

    filter {}

    expiration {
      days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# ============================================================
# S3 ACCESS LOGGING
# ============================================================

resource "aws_s3_bucket_logging" "cloud_security_demo" {
  bucket = aws_s3_bucket.cloud_security_demo.id

  target_bucket = aws_s3_bucket.cloud_security_logs.id
  target_prefix = "log/"
}
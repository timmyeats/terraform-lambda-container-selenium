resource "random_string" "random" {
  length  = 8
  lower   = true
  upper   = false
  special = false
}

# ECR repository for Lambda container image
resource "aws_ecr_repository" "lambda_repo" {
  name = "${var.resource_tags.project}-${random_string.random.id}"
  tags = var.resource_tags

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Generate timestamp for unique image tags (UTC+8)
locals {
  timestamp = formatdate("YYMMDD-hhmmss", timeadd(timestamp(), "8h"))
  source_hash = md5(join("", [
    filemd5("../context/main.py"),
    filemd5("../context/font_handler.py"),
    filemd5("../context/loading_handler.py"),
    filemd5("../context/Dockerfile")
  ]))
}

# Build and push Docker image to ECR
module "lambda_docker_image" {
  source  = "terraform-aws-modules/lambda/aws//modules/docker-build"
  version = "7.21.0"

  create_ecr_repo = false
  ecr_repo        = aws_ecr_repository.lambda_repo.name
  ecr_repo_tags   = var.resource_tags
  source_path     = "../context"
  image_tag       = "v${local.timestamp}"

  # Use the existing Dockerfile in context directory
  docker_file_path = "Dockerfile"

  # Force rebuild when source code changes
  triggers = {
    timestamp            = local.timestamp
    source_hash          = local.source_hash
    dockerfile_hash      = filemd5("../context/Dockerfile")
    main_py_hash         = filemd5("../context/main.py")
    font_handler_hash    = filemd5("../context/font_handler.py")
    loading_handler_hash = filemd5("../context/loading_handler.py")
  }
}

# Lambda function using container image
module "lambda_container" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.21.0"

  function_name = "${var.resource_tags.project}-${random_string.random.id}"
  description   = "Lambda function from container image for Selenium web scraping"

  # Container configuration
  create_package = false
  image_uri      = module.lambda_docker_image.image_uri
  package_type   = "Image"
  architectures  = ["x86_64"]

  # Function configuration
  memory_size = 1024
  timeout     = 300 # 5 minutes for complex scraping tasks

  # Environment variables
  environment_variables = {
    ENVIRONMENT = "prod"
    LOG_LEVEL   = "INFO"
  }

  tags = var.resource_tags

  depends_on = [module.lambda_docker_image]
}

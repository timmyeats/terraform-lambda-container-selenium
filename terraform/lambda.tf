module "lambda_container" {
  source         = "terraform-aws-modules/lambda/aws"
  version        = "4.6.0"
  function_name  = "${var.resource_tags.project}-${random_string.random.id}"
  description    = "Lambda function from container image"
  create_package = false
  memory_size    = 1024
  timeout        = 60
  tags           = var.resource_tags

  # Container Image
  image_uri     = module.lambda_docker_image.image_uri
  package_type  = "Image"
  architectures = ["x86_64"]
}

# Check the main.py status in the context folder
resource "null_resource" "lambda_docker_image" {
  triggers = {
    context = filemd5("../context/main.py")
  }
}

module "lambda_docker_image" {
  source          = "terraform-aws-modules/lambda/aws//modules/docker-build"
  version         = "4.6.0"
  create_ecr_repo = true
  source_path     = "../context"
  image_tag       = "latest"
  ecr_repo        = "${var.resource_tags.project}-${random_string.random.id}"
  depends_on      = [null_resource.lambda_docker_image]
  ecr_repo_tags   = var.resource_tags
}

resource "random_string" "random" {
  length  = 8
  lower   = true
  upper   = false
  special = false
}
# Lambda Function
output "lambda_function_name" {
  description = "The name of the Lambda Function"
  value       = module.lambda_container.lambda_function_name
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda Function"
  value       = module.lambda_container.lambda_function_arn
}

# Docker Image
output "lambda_docker_image_uri" {
  description = "The ECR Docker image URI used to deploy Lambda Function"
  value       = module.lambda_docker_image.image_uri
}

# ECR Repository
output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.lambda_repo.repository_url
}

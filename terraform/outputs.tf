# Lambda Function
output "lambda_function_name" {
  description = "The name of the Lambda Function"
  value       = module.lambda_container.lambda_function_name
}

# Docker Image
output "lambda_docker_image_uri" {
  description = "The ECR Docker image URI used to deploy Lambda Function"
  value       = module.lambda_docker_image.image_uri
}
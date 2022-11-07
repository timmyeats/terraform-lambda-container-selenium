variable "aws_region" {
  default     = "us-east-1"
  type        = string
  description = "The resource deployment region"
}

variable "resource_tags" {
  type        = map(string)
  description = "Tags to apply to resources"
}

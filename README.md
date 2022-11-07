# Terraform Lambda Container Selenium

Using this terraform module you can deploy a lambda function that will run a selenium in a lambda container.

## Prerequisites

- Install Terraform

- Install AWS CLI

- Set AWS credential in your environment, ```aws configure  --profile your_profile_name```

- Set AWS profile in your environment, ```export AWS_PROFILE=your_profile_name```

## Configuration

Modify ```terraform.tfvars.template``` to ```terraform.tfvars```, and set the tfvars

```
resource_tags = {
  terraform = "true"
  project   = "lambda-container-selenium"
  version   = "1.0"
}
```

### Deploy and Destroy

#### Resources in a single region

- Deploy resources:

   `terraform init`

   `terraform plan`

   `terraform apply`

- Destroy resources:

   `terraform destroy`


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0 |
| <a name="requirement_docker"></a> [docker](#requirement\_docker) | >= 2.0 |
| <a name="requirement_null"></a> [null](#requirement\_null) | >= 3.0 |
| <a name="requirement_random"></a> [random](#requirement\_random) | >= 3.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.38.0 |
| <a name="provider_null"></a> [null](#provider\_null) | 3.2.0 |
| <a name="provider_random"></a> [random](#provider\_random) | 3.4.3 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_lambda_container"></a> [lambda\_container](#module\_lambda\_container) | terraform-aws-modules/lambda/aws | 4.6.0 |
| <a name="module_lambda_docker_image"></a> [lambda\_docker\_image](#module\_lambda\_docker\_image) | terraform-aws-modules/lambda/aws//modules/docker-build | 4.6.0 |

## Resources

| Name | Type |
|------|------|
| [null_resource.lambda_docker_image](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |
| [random_string.random](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |
| [aws_caller_identity.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_ecr_authorization_token.token](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ecr_authorization_token) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The resource deployment region | `string` | `"us-east-1"` | no |
| <a name="input_resource_tags"></a> [resource\_tags](#input\_resource\_tags) | Tags to apply to resources | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_docker_image_uri"></a> [lambda\_docker\_image\_uri](#output\_lambda\_docker\_image\_uri) | The ECR Docker image URI used to deploy Lambda Function |
| <a name="output_lambda_function_name"></a> [lambda\_function\_name](#output\_lambda\_function\_name) | The name of the Lambda Function |
<!-- END_TF_DOCS -->
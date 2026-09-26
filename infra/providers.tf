# Providers tf tells terraform whcih cloud (or service) it is going to talk to, and hot wo configure that connection 
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.66.0"
    }
  }
}

provider "aws" {
    region = var.aws_region
}
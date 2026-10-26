locals {
  services = ["ui", "api", "worker"] # Creating three different repos for each task 
}
resource "aws_ecr_repository" "services" { ## Declaring the ecr repository 
  for_each = toset(local.services) ## Creating one rpeo for each unique service name 
  name = "research-rag-$(each.key)" ## Name of the each repos
  image_tag_mutability = "MUTABLE" ## Overwriting permissions 
  force_delete = true # Permission to delete if needed
  image_scanning_configuration { ## Scanning for any vulnerabilities
    scan_on_push = true
  }
}
locals {
  services = ["ui", "api", "worker"] # Creating three different repos for each task 
}
resource "aws_ecr_repository" "services" { ## Declaring the ecr repository 
  for_each = toset(local.services) ## Creating one rpeo for each unique service name 
  

}
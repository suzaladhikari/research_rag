## Checking which zones are available for my region 
data "aws_availability_zones" "available_zones" {
  state = "available"
} ## This lists out all the available zones 

locals { ## Values that can be used later or can be said variable 
    azs = slice(data.aws_availability_zones.available_zones.names, 0, 2) ## Selecing only the first two zones 
    public_cidrs = ["10.0.1.0/24", "10.0.2.0/24"] ## Location for each subnet
    private_cidrs = ["10.0.11.0/24", "10.0.12.0/24"] ## Location for the private subnets
}## This is just a variable whwere if we do locals.azs then we can access the list of available 2 zones, similarly two access teh public and private cidrds same process can be done 

resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16" ## Think of the vpc as a town and subnets as the neighbourhood and task as houses
    enable_dns_support = true
    enable_dns_hostnames = true
}
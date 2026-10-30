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
### Creating the public subnet first
resource "aws_subnet" "public" {
    count = 2
    vpc_id = aws_vpc.main.id ## Both belong to the VPC created as main 
    cidr_block = local.public_cidrs[count.index] ## Give each subnet its corresponding address range from the lcoal.public_cidrs 
    availability_zone = local.azs[count.index]
    tags = {Name = "research-rag-public-${local.azs[count.index]}"} ## The name would look like research-rag-public-us-east-1a/1b
}

resource "aws_subnet" "private" {
    count = 2
    vpc_id = aws_vpc.main.id 
    cidr_block = local.private_cidrs[count.index]
    availability_zone = local.azs[count.index]
    tags = {Name = "research-rag-private-${local.azs[count.index]}"} 
}

## Creating the internet gateway so that the public subnets can communicate to the internet

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id ## which vpc it belongs to 
  tags   = { Name = "research-rag-igw" }
}

## Giving direction for the public subnets to access the internet 
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id ## which vpc it belongs to 
  route = {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = {Name = "research-rag-public-rt"}

}

## Applying the route table instructino to both subnets 
resource "aws_route_table_association" "public" {
  count = 2
  subnet_id = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
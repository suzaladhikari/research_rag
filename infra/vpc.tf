## Checking which zones are available for my region 
data "aws_availability_zones" "available_zones" {
  state = "available"
} ## This lists out all the available zones 

locals { ## Values that can be used later or can be said variable 
    azs = slice(data.aws_availability_zones.available_zones.names, 0, 2) ## Selecing only the first two zones 
}
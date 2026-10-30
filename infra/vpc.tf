## Checking which zones are available for my region 
data "aws_availability_zones" "available_zones" {
  state = "available"
} ## This lists out all the available zones 

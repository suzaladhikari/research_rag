### Setting up the varaibles that can be used in the main terraform 
variable "aws_region" {
    description = "AWS Region that needs to be used"
    type = string
    default = 'us-east-1'
}
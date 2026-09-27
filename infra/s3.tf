resource "random_id" "bucket_suffix" {
    byte_length = 4
} ## creatinga random hexadecimal value 

resource "aws_s3_bucket" "uploads" {

} ## Aws s3 bucket is the resource type that comes from the AWS provider, and the nickname to this bucket is uploads
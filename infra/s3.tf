resource "random_id" "bucket_suffix" {
    byte_length = 4
} ## creatinga random hexadecimal value 

resource "aws_s3_bucket" "uploads" {
    bucket = "security-rag-uploads-${random_id.bucket_suffix.hex}"
}
# Aws s3 bucket is the resource type that comes from the AWS provider, and the nickname to this bucket is uploads
# here we have used to create the bucket name using the random hexadecimal created from random_id resurouce 

## Adding encryption to the bucket 
resource "aws_s3_bucket_server_side_encryption_configuration" "updates_encryption" {
    bucket = aws_s3_bucket.uploads.id
    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}
# Block all the public access

resource "aws_s3_bucket_public_access_block" "uploads_block" {
    bucket = aws_s3_bucket.uploads.id
    block_public_policy =  true
    block_public_acls =  true
    ignore_public_acls = true
    restrict_public_buckets = true
  
}

output "bucket_name" {
  value = aws_s3_bucket.uploads.id
}
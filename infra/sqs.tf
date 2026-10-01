### Creating dlq to hold the message request that fail
resource "aws_sqs_queue" "dlq" {
    name = "security-rag-dlq"
    message_retention_seconds = 1209600
    sqs_managed_sse_enabled = true 
}
resource "aws_sqs_queue" "retrieve" {
    name = "security-rag-sqs"
    receive_wait_time_seconds = 20 ## Adding long polling where sqs waits for 20 seconds for the message before returning an empty response
    visibility_timeout_seconds = 300 ## The message will be hidden for 300 seconds before the other worker try to access it !
    message_retention_seconds = 345600 ## If the message is in queue then that will get hold for 4 days if not gets removed
    sqs_managed_sse_enabled = true 
    redrive_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.dlq.arn
        maxReceiveCount = 3 
    })
}

### Giving the s3 authority to communicate with sqs
resource "aws_sqs_queue_policy" "allow_s3_communication" {
  queue_url = aws_sqs_queue.retrieve.id
  policy = jsondecode({
    Version = "2012-10-17" ## Adding version in orderto stop the AWS timeout 
    
  })

}

output "sqs_queue_url" {
  value = aws_sqs_queue.retrieve.url ## Returns the url for sqs
}

output "sqs_dlq_url" {
  value = aws_sqs_queue.dlq.url ## Returns the url for dlq
}



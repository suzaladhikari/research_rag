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
    Statment = [{
      Effect = "Allow" ## Granting permission for the operatoin described below
      Principal = {Service = "s3.amazonaws.com"} ## Who can perform it 
      Action = "sqs:SendMessage" ## What can s3 do ?!
      Resource = aws_sqs_queue.retrieve.arn ### Where can it send message 
      Condition = {
        ArnEquals = {"aws:SourceArn" = aws_s3_bucket.uploads.arn}
      }
    }] ## List of permissions
  })

}

##Telling the bucket to push an event to the queue whenever an object is created under uploads/

resource "aws_s3_bucket_notification" "uploading_notify" {
  bucket = aws_s3_bucket.uploads.id
  queue {
    queue_arn = aws_sqs_queue.retrieve.arn ## Sending the notifications to the retrieve SQS queue 
    events = ["s3:ObjectCreated:*"] ## Sending notification whenever an object is created 
    filter_prefix = "uploads/" ##Only notify for objects whose keys start with uploads/ 
  }
  depends_on = [aws_sqs_queue_policy.allow_s3_communication] ## It depends on the rule based on the allow_s3_communication

}

output "sqs_queue_url" {
  value = aws_sqs_queue.retrieve.url
  
}

output "sqs_dlq_url" {
  value = aws_sqs_queue.dlq.url ## Returns the url for dlq
}



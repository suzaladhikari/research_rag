### Creating dlq to hold the message request that fail
resource "aws_sqs_queue" "dlq" {
    name = "security-rag-dlq"
    message_retention_seconds = 1209600
    sqs_managed_sse_enabled = true 
}
resource "aws_sqs_queue" "retrieve" {
    name = "security-rag-sqs"
    receive_wait_time_seconds = 20
}

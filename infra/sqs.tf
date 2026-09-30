resource "aws_sqs_queue" "retrieve" {
    name = "security-rag-sqs"
    receive_wait_time_seconds = 10
}

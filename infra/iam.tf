resource "aws_iam_role" "api_task" { ## If this is accessed or used in the task defination then following permission is granted 
    name = "research-rag-api-task"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
    })


  
}
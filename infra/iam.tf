resource "aws_iam_role" "api_task" { ## If this is accessed or used in the task defination then following permission is granted 
    name = "research-rag-api-task"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"  
                Principal = {
                    Serivce = "ecs_tasks.amazonaws.com"  ## Who is allowed to use this role 
                }
            Action = "sts:AssumeRole"
            }
        ]
    })
}
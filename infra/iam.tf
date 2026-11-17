resource "aws_iam_role" "api_task" { ## If this is accessed or used in the task defination then following permission is granted 
    name = "research-rag-api-task"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"  
                Principal = {
                    Service = "ecs_tasks.amazonaws.com"  ## Who is allowed to use this role 
                }
            Action = "sts:AssumeRole"
            }
        ]
    })
}

## Adding permissions to the role 
resource "aws_iam_role_policy" "api_permissions" {
  name = "research-rag-api-permissions"
  role = aws_iam_role.api_task.id ## Attaching to the API role 
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = "s3:PutObject"
            Resource = "${aws_s3_bucket.uploads.arn}"
        }
    ]
  })
}
resource "aws_iam_role" "app_task" { ## If this is accessed or used in the task defination then following permission is granted 
    name = "research-rag-app-permissions"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"  
                Principal = {
                    Service = "ecs-tasks.amazonaws.com"  ## Who is allowed to use this role 
                }
            Action = "sts:AssumeRole"
            }
        ]
    })
}

## Adding permissions to the role 
resource "aws_iam_role_policy" "app_permissions" {
  name = "research-rag-app-permissions"
  role = aws_iam_role.app_task.id  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = "s3:*" ## This is the way of allowing what needs to be happened
            Resource = [aws_s3_bucket.uploads.arn, "${aws_s3_bucket.uploads.arn}/*"] ## This gives permissoin to list the bucket, delete the bucket and upload and delete the file insisde the bucket as well 
        },
        {
            Effect = "Allow"
            Action = "sqs:*"
            Resource = aws_sqs_queue.retrieve.arn ## This gives permission to delete message and add message 
        }

    ]
  })
}

## Creating the execution permission for ECS- meaning ECS uses it to download the ECR in the private repository 
resource "aws_iam_role" "ecs_execution" {
  name = "research-rag-ecs-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Principal = {
            Service = "ecs-task.amazonaws.com" ## Who is allowed to use this role - ECS
        }
        Action = "sts:AssumeRole"
    }]
  })
}
## What does the IAM role do actually ?
resource "aws_iam_role_attachment" "ecs_execution" { ## What kind of permission does ECS gets
    role = aws_iam_role.ecs_execution.id
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
} ## We used aws_iam_role_attachment because the ecs execution already exists 


### Task definition is all about the settings for ecs to run the ecr images
resource "aws_ecs_task_definition" "api" { ## Setting up the task definition for the api 
    family = "research-rag-api" ## Name of the task 
    network_mode = "awsvpc" ## Gives tasks its own ip address and network interface 
    requires_compatibilities = ["FARGATE"] ## This task must be compatible with Fargate

    cpu = "256"  ## 0.25 vCPU 
    memory = "512" ## 512 MiB 

    execution_role_arn =  aws_iam_role.ecs_execution.arn  
    task_role_arn = aws_iam_role.app_task.arn 
    container_definitions = jsonencode({
        name = "api-conatiner" ## Name of the contianer after the container is created from ECS 
        image = "${aws_ecr_repository.services["api"].repository_url}:latest" ## This is the image that will run 
    })

}

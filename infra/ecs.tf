### Starting to write the ecs code   
resource "aws_ecs_task_definition" "api" { ## Setting up the task definition for the api 
    family = "research-rag-api" ## Name of the task 
    network_mode = "awsvpc" ## Gives tasks its own ip address and network interface 
    requires_compatibilities = ["FARGATE"] ## This task must be compatible with Fargate

    cpu = "256"  ## 0.25 vCPU 
    memory = "512" ## 512 MiB 
    
}

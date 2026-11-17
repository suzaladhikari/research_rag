### Starting to write the ecs code   
resource "aws_ecs_task_definition" "api" { ## Setting up the task definition for the api 
    family = "research-rag-api"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
  
}

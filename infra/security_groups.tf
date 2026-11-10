### Security groups are a set of rules attached to an individual resource, It is like a lock in each room. 
### ALB 
resource "aws_security_group" "alb" {
  name = "research-rag-alb"
  description = "ALlowing the web traffic to the load balancer"
  vpc_id = aws_vpc.main.id ## This is the vpc that the load balancer belongs to 
  ingress { ## Traffic coming into the resource
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  } ## This is the from Users -> ALB, on port 80
  egress { ## Traffic going out of the resource 
    from_port = 0
    to_port = 0 
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  } ### This is from ALB to all the tasks 
}

## Setting up the lock in the streamlit 
resource "aws_security_group" "api" {
  name = "research-rag-api" ## This will be the name of the rag's security group
  vpc_id = aws_vpc.main.id
  description = "This handles the user's request and does all the frontend tasks"
  ingress {
    
  }
}
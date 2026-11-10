### Security groups are a set of rules attached to an individual resource, It is like a lock in each room. 
### ALB 
resource "aws_security_group" "alb" {
  name = "research-rag-alb"
  description = "ALlowing the web traffic to the load balancer"
  vpc_id = aws_vpc.main.id ## This is the vpc that the load balancer belongs to 
  ingress { ## Traffic coming into the resource
    from_port = 80 ## Allowing anyone in the internet to connect with the alb 
    to_port = 80 
    protocol = "tcp" 
    cidr_blocks = ["0.0.0.0/0"] ## Who is allowed (internet)
  } ## This is the from Users -> ALB, on port 80
  egress { ## Traffic going out of the resource 
    from_port = 0
    to_port = 0 
    protocol = "-1" ## Since we are not considering any protocol, the from_port and to_port really doesnot matter. Long story short The ALB may connect out to anywhere, on any port, using any protocol. 
    cidr_blocks = ["0.0.0.0/0"]
  } ### This is from ALB to all the tasks 
}

## Setting up the lock in the streamlit 
resource "aws_security_group" "ui" {
  name = "research-rag-ui" ## This will be the name of the rag's security group
  vpc_id = aws_vpc.main.id
  description = "This handles the user's request and does all the frontend tasks"
  ingress {
    from_port = 8501
    to_port = 8501
    protocol = "tcp"
    security_groups = [aws_security_group.alb.id] ## Only resources or request with ALB security group can connect 
  }
  egress {## egress can connec to anything with any protocol 
    from_port = 0
    to_port = 0 
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"] ### Can be any destination 
  }
}

resource "aws_security_group" "api" {
  name = "research-rag-api"
  vpc_id = aws_vpc.main.id 
  description = "This is the security group for the api"
  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    security_groups = [aws_security_group.ui.id]
  }
  egress {
    from_port = 0
    to_port = 0 
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

## Setting up for the worker 
resource "aws_security_group" "worker" {
  name = "research-rag-worker"
  
  
}
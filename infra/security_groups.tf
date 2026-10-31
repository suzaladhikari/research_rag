### ALB 
resource "aws_security_group" "alb" {
  name = "research-rag-alb"
  description = "ALlowing the web traffic to the load balancer"
  vpc_id = aws_vpc.main.id ## This is the vpc that the load balancer belongs to 
  ingress = {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  } ## What kind of traffic should be allowed to come 
  egress = {
    from_port = 0
    to_port = 0 
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

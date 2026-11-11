### This file is for the database that will be hosted in RDS 
resource "aws_db_subnet_group" "rds" {
  name = "researhc-rag-rds-subnets"
  subnet_ids = [aws_subnet.private[0].id, aws_subnet.private[1].id] ## Giving exact location on where to put the RDS i.e. private subnets
}
resource "aws_db_instance" "pg" {
  identifier = "research-rag-db"
  engine = "postgres"
  engine_version = "16"
  ## Setting up the rds server computing power and storage 
  instance_class = "db.t4g.micro" ## Choosing the server's RAM and CPU
  allocated_storage = 20 ## Allocating 20 GiB of storage 

}
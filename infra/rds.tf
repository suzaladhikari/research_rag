### This file is for the database that will be hosted in RDS 
resource "aws_db_subnet_group" "rds" {
  name = "researhc-rag-rds-subnets"
  subnet_ids = [aws_subnet.private[0].id, aws_subnet.private[1].id] ## Giving exact location on where to put the RDS i.e. private subnets
}
resource "aws_db_instance" "pg" {
  identifier = "security-rag-db"
  
}
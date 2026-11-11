### This file is for the database that will be hosted in RDS 
resource "aws_db_subnet_group" "rds" {
  name = "research-rag-rds-subnets"
  subnet_ids = [aws_subnet.private[0].id, aws_subnet.private[1].id] ## Giving exact location on where to put the RDS i.e. private subnets
}
resource "aws_db_instance" "pg" {
  identifier = "research-rag-db" ## RDS instance in AWS/ "research-rag-db" belongs to this project 
  engine = "postgres"
  engine_version = "16"
  ## Setting up the rds server computing power and storage 
  instance_class = "db.t4g.micro" ## Choosing the server's RAM and CPU
  allocated_storage = 20 ## Allocating 20 GiB of storage 
  storage_type = "gp3" ## Uses SSD 
  storage_encrypted = true ## Encrypts the data 

  ### Setting up the name of the database 
  db_name = "rag_db"
  username = "rag_admin" ## Username for the database 
  manage_master_user_password = true ## This stores the password for the database created 

  db_subnet_group_name = aws_db_subnet_group.rds.name ## Use the research-rag-rds-subnets subnet group to put the rds 
  


}
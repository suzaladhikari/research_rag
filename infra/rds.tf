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
  vpc_security_group_ids = [aws_security_group.rds.id] ## Uses the security group RDS 
  publicly_accessible = false 
  multi_az = false ## the databse will be updated in only one !

  ## Additional security and what happens when the RDS is deleted 
  backup_retention_period = 1 ## If exceeding then 1 day the backup will be erased 
  skip_final_snapshot = true ##  Do not create a final database backup when deleting the instance
  deletion_protection = false ## Allowing the instance to be deleted, if it were set to "true" then aws will prevent deletion from the terraform or cli marking it as accidential 


  ### The above deleteion process is set up in a way to save expensees, the industry standard is exactly opposite !
}

### Outputs after the terraform instance is created 

output "rds_endpoint" {
  value = aws_db_instance.pg.address ## This returns the database's hostname, the application uses this address toknow which databse server to connect to 
}
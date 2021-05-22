terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = "us-west-2"
}

variable "allowed_ip" {
  type = string
}

resource "aws_vpc" "test_kitchen" {
  # Randomly generated RFC1918 subnets are less likely to conflict if you have future VPN needs
  # https://www.marmot.org.uk/1918.pl?pfxlen=24
  # This is hardcoded, not re-randomized, and that's fine here. https://xkcd.com/221/
  cidr_block           = "10.193.71.0/24"
  enable_dns_hostnames = true

  tags = {
    Name = "Test Kitchen"
  }
}

resource "aws_subnet" "test_kitchen" {
  vpc_id                  = aws_vpc.test_kitchen.id
  cidr_block              = "10.193.71.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "tf_test_subnet"
  }
}

output "test_kitchen_subnet" {
  value = aws_subnet.test_kitchen.id
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.test_kitchen.id

  tags = {
    Name = "Test Kitchen"
  }
}

resource "aws_route_table" "test_kitchen" {
  vpc_id = aws_vpc.test_kitchen.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "Test Kitchen"
  }
}

resource "aws_route_table_association" "test_kitchen" {
  subnet_id      = aws_subnet.test_kitchen.id
  route_table_id = aws_route_table.test_kitchen.id
}

resource "aws_security_group" "test_kitchen" {
  name        = "test_kitchen"
  description = "Used by Test Kitchen for RSpec integration tests"
  vpc_id      = aws_vpc.test_kitchen.id

  tags = {
    Name = "Test Kitchen"
  }

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.allowed_ip}/32"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "test_kitchen_sg" {
  value = aws_security_group.test_kitchen.id
}

resource "aws_key_pair" "test_kitchen" {
  key_name   = "test-kitchen"
  public_key = file("../id_rsa.pub")
}

output "key_pair_id" {
  value = aws_key_pair.test_kitchen.id
}

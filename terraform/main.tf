provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags = merge(var.tags, {
    Name = "main-vpc"
  })
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = merge(var.tags, {
    Name = "main-igw"
  })
}

# Public Subnets
resource "aws_subnet" "public_subnets" {
  for_each = { for idx, cidr in var.public_subnets : idx => cidr }

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = element(var.availability_zones, each.key)
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "public-subnet-${each.key}"
  })
}

# Private Subnets
resource "aws_subnet" "private_subnets" {
  for_each = { for idx, cidr in var.private_subnets : idx => cidr }

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = element(var.availability_zones, each.key)

  tags = merge(var.tags, {
    Name = "private-subnet-${each.key}"
  })
}

# Databasse Subnets
resource "aws_subnet" "databases_subnets" {
  for_each = { for idx, cidr in var.database_subnets : idx => cidr }

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = element(var.availability_zones, each.key)

  tags = merge(var.tags, {
    Name = "databases-subnet-${each.key + 1}"
  })
}

# Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(var.tags, {
    Name = "public-route-table"
  })
}

# Route Table Associations for Public Subnets
resource "aws_route_table_association" "public_subnets" {
  for_each = aws_subnet.public_subnets

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

# NAT Gateway
resource "aws_eip" "nat" {
  count = length(var.public_subnets)

  vpc = true
  tags = merge(var.tags, {
    Name = "nat-eip-${count.index + 1}"
  })
}

resource "aws_nat_gateway" "nat" {
  count = length(var.public_subnets)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public_subnets[count.index].id

  tags = merge(var.tags, {
    Name = "nat-gateway-${count.index + 1}"
  })
}

# Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat[0].id
  }

  tags = merge(var.tags, {
    Name = "private-route-table"
  })
}

# Route Table Associations for Private Subnets
resource "aws_route_table_association" "private_subnets" {
  for_each = aws_subnet.private_subnets

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

# Security Group - Allow All Traffic (for example purposes)
resource "aws_security_group" "allow_all" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "allow-all-sg"
  })
}

# Outputs
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnets" {
  value = aws_subnet.public_subnets[*].id
}

output "private_subnets" {
  value = aws_subnet.private_subnets[*].id
}

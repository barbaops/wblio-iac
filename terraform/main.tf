resource "aws_vpc" "main" {
  cidr_block            = var.cidr_block
  enable_dns_hostnames  = true
  enable_dns_support    = true

  tags = {
    Name    = var.project
    Project = var.project
    Region  = var.region
  }
}

resource "aws_subnet" "subnets" {
  for_each = var.subnets

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr_block
  availability_zone = format("%s%s", var.region, each.value.availability_zone)

  tags = {
    Name    = format("%s-%s", var.region, each.key)
    Project = var.project
    Region  = var.region
  }
}

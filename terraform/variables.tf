variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "project" {
  description = "Project name for tagging"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "subnets" {
  description = "Subnet configurations"
  type = map(object({
    cidr_block         = string
    availability_zone  = string
  }))
  default = {
    "private-1a"  = { cidr_block = "10.0.0.0/20",   availability_zone = "a" }
    "private-1b"  = { cidr_block = "10.0.16.0/20",  availability_zone = "b" }
    "private-1c"  = { cidr_block = "10.0.32.0/20",  availability_zone = "c" }
    "public-1a"   = { cidr_block = "10.0.48.0/24",  availability_zone = "a" }
    "public-1b"   = { cidr_block = "10.0.49.0/24",  availability_zone = "b" }
    "public-1c"   = { cidr_block = "10.0.50.0/24",  availability_zone = "c" }
    "database-1a" = { cidr_block = "10.0.51.0/24",  availability_zone = "a" }
    "database-1b" = { cidr_block = "10.0.52.0/24",  availability_zone = "b" }
    "database-1c" = { cidr_block = "10.0.53.0/24",  availability_zone = "c" }
  }
}
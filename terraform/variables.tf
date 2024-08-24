variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnets" {
  description = "List of CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.0.0/20", "10.0.16.0/20", "10.0.32.0/20"]
}

variable "public_subnets" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.48.0/24", "10.0.49.0/24", "10.0.50.0/24"]
}

variable "database_subnets" {
  description = "List of CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.51.0/20", "10.0.52.0/20", "10.0.53.0/20"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "tags" {
  description = "A map of tags to assign to resources"
  type        = map(string)
  default     = {
    "Environment" = "dev"
    "Team"        = "DevOps"
  }
}

variable "nat_gateway_enabled" {
  description = "Enable or disable the NAT Gateway"
  type        = bool
  default     = true
}

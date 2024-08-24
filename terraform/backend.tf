terraform {
  backend "s3" {
    bucket      = "wblio-tf-state"
    key         = "vpc/state"
    region      = "us-east-1"
  }
}
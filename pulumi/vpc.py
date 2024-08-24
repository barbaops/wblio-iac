import pulumi
import pulumi_aws as aws

# Variáveis de entrada
project_name = pulumi.Config().require("project_name")
region = pulumi.Config().require("region")
cidr_block = pulumi.Config().require("cidr_block")

subnets = {
    "private-1a":  {"cidr_block": "10.0.0.0/20",   "availability_zone": "a"},
    "private-1b":  {"cidr_block": "10.0.16.0/20",  "availability_zone": "b"},
    "private-1c":  {"cidr_block": "10.0.32.0/20",  "availability_zone": "c"},
    "public-1a":   {"cidr_block": "10.0.48.0/24",  "availability_zone": "a"},
    "public-1b":   {"cidr_block": "10.0.49.0/24",  "availability_zone": "b"},
    "public-1c":   {"cidr_block": "10.0.50.0/24",  "availability_zone": "c"},
    "database-1a": {"cidr_block": "10.0.51.0/24",  "availability_zone": "a"},
    "database-1b": {"cidr_block": "10.0.52.0/24",  "availability_zone": "b"},
    "database-1c": {"cidr_block": "10.0.53.0/24",  "availability_zone": "c"}
}

# Criando VPC
vpc = aws.ec2.Vpc("main",
    cidr_block=cidr_block,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": project_name,
        "Project": project_name,
        "Region": region
    }
)

# Criando Subnets
for name, subnet in subnets.items():
    aws.ec2.Subnet(name,
        vpc_id=vpc.id,
        cidr_block=subnet["cidr_block"],
        availability_zone=f"{region}{subnet['availability_zone']}",
        tags={
            "Name": f"{region}-{name}",
            "Project": project_name,
            "Region": region
        }
    )

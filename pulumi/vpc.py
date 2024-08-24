import pulumi
import pulumi_aws as aws

vpc_cidr = "10.0.0.0/16
private_subnets = ["10.0.0.0/20", "10.0.16.0/20", "10.0.32.0/20"]
public_subnets = ["10.0.48.0/24", "10.0.49.0/24", "10.0.50.0/24"]
database_subnets = ["10.0.51.0/24", "10.0.52.0/24", "10.0.53.0/24"]
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
tags = {"Environment": "dev", "Team": "DevOps"}
nat_gateway_enabled = True

vpc = aws.ec2.Vpc(
    "main-vpc",
    cidr_block=vpc_cidr,
    tags={**tags, "Name": "main-vpc"}
)

igw = aws.ec2.InternetGateway(
    "main-igw",
    vpc_id=vpc.id,
    tags={**tags, "Name": "main-igw"}
)

public_subnets_resources = []
for i, cidr in enumerate(public_subnets):
    subnet = aws.ec2.Subnet(
        f"public-subnet-{i+1}",
        vpc_id=vpc.id,
        cidr_block=cidr,
        availability_zone=availability_zones[i],
        map_public_ip_on_launch=True,
        tags={**tags, "Name": f"public-subnet-{i+1}"}
    )
    public_subnets_resources.append(subnet)

private_subnets_resources = []
for i, cidr in enumerate(private_subnets):
    subnet = aws.ec2.Subnet(
        f"private-subnet-{i+1}",
        vpc_id=vpc.id,
        cidr_block=cidr,
        availability_zone=availability_zones[i],
        tags={**tags, "Name": f"private-subnet-{i+1}"}
    )
    private_subnets_resources.append(subnet)

public_route_table = aws.ec2.RouteTable(
    "public-route-table",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "gateway_id": igw.id,
    }],
    tags={**tags, "Name": "public-route-table"}
)

for i, subnet in enumerate(public_subnets_resources):
    aws.ec2.RouteTableAssociation(
        f"public-subnet-{i+1}-rta",
        subnet_id=subnet.id,
        route_table_id=public_route_table.id
    )

nat_gateway = None
if nat_gateway_enabled:
    nat_eips = []
    nat_gateways = []
    for i, subnet in enumerate(public_subnets_resources):
        eip = aws.ec2.Eip(f"nat-eip-{i+1}", vpc=True, tags={**tags, "Name": f"nat-eip-{i+1}"})
        nat_gateway = aws.ec2.NatGateway(
            f"nat-gateway-{i+1}",
            allocation_id=eip.id,
            subnet_id=subnet.id,
            tags={**tags, "Name": f"nat-gateway-{i+1}"}
        )
        nat_gateways.append(nat_gateway)
        nat_eips.append(eip)

    private_route_table = aws.ec2.RouteTable(
        "private-route-table",
        vpc_id=vpc.id,
        routes=[{
            "cidr_block": "0.0.0.0/0",
            "nat_gateway_id": nat_gateways[0].id,
        }],
        tags={**tags, "Name": "private-route-table"}
    )

    for i, subnet in enumerate(private_subnets_resources):
        aws.ec2.RouteTableAssociation(
            f"private-subnet-{i+1}-rta",
            subnet_id=subnet.id,
            route_table_id=private_route_table.id
        )

sg = aws.ec2.SecurityGroup(
    "allow-all-sg",
    vpc_id=vpc.id,
    ingress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
    tags={**tags, "Name": "allow-all-sg"}
)

pulumi.export("vpc_id", vpc.id)
pulumi.export("public_subnets", [subnet.id for subnet in public_subnets_resources])
pulumi.export("private_subnets", [subnet.id for subnet in private_subnets_resources])
pulumi.export("databases_subnets", [subnet.id for subnet in databases_subnets_resources])

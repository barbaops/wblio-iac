import boto3
import logging
from models import VPCRequest

# Configuração do log
logger = logging.getLogger(__name__)

def create_vpc_and_subnets(request: VPCRequest):
    ec2 = boto3.client('ec2', region_name=request.region)

    # Verifica se a VPC já existe com o mesmo CIDR block
    existing_vpcs = ec2.describe_vpcs(Filters=[{'Name': 'cidr-block', 'Values': [request.cidr_block]}])
    if existing_vpcs['Vpcs']:
        vpc_id = existing_vpcs['Vpcs'][0]['VpcId']
        logger.info(f"VPC já existente com o CIDR block {request.cidr_block}. ID da VPC: {vpc_id}")
        return f"VPC já existente com o CIDR block {request.cidr_block}. ID da VPC: {vpc_id}"

    # Criação da VPC
    logger.info(f"Criando VPC com CIDR block {request.cidr_block}.")
    response = ec2.create_vpc(
        CidrBlock=request.cidr_block,
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {'Key': 'Name', 'Value': request.project_name},
                    {'Key': 'Project', 'Value': request.project_name},
                    {'Key': 'Region', 'Value': request.region},
                ]
            }
        ]
    )
    vpc_id = response['Vpc']['VpcId']
    logger.info(f"VPC criada com sucesso. ID da VPC: {vpc_id}")

    # Ativando DNS Support e DNS Hostnames
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    logger.info("DNS Support e DNS Hostnames ativados.")

    # Criação das Subnets
    for name, subnet in request.subnets.items():
        subnet_name = f"{request.region}-{name}"
        az = f"{request.region}{subnet['availability_zone']}"
        
        logger.info(f"Criando Subnet {subnet_name} com CIDR block {subnet['cidr_block']}.")
        response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=subnet["cidr_block"],
            AvailabilityZone=az,
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': subnet_name},
                        {'Key': 'Project', 'Value': request.project_name},
                        {'Key': 'Region', 'Value': request.region},
                    ]
                }
            ]
        )
        
        subnet_id = response['Subnet']['SubnetId']
        logger.info(f"Subnet '{subnet_name}' criada com sucesso. ID da Subnet: {subnet_id}")
    
    return "VPC e Subnets criadas com sucesso."

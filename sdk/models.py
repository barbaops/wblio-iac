from pydantic import BaseModel
from typing import Dict

class SubnetConfig(BaseModel):
    cidr_block: str
    availability_zone: str

class VPCRequest(BaseModel):
    project_name: str
    region: str
    cidr_block: str
    subnets: Dict[str, SubnetConfig]

from fastapi import FastAPI, HTTPException
import logging
from aws_services import create_vpc_and_subnets
from models import VPCRequest

# Configuração do log
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/create_vpc")
async def create_vpc(request: VPCRequest):
    try:
        logger.info("Recebendo requisição para criação de VPC e Subnets.")
        result = create_vpc_and_subnets(request)
        return {"message": result}
    except Exception as e:
        logger.error(f"Erro ao criar VPC: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

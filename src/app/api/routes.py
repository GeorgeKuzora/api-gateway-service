from fastapi import APIRouter, Depends

from app.external.clients import clients

auth = APIRouter(
    prefix='/auth',
)
transaction = APIRouter(
    prefix='/transaction',
    dependencies=[Depends(clients.auth_client.check_token)],
)

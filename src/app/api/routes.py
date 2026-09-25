from fastapi import APIRouter, Depends

from app.external.clients import clients

auth = APIRouter(
    prefix='/auth',
    tags=['auth'],
)
transaction = APIRouter(
    prefix='/transaction',
    tags=['transaction'],
    dependencies=[Depends(clients.auth_client.check_token)],
)
healthz = APIRouter(prefix='/healthz', tags=['healthz'])

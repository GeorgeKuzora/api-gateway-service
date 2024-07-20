from fastapi import APIRouter, Depends

from app.external.clients import clients

auth = APIRouter(
    prefix='/auth',
)
register = APIRouter(
    prefix='/register',
)
transaction = APIRouter(
    prefix='/transaction',
    dependencies=[Depends(clients.auth_client.check_token)],
)
report = APIRouter(
    prefix='/report',
    dependencies=[Depends(clients.auth_client.check_token)],
)

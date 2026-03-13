from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
import os
import sys
import inspect
# import requests

router = APIRouter()
@router.get("/secure-data")

def securedata(request: Request):
    response = request.get('http://localhost:8000/secure-data')
    # print(type(request.query_params.get('name')))
    # return type(request.query_params)
    # print(dir(set))
    # print(dir(os.__dir__))
    # print(sys.getsizeof(request.headers))
    a = 12345678
    # print(hasattr(Request, 'path_params'))
    # print(os.__class__)
    # print(sys.thread_info)
    # print(help(request.client))
    # print(request.headers)
    # print(dir(request.client))
    print(request.client.host)
    api_key = request.headers.get('X-API-key', None)
    if ( 'X-API-key' in request.headers):
        print(" api key is "+api_key)
        # return 'header exists'
        if (api_key == 'admin123'):
            return 'Api key is valid'
        else:
            return 'Invalid API key'
    else:
        return 'header not exists'
    return request.headers
from datetime import date
from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
from typing import Optional
from fastapi import Query
import ast
import json

router=APIRouter(prefix="/paymentTransactionHistory",tags=['paymentTransactionHistory'])

@router.get('')
def getPaymentTransactionHistory(fromDate:Optional[date]=Query(None), toDate:Optional[date]=Query(None),paymentType:Optional[int]=Query(None),branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[getPaymentTransactionHistory] ?,?,?,?""",(fromDate, toDate,paymentType,branchId))  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
       
        return {"statusCode": 0,"response": str(e)}
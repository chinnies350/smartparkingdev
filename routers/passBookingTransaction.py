from fastapi.routing import APIRouter
import schemas
from routers import Response
from routers.config import engine
from joblib import Parallel, delayed
import json
from typing import Optional
from fastapi import Query

router=APIRouter(prefix="/passBookingTransaction",tags=['passBookingTransaction'])

@router.get('')
def getpassbookingtransaction(passBookingTransactionId:Optional[int]=Query(None), userId:Optional[str]=Query(None), type:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute("EXEC [dbo].[getPassBookingTransaction] ?,?,?",(passBookingTransactionId, userId, type))
            rows= result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")
    except Exception as e:
        return {"statusCode":0,"response":str(e)}
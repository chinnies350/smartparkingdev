from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix='/cancellationDetails',tags=['cancellationDetails'])

@router.get('')
def getCancellationRefundCharges(bookingId:int):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getCancellationRefundCharges] ?""",bookingId)  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putCancellation(request:schemas.cancellationupdate):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putcancellation]
                                    @refundStatus=?,
                                    @cancellationCharges=?,
                                    @cancellationReason=?,
                                    @updatedBy=?,
                                    @bookingId=?""",
                                    (request.refundStatus,
                                    request.cancellationCharges,
                                    request.cancellationReason,
                                    request.updatedBy,
                                    request.bookingId))
            rows=result.fetchall()
            return{"statusCode":int(rows[0][1]),"response":rows[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

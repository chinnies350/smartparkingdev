from optparse import Option
from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import ast
import json

router=APIRouter(prefix="/paymentUPIDetails",tags=['paymentUPIDetails'])

@router.get('')
def getPaymentUPIDetails(paymentUPIDetailsId:Optional[int]=Query(None), branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getPaymentUPIDetails] ?,?""",(paymentUPIDetailsId, branchId))  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
       
        return {"statusCode": 0,"response": str(e)}

@router.post('')
def postPaymentUPIDetails(request:schemas.PaymentUPIDetails):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postPaymentUPIDetails]
                                                @name =?,
                                                @phoneNumber =?,
                                                @UPIId =?,
                                                @branchId =?,
                                                @merchantId =?,
                                                @merchantCode=?,
                                                @mode=?,
                                                @orgId=?,
                                                @sign=?,
                                                @url=?,
                                                @activeStatus =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.name,
                                            request.phoneNumber,
                                            request.UPIId,
                                            request.branchId,
                                            request.merchantId,
                                            request.merchantCode,
                                            request.mode,
                                            request.orgId,
                                            request.sign,
                                            request.url,
                                            request.activeStatus,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception as postPaymentUPIDetails ",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putPaymentUPIDetails(request:schemas.PutPaymentUPIDetails):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putPaymentUPIDetails]
                                                @name =?,
                                                @phoneNumber =?,
                                                @UPIId =?,
                                                @branchId =?,
                                                @merchantId =?,
                                                @merchantCode=?,
                                                @mode=?,
                                                @orgId=?,
                                                @sign=?,
                                                @url=?,
                                                @updatedBy= ?,
                                                @paymentUPIDetailsId=?
                                                
                                                """,
                                            (request.name,
                                            request.phoneNumber,
                                            request.UPIId,
                                            request.branchId,
                                            request.merchantId,
                                            request.merchantCode,
                                            request.mode,
                                            request.orgId,
                                            request.sign,
                                            request.url,
                                            request.updatedBy,
                                            request.paymentUPIDetailsId
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.delete('')
def deleteparkingSlot(paymentUPIDetailsId:int,activestatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE paymentUPIDetails SET activestatus=? Where paymentUPIDetailsId=?",activestatus,paymentUPIDetailsId)
            result.close()
            if result.rowcount>=1:
                if activestatus=='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import ast
import json

router=APIRouter(prefix='/subscriptionMaster',tags=['subscriptionMaster'])


@router.get('')
def getSubscriptionMaster(subscriptionId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getsubscripitionMaster] ?,?""",subscriptionId,activeStatus)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")  

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode": 0,"response":"Server Error"}



@router.post('')
def postSubscriptionMaster(request:schemas.SubscriptionMaster):
    try:
        with engine.connect() as  cur:
            result=cur.execute(f"""EXEC [dbo].[postsubscriptionMaster]
                                    @subscriptionName=?,
                                    @validity=?,
                                    @offerType=?,
                                    @offerValue=?,
                                    @parkingLimit=?,
                                    @rules=?,
                                    @taxId=?,
                                    @totalAmount=?,
                                    @validityFrom=?,
                                    @validityTo=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                                (
                                request.subscriptionName,
                                request.validity,
                                request.offerType,
                                request.offerValue,
                                request.parkingLimit,
                                request.rules,
                                request.taxId,
                                request.totalAmount,
                                request.validityFrom,
                                request.validityTo,
                                request.activeStatus,
                                request.createdBy,
                                ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode": 0,"response":"Server Error"}


@router.put('')
def putSubscriptionMaster(request:schemas.PutSubscriptionMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f""" EXEC [dbo].[putsubscriptionMaster]
                                    @subscriptionName=?,
                                    @validity=?,
                                    @offerType=?,
                                    @offerValue=?,
                                    @parkingLimit=?,
                                    @rules=?,
                                    @totalAmount=?,
                                    @validityFrom=?,
                                    @validityTo=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @subscriptionId=?,
                                    @taxId=?""",
                                (request.subscriptionName,
                                request.validity,
                                request.offerType,
                                request.offerValue,
                                request.parkingLimit,
                                request.rules,     
                                request.totalAmount,
                                request.validityFrom,
                                request.validityTo,
                                request.activeStatus,
                                request.updatedBy,
                                request.subscriptionId,
                                request.taxId))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statuscode":0,"response":"Server Error"}



@router.delete('')
def deleteSubscriptionMaster(subscriptionId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE subscriptionMaster SET activeStatus=? WHERE subscriptionId=?",activeStatus,subscriptionId)
            result.close()
            if result.rowcount>=1:
                if activeStatus=='D':
                   return Response("deactiveMsg")
                else:
                   return Response("ActiveMsg")
            else:
                return Response("NotFound")
    
    except Exception as e:
        print("Exception Error",str(e))
        return {"statuscode":0,"response":"Server Error"}
        







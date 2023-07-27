from unittest import result
from fastapi.routing import APIRouter
from requests import request
from routers.config import engine
from routers import Response
import schemas
from datetime import date,time
from fastapi import Query
from typing import Optional
import json
from joblib import Parallel, delayed
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS

router=APIRouter(prefix='/offerMaster',tags=['offerMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
def getofferMaster(userId:Optional[int]=Query(None), Amount:Optional[str]=Query(None), fromDate:Optional[date]=Query(None), toDate:Optional[date]=Query(None), fromTime:Optional[time]=Query(None), toTime:Optional[time]=Query(None), branchId:Optional[int]=Query(None), parkingOwnerId:Optional[int]=Query(None), date:Optional[date]=Query(None),offerId:Optional[int]=Query(None),offerTypePeriod:Optional[str]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getofferMaster] ?,?,?,?,?,?,?,?,?,?,?,?""",userId,Amount,fromDate,toDate,fromTime,toTime,branchId, parkingOwnerId,date,offerId,offerTypePeriod,activeStatus)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")
            

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postofferMaster(request:schemas.offerMaster):
    try:
        with engine.connect() as cur:
            r = None
            if request.offerRulesDetails!=None:
                r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.offerRulesDetails)
            else:
                r=None
            result=cur.execute(f"""EXEC [dbo].[postofferMaster]
                                    @offerTypePeriod=?,
                                    @offerHeading=?,
                                    @offerDescription=?,
                                    @offerCode=?,
                                    @offerImageUrl=?,
                                    @fromDate=?,
                                    @toDate=?,
                                    @fromTime=?,
                                    @toTime=?,
                                    @offerType=?,
                                    @offerValue=?,
                                    @minAmt=?,
                                    @maxAmt=?,
                                    @noOfTimesPerUser=?,
                                    
                                    @activeStatus=?,
                                    @createdBy=?,
                                    @offerRulesDetailsJson=?""",
                                    
                                    (request.offerTypePeriod,
                                    request.offerHeading,
                                    request.offerDescription,
                                    request.offerCode,
                                    request.offerImageUrl,
                                    request.fromDate,
                                    request.toDate,
                                    request.fromTime,
                                    request.toTime,
                                    request.offerType,
                                    request.offerValue,
                                    request.minAmt,
                                    request.maxAmt,
                                    request.noOfTimesPerUser,
                                    
                                    request.activeStatus,
                                    request.createdBy,
                                    json.dumps(r,indent=4, sort_keys=True, default=str) if r else None))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putofferMaster(request:schemas.putofferMaster):
    try:
        with engine.connect() as cur:
            if request.offerRulesDetails!=None:
                r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.offerRulesDetails)
                r=json.dumps(r,indent=4, sort_keys=True, default=str)
            else:
                r=None
            result=cur.execute("""EXEC [dbo].[putofferMaster]
                                    @offerId=?,
                                    @offerTypePeriod=?,
                                    @offerHeading=?,
                                    @offerDescription=?,
                                    @offerCode=?,
                                    @offerImageUrl=?,
                                    @fromDate=?,
                                    @toDate=?,
                                    @fromTime=?,
                                    @toTime=?,
                                    @offerType=?,
                                    @offerValue=?,
                                    @minAmt=?,
                                    @maxAmt=?,
                                    @noOfTimesPerUser=?,
                                    
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @offerRulesDetailsJson=?""",
                                    
                                    (request.offerId,
                                    request.offerTypePeriod,
                                    request.offerHeading,
                                    request.offerDescription,
                                    request.offerCode,
                                    request.offerImageUrl,
                                    request.fromDate,
                                    request.toDate,
                                    request.fromTime,
                                    request.toTime,
                                    request.offerType,
                                    request.offerValue,
                                    request.minAmt,
                                    request.maxAmt,
                                    request.noOfTimesPerUser,
                                    
                                    request.activeStatus,
                                    request.updatedBy,
                                    r))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteofferMaster(activeStatus:str,offerId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE offerMaster SET activeStatus=? WHERE offerId=?",activeStatus,offerId)
            result.close()
            if result.rowcount >=1:
                if activeStatus=='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

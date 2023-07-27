from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from fastapi import Query
from typing import Optional
import ast
from  routers import Response
import json

router=APIRouter(prefix='/shiftMaster',tags=['shiftMaster'])

@router.get('')
def getshiftMaster(shiftId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),activestatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getshiftMaster] ?,?,?,?""",shiftId,parkingOwnerId,branchId,activestatus)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postshiftMaster(request:schemas.shiftMaster):
    try:
        # createdDate=datetime.datetime.now()
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postshiftMaster]
                                    @parkingOwnerId=?,
                                    @branchId=?,
                                    @shiftName=?,
                                    @startTime=?,
                                    @endTime=?,
                                    @breakStartTime=?,
                                    @breakEndTime=?,
                                    @gracePeriod=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                                    (request.parkingOwnerId,
                                    request.branchId,
                                    request.shiftName,
                                    request.startTime,
                                    request.endTime,
                                    request.breakStartTime,
                                    request.breakEndTime,
                                    request.gracePeriod,
                                    request.activeStatus,
                                    request.createdBy))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}               
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')
def putshiftMaster(request:schemas.putshiftMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putshiftMaster] 
                                    @shiftName=?,
                                    @startTime=?,
                                    @endTime=?,
                                    @breakStartTime=?,
                                    @breakEndTime=?,
                                    @gracePeriod=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @shiftId=?,
                                    @parkingOwnerId=?,
                                    @branchId=?""",
                                    (request.shiftName,
                                    request.startTime,
                                    request.endTime,
                                    request.breakStartTime,
                                    request.breakEndTime,
                                    request.gracePeriod,
                                    request.activeStatus,
                                    request.updatedBy,
                                    request.shiftId,
                                    request.parkingOwnerId,
                                    request.branchId))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}    

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}



@router.delete('')     
def deleteShiftmaster(shiftId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""UPDATE shiftMaster SET activeStatus=? WHERE shiftId=?""",(activeStatus,shiftId))
            if result.rowcount>=1:
                if activeStatus=="D":
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

   


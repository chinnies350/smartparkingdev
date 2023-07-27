from fastapi.routing import APIRouter
import schemas
from routers.config import engine
import json
from routers import Response
from typing import Optional
from fastapi import Query

router=APIRouter(prefix="/branchWorkingHrs",tags=['branchWorkingHrs'])

@router.get('')
def getBranchWorkingHrs(branchId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None)):
    try:
      with engine.connect() as cur:
          result=cur.execute(f"""EXEC [dbo].[getBranchWorkingHrs] ?,?""",(branchId,parkingOwnerId))
          rows=result.fetchone()
          result.close()
          if rows[0]:
            return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
          else:
            return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.post('')
def postBranchWorkingHrs(request:schemas.BranchWorkingHrs):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postBranchWorkingHrs]
                                            @branchId =?,
                                            @parkingOwnerId =?,
                                            @workingDay =?,
                                            @fromTime =?,
                                            @toTime =?,
                                            @isHoliday =?,
                                            @createdBy =?""",
                                            (
                                            request.branchId,
                                            request.parkingOwnerId,
                                            request.workingDay,
                                            request.fromTime,
                                            request.toTime,
                                            request.isHoliday,
                                            request.createdBy))
            rows=result.fetchall()
            return{"statusCode":int(rows[0][1]),"response":rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.put('')
def putbranchWorkingHrs(request:schemas.PutBranchWorkingHrs):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putBranchWorkingHrs]
                                            @uniqueId=?,
                                            @branchId =?,
                                            @parkingOwnerId =?,
                                            @workingDay =?,
                                            @fromTime =?,
                                            @toTime =?,
                                            @isHoliday =?,
                                            @updatedBy =?""",
                                            (
                                            request.uniqueId,
                                            request.branchId,
                                            request.parkingOwnerId,
                                            request.workingDay,
                                            request.fromTime,
                                            request.toTime,
                                            request.isHoliday,
                                            request.updatedBy))
            rows=result.fetchall()
            return{"statusCode":int(rows[0][1]),"response":rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
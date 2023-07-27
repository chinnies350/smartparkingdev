from fastapi.routing import APIRouter
import schemas
from datetime import datetime
from routers import Response
from routers.config import engine
import json
from typing import Optional
from fastapi import Query

router=APIRouter(prefix="/parkingOwnerMaster",tags=['parkingOwnerMaster'])

@router.get('')
def getParkingOwnerMaster(userId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),type:Optional[str]=Query(None),city:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getParkingOwnerMaster] ?,?,?,?,?""",(userId,parkingOwnerId,activeStatus,type,city))
            rows = result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound") 

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

# @router.post('')
# def postParkingOwnerMaster(request:schemas.ParkingOwnerMaster):
#     try:
#         with engine.connect() as cur:
#             result=cur.execute(f"""EXEC [dbo].[postParkingOwnerMaster]
#                                         @parkingName=?,
#                                         @shortName=?,
#                                         @founderName=?,
#                                         @logoUrl=?,
#                                         @websiteUrl=?,
#                                         @gstNumber=?,
#                                         @placeType=?,
#                                         @activeStatus=?,
#                                         @createdBy=?
#                             """,
#                             (request.parkingName,
#                             request.shortName,
#                             request.founderName,
#                             request.logoUrl,
#                             request.websiteUrl,
#                             request.gstNumber,
#                             request.placeType,
#                             request.activeStatus,
#                             request.createdBy))
#             row=result.fetchall()
#             return {"statusCode": int(row[0][1]), "response": row[0][0]}
#     except Exception as e:
#         return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putParkingOwnerMaster(request:schemas.PutParkingOwnerMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putParkingOwnerMaster]
                                        @parkingOwnerId=?,
                                        @userId=?,
                                        @parkingName=?,
                                        @shortName=?,
                                        @founderName=?,
                                        @logoUrl=?,
                                        @websiteUrl=?,
                                        @gstNumber=?,
                                        @placeType=?,
                                        @updatedBy=?
                                """,
                                (request.parkingOwnerId,
                                request.userId,
                                request.parkingName,
                                request.shortName,
                                request.founderName,
                                request.logoUrl,
                                request.websiteUrl,
                                request.gstNumber,
                                request.placeType,
                                request.updatedBy))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
                                       
@router.delete('')
def deleteParkingOwnerMaster(parkingOwnerId:int,userId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""UPDATE parkingOwnerMaster SET activeStatus=? WHERE parkingOwnerId=? AND userId=?""",activeStatus,parkingOwnerId,userId)
            result.close()
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


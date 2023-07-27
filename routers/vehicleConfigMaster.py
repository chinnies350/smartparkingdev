from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import ast,json

router=APIRouter(prefix='/vehicleConfigMaster',tags=['vehicleConfigMaster'])

@router.get('')
def getvehicleConfigMaster(vehicleConfigId:Optional[int]=Query(None),vehicleName:Optional[str]=Query(None),activeStatus:Optional[str]=Query(None),floorId:Optional[int]=Query(None), branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getvehicleConfigMaster] ?,?,?,?,?""",vehicleConfigId,vehicleName,activeStatus,floorId, branchId)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.post('')
def postvehicleConfigMaster(request:schemas.VehicleConfigMaster):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[postvehicleConfigMaster]
                                    @vehicleName=?,
                                    @vehicleImageUrl=?,
                                    @vehiclePlaceHolderImageUrl=?,
                                    @vehicleKeyName=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                                    (request.vehicleName,
                                    request.vehicleImageUrl,
                                    request.vehiclePlaceHolderImageUrl,
                                    request.vehicleKeyName,
                                    request.activeStatus,
                                    request.createdBy))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')
def putvehicleConfigMaster(request:schemas.PutVehicleConfigMaster):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[putvehicleConfigMaster]
                                   @vehicleName=?,
                                   @vehicleImageUrl=?,
                                   @vehiclePlaceHolderImageUrl=?,
                                   @vehicleKeyName=?,
                                   @updatedBy=?,
                                   @vehicleConfigId=?""",
                                   (request.vehicleName,
                                   request.vehicleImageUrl,
                                   request.vehiclePlaceHolderImageUrl,
                                   request.vehicleKeyName,
                                   request.updatedBy,
                                   request.vehicleConfigId))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}



@router.delete('')
def deletevehicleConfigMaster(vehicleConfigId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE vehicleConfigMaster SET activeStatus=? WHERE vehicleConfigId=?",activeStatus,vehicleConfigId)
            result.close()
            if result.rowcount>=1:
                if activeStatus=='D':
                   return Response("deactiveMsg")
                else:
                   return Response("ActiveMsg")
            else:
                return Response("NotDelete")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}




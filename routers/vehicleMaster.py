from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router= APIRouter(prefix=('/vehicleMaster'),tags=['vehicleMaster'])

@router.get('')
def getvehicleMaster(vehicleId:Optional[int]=Query(None),userId:Optional[int]=Query(None), vehicleType:Optional[int]=Query(None), phoneNumber:Optional[str]=Query(None)):
    try:
        with engine.connect() as  cur:
            result=cur.execute("EXEC [dbo].[getVehicleMaster] ?,?,?,?",vehicleId,userId,vehicleType,phoneNumber)
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
def postvehicleMaster(request:schemas.vehicleMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postvehicleMaster]
                                    @userId=?,
                                    @vehicleName=?,
                                    @vehicleNumber=?,
                                    @vehicleType=?,
                                    @insuranceValidity=?,
                                    @vehicleImageUrl=?,
                                    @documentImageUrl=?,
                                    @isEV=?,
                                    @chargePinType=?""",
                                (request.userId,
                                request.vehicleName,
                                request.vehicleNumber,
                                request.vehicleType,
                                request.insuranceValidity,
                                request.vehicleImageUrl,
                                request.documentImageUrl,
                                request.isEV,
                                request.chargePinType,
                              ))

            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putvehicleMaster(request:schemas.PutvehicleMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putvehicleMaster]
                                    @vehicleName=?,
                                    @vehicleNumber=?,
                                    @vehicleType=?,
                                    @insuranceValidity=?,
                                    @vehicleImageUrl=?,
                                    @documentImageUrl=?,
                                    @isEV=?,
                                    @chargePinType=?,
                                    @vehicleId=?,
                                    @userId=?""",
                            (request.vehicleName,
                            request.vehicleNumber,
                            request.vehicleType,
                            request.insuranceValidity,
                            request.vehicleImageUrl,
                            request.documentImageUrl,
                            request.isEV,
                            request.chargePinType,
                            request.vehicleId,
                            request.userId))

            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}


    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.delete('')
def deletevehicleMaster(vehicleId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("DELETE FROM vehicleMaster WHERE vehicleId=?",vehicleId)
            result.close()
            if result.rowcount>=1:
                return Response("deleteMsg")
            else:
                return Response("NotDelete")
                
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}



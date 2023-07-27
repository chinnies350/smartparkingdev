from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/vehicleSizeConfigMaster',tags=['vehicleSizeConfigMaster'])

@router.get('')
def getVehicleSizeConfigMaster(vehicleSizeConfigId:Optional[int]=Query(None),activestatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                f"""EXEC [dbo].[getVehicleSizeConfigMaster] ?,?""",vehicleSizeConfigId,activestatus)  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.post('')
def postVehicleSizeConfigMaster(request:schemas.VehicleSizeConfigMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postVehicleSizeConfigMaster]
                                    @vehicleConfigId =?,
									@modelName =?,
									@length =?,
									@height =?,
									@activeStatus =?,
									@createdBy =?""",
                        (
                            request.vehicleConfigId,
                            request.modelName,
                            request.length,
                            request.height,
                            request.activeStatus,
                            request.createdBy                                                        
                        ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]), "response": row[0][0]}  
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.put('')
def putVehicleSizeConfigMaster(request: schemas.PutVehicleSizeConfigMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putVehicleSizeConfigMaster]
                                    @modelName =?,
									@length =?,
									@height =?,
                                    @updatedBy=?,
                                    @vehicleSizeConfigId=?
                                """,
                                                       
                            request.modelName,
                            request.length,
                            request.height,
                            request.updatedBy ,
                            request.vehicleSizeConfigId
                           
                           )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}                 
        
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
 

@router.delete('')
def deleteVehicleSizeConfigMaster(vehicleSizeConfigId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE vehicleSizeConfigMaster SET activeStatus=? WHERE vehicleSizeConfigId=?",activeStatus,vehicleSizeConfigId) 
            result.close()
            if result.rowcount >= 1:
               if activeStatus=='D':
                   return Response("deactiveMsg")
               else:
                   return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}



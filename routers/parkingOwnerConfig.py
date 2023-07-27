from optparse import Option
from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/parkingOwnerConfig",tags=['parkingOwnerConfig'])

@router.get('')
def getParkingOwnerConfig(parkingOwnerId:Optional[int]=Query(None), branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getParkingOwnerConfig] ?,?""",(parkingOwnerId, branchId))  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
       
        return {"statusCode": 0,"response": str(e)}

@router.post('')
def postParkingOwnerConfig(request:schemas.PostParkingOwnerConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postParkingOwnerConfig]
                                                @parkingOwnerId =?,
										@branchId =?,
                                        @blockOption=?,
                                        @floorOption =?,
                                        @squareFeet=?,
                                        @floorType=?,
                                        @employeeOption =?,
                                        @slotsOption=?,
                                        @createdBy =?
                                                
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.blockOption,
                                            request.floorOption,
                                            request.squareFeet,
                                            request.floorType,
                                            request.employeeOption,
                                            request.slotsOption,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception as postParkingOwnerConfig ",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putParkingOwnerConfig(request:schemas.PutParkingOwnerConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putParkingOwnerConfig]
                                                @parkingOwnerConfigId=?,
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @blockOption=?,
                                                @floorOption =?,
                                                @squareFeet=?,
                                                @floorType=?,
                                                @employeeOption =?,
                                                @slotsOption=?,
                                                @updatedBy= ?
                                                
                                                """,
                                            (request.parkingOwnerConfigId,
                                            request.parkingOwnerId,
                                            request.branchId,
                                            request.blockOption,
                                            request.floorOption,
                                            request.squareFeet,
                                            request.floorType,
                                            request.employeeOption,
                                            request.slotsOption,
                                            request.updatedBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}



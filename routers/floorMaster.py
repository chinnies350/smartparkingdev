from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
from fastapi import Query
import json
from joblib import Parallel, delayed
from typing import Optional

router = APIRouter(prefix='/floorMaster',tags=['floorMaster'])
def callFunction(i):
    return i.dict()


@router.get('')
def getfloorMaster(floorId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),blockId:Optional[int]=Query(None),floorName:Optional[int]=Query(None),floorType:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None), type:Optional[str]=Query(None), vehicleType:Optional[int]=Query(None),configId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getFloorMaster] ?,?,?,?,?,?,?,?,?,?""",floorId,parkingOwnerId,branchId,blockId,floorName,floorType,activeStatus, type, vehicleType,configId)
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
def postfloorMaster(request:schemas.FloorMaster):
    try:
        with engine.connect() as cur:
            
            if request.floorVehicleMasterDetails!=None:
                floorVehicleMasterJson = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.floorVehicleMasterDetails)
                floorVehicleMasterJson=json.dumps(floorVehicleMasterJson)
            else:
                
                floorVehicleMasterJson=None
            if request.floorFeaturesDetails!=None:
                floorFeaturesDetailsJson = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.floorFeaturesDetails)
                floorFeaturesDetailsJson=json.dumps(floorFeaturesDetailsJson)
            else:
                floorFeaturesDetailsJson=None
            conn,cur=cursorCommit()
           
            cur.execute(f"""
                        DECLARE @varRes NVARCHAR(400);
                        DECLARE @varStatus NVARCHAR(1);
                        EXEC [dbo].[postFloorMaster] 
                        @parkingOwnerId=?,
                        @branchId=?,
                        @blockId=?,
                        @floorName=?,
                        @floorType=?,
                        @squareFeet=?,
                        @activeStatus=?,
                        @createdBy=?,
                        @floorVehicleMasterJson=?,
                        @floorFeaturesJson=?,
                        @outputVal = @varRes OUTPUT,
                        @outputStatus = @varStatus OUTPUT
                        SELECT @varRes AS varRes,@varStatus AS varStatus
                      """,
                      (request.parkingOwnerId,
                        request.branchId,
                        request.blockId,
                        request.floorName,
                        request.floorType,
                        request.squareFeet,
                        request.activeStatus,
                        request.createdBy,
                        floorVehicleMasterJson,
                        floorFeaturesDetailsJson))
            row=cur.fetchall()
            conn.commit()
            conn.close()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
    
    
@router.put('')
def putfloorMaster(request:schemas.PutFloorMaster):
    try:
        with engine.connect() as cur:
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putfloorMaster] 
                               @floorId=?,
                               @squareFeet=?,
                               @floorName=?,
                               @floorType=?,
                               @activeStatus=?,
                               @updatedBy=?
                               """,
                                (request.floorId,
                                 request.squareFeet,
                                 request.floorName,
                                 request.floorType,
                                 request.activeStatus,
                                 request.updatedBy
                                ))
            row=cur.fetchall()
            conn.commit()
            conn.close()
        
            return {"statusCode": int(row[0][1]), "response": row[0][0]} 

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deletefloorMaster(floorId:int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE floorMaster SET activeStatus=? WHERE floorId=?",activeStatus,floorId) 
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
        return {"statusCode":0,"response":"Server Error"}

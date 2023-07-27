from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
from fastapi import Query
import json
from joblib import Parallel, delayed
from typing import Optional

router = APIRouter(prefix='/floorVehicleMaster',tags=['floorMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
def getfloorVehicleMaster(floorVehicleId:Optional[int]=Query(None),floorId:Optional[int]=Query(None),vehicleType:Optional[int]=Query(None),capacity:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getfloorVehicleMaster] ?,?,?,?,?,?""",floorVehicleId,floorId,vehicleType,capacity,activeStatus,branchId)
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
def postfloorVehicleMaster(request:schemas.PostfloorVehicleMaster):
    try:
        print(request)
        with engine.connect() as cur:
            conn,cur=cursorCommit()
           
            cur.execute(f"""
                        EXEC [dbo].[postfloorVehicleMaster] 
                        @floorId=?,
                        @vehicleType=?,
                        @capacity=?,
                        @length=?,
                        @height=?,
                        @rules=?,
                        @activeStatus=?,
                        @createdBy=?
                   
                      """,
                      (request.floorId,
                        request.vehicleType,
                        request.capacity,
                        request.length,
                        request.height,
                        request.rules,
                        request.activeStatus,
                        request.createdBy
                      ))
            row=cur.fetchall()
            conn.commit()
            conn.close()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putfloorVehicleMaster(request:schemas.PutfloorVehicleMaster):
    try:
        with engine.connect() as cur:
            
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putfloorVehicleMaster] 
                               @floorId=?,
                               @floorVehicleId=?,
                               @vehicleType=?,
                               @capacity=?,
                               @length=?,
                               @height=?,
                               @rules=?,
                              
                               @updatedBy=?
                               """,
                                (
                                 request.floorId,
                                 request.floorVehicleId,
                                 request.vehicleType,
                                 request.capacity,
                                 request.length,
                                 request.height,
                                 request.rules,
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
def deletefloorVehicleMaster(floorVehicleId:int,activeStatus:str):
    try:
       with engine.connect() as cur:
            if activeStatus == 'A':
                result = cur.execute(f"""
                        DECLARE @floorId INT,
                        @vehicleType INT ,
                        @floorVehicleId INT = ?

                        SELECT @floorId = floorId, @vehicleType = vehicleType FROM floorVehicleMaster
                        WHERE floorVehicleId= @floorVehicleId

                        SELECT * FROM floorVehicleMaster
                        WHERE floorId = @floorId AND vehicleType =@vehicleType AND floorVehicleId != @floorVehicleId AND activeStatus = 'A'
               """, (floorVehicleId))
                row = result.fetchone()
                if row != None:
                   return {
                       "statusCode":0,
                       "response": "Data Already Exists"
                   }
            result=cur.execute("UPDATE floorVehicleMaster SET activeStatus=? WHERE floorVehicleId=?",activeStatus,floorVehicleId) 
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
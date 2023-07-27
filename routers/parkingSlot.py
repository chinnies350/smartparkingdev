from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from datetime import datetime,date,time
from fastapi import Query
from typing import Optional
from routers import Response
import ast,json
from joblib import Parallel, delayed

router=APIRouter(prefix='/parkingSlot',tags=['parkingSlot'])

def callFunction(i):
    return i.dict()

@router.get('')
def getparkingSlot(floorId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),parkingLotLineId:Optional[int]=Query(None),typeOfVehicle:Optional[int]=Query(None),laneNumber:Optional[str]=Query(None),fromTime: Optional[time] = Query(None),toTime: Optional[time] = Query(None),fromDate: Optional[date] = Query(None),toDate: Optional[date] = Query(None),type: Optional[str] = Query(None), activeStatus: Optional[str] = Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[getparkingSlot] ?,?,?,?,?,?,?,?,?,?,?""",floorId,branchId,parkingLotLineId,typeOfVehicle,laneNumber,fromTime,toTime,fromDate,toDate,type, activeStatus)
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
def postparkingSlot(request:schemas.parkingSlot):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ParkingSlotDetails)
            result=cur.execute(f""" EXEC [dbo].[postParkingSlot]
                                    @branchId=?,
                                    @blockId=?,
                                    @floorId=?,
                                    @parkingOwnerId=?,
                                    @typeOfVehicle=?,
                                    @noOfRows=?,
                                    @noOfColumns=?,
                                    @passageLeftAvailable=?,
                                    @passageRightAvailable=?,
                                    @typeOfParking=?,
                                    @activeStatus=?,
                                    @createdBy=?,
                                    @parkingSlotDetailsJson=?""",
                                        
                                    (
                                    request.branchId,
                                    request.blockId,
                                    request.floorId,
                                    request.parkingOwnerId,
                                    request.typeOfVehicle,
                                    request.noOfRows,
                                    request.noOfColumns,
                                    request.passageLeftAvailable,
                                    request.passageRightAvailable,
                                    request.typeOfParking,
                                    
                                    request.activeStatus,
                                    request.createdBy,
                                    json.dumps(r,indent=4, sort_keys=True, default=str)
                                    ))
            row=result.fetchall()
            result.close()
            
            return{"statusCode": int(row[0][1]), "response": row[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putparkingSlot(request:schemas.putparkingSlot):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request. ParkingSlotDetailsupdate)
            r=json.dumps(r,indent=4, sort_keys=True, default=str)
            result=cur.execute(f"""EXEC [dbo].[putParkingSlot1]
                                    @parkingLotLineId=?,
                                    @branchId=?,
                                    @blockId=?,
                                    @floorId=?,
                                    @parkingOwnerId=?,
                                    @typeOfVehicle=?,
                                    @noOfRows=?,
                                    @noOfColumns=?,
                                    @passageLeftAvailable=?,
                                    @passageRightAvailable=?,
                                    @typeOfParking=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @ParkingSlotDetailsupdateJson=?""",
                                        
                                    (
                                    request.parkingLotLineId,
                                    request.branchId,
                                    request.blockId,
                                    request.floorId,
                                    request.parkingOwnerId,
                                    request.typeOfVehicle,
                                    request.noOfRows,
                                    request.noOfColumns,
                                    request.passageLeftAvailable,
                                    request.passageRightAvailable,
                                    request.typeOfParking,
                                    request.activeStatus,
                                    request.updatedBy,
                                    r
                                    ))
            row=result.fetchall()
            result.close()
            return{"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.delete('')
def deleteparkingSlot(activestatus:str,parkingLotLineId:Optional[int]=Query(None),parkingSlotId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[deleteparkingSlot] ?,?,?""",activestatus,parkingLotLineId,parkingSlotId)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": rows[1],"response":rows[0]} 
            else:
                return Response("NotFound")  
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}




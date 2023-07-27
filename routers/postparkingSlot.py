from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from fastapi import Query
from typing import Optional
from routers import Response
from joblib import Parallel, delayed
import json

router=APIRouter(prefix='/postparkingSlot',tags=['postparkingSlot'])
def callFunction(i):
    return i.dict()


@router.post('')
def postparkingSlot(request:schemas.postparkingSlot):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.ParkingSlotDetail)
            result=cur.execute(f"""EXEC [dbo].[singlepostparkingSlot]
                                         @parkingSlotDetailJson=?""",
                                         (json.dumps(r,indent=4, sort_keys=True, default=str)))
            row=result.fetchall()
            result.close()
            return{"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putspostparkingslot(request:schemas.putparkingSlotDetails):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[singleputparkingSlot] 
                                    @laneNumber=?,
                                    @parkingSlotId=?,
                                    @parkingLotLineId=?,
                                    @slotNumber=?,
                                    @rowId=?,
                                    @columnId=?,
                                    @isChargeUnitAvailable=?,
                                    @chargePinType=?,
                                    @activeStatus=?,
                                    @updatedBy=?""",
                                    (request.laneNumber,
                                    request.parkingSlotId,
                                    request.parkingLotLineId,
                                    request.slotNumber,
                                    request.rowId,
                                    request.columnId,
                                    request.isChargeUnitAvailable,
                                    request.chargePinType,
                                    request.activeStatus,
                                    request.updatedBy))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}    

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteparkingSlot(parkingSlotId:int,activestatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE parkingSlot SET activestatus=? Where parkingSlotId=?",activestatus,parkingSlotId)
            result.close()
            if result.rowcount>=1:
                if activestatus=='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}



from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from datetime import datetime,date,time
from fastapi import Query
from typing import Optional
from routers import Response
import ast,json
from joblib import Parallel, delayed

router = APIRouter(prefix='/parkingSlotTest',tags=['parkingSlot'])

@router.post('')
def postparkingSlot(request:schemas.postparkingDetailsSlot):
    try:
        with engine.connect() as cur:
            data = []
            for eachParkingLot in request.parkingLotlineDetails:
                dic = eachParkingLot.dict()
                dic['ParkingSlotDetails'] = json.dumps(dic['ParkingSlotDetails'],indent=4, sort_keys=True, default=str)
            
                data.append(dic)
            data = json.dumps(data,indent=4, sort_keys=True, default=str)
            result=cur.execute(f""" EXEC [dbo].[postParkingSlotTest]
                                    @ParkingLotlineDetailsJson=?""",                                        
                                    (data
                                    ))
            row=result.fetchall()
            result.close()
            
            return{"statusCode": int(row[0][1]), "response": row[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
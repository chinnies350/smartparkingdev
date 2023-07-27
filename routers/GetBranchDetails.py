from datetime import date, datetime
from time import time
from fastapi.routing import APIRouter
import schemas
from routers import Response
from routers.config import engine
from typing import Optional
from fastapi import Query
from routers.config import engine,cursorCommit
from joblib import Parallel, delayed
import json
from datetime import time

router=APIRouter(prefix="/getBranchBasedOnDateTime",tags=['branchMaster'])


@router.get('')
def getBranchMasterBasedOnDateTime(vehicleType:int,fromDate:Optional[date]=Query(None),toDate:Optional[date]=Query(None),Date:Optional[date]=Query(None),fromTime:Optional[time]=Query(None),toTime:Optional[time]=Query(None),lat:Optional[str]=Query(None),lng:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute("EXEC [dbo].[getBranchBasedOnDateTime] @vehicleType=?, @fromDate =?, @toDate=?,@fromTime= ?, @toTime=?,@lat=?,@lng=?", (vehicleType, fromDate, toDate, fromTime, toTime, lat, lng))
            # if fromDate!=None and toDate!=None:
            #     result=cur.execute(f"""EXEC [dbo].[getBranchBasedOnDate] ?,?,?,?,?,?""",(vehicleType,fromDate,toDate,Date,lat,lng))
            # elif fromTime!=None and toTime!=None:
            #     result=cur.execute(f"""EXEC [dbo].[getBranchBasedOnTime] ?,?,?,?,?,?""",(vehicleType,fromTime,toTime,Date,lat,lng))
            rows=result.fetchall()
            # print(rows)
            result.close()
            if rows[0][0] != None:
                return {"statusCode": 1, "response":  json.loads(rows[0][0]) if rows[0][0] != None or len(rows[0]) == 0 else []}
            else:
                return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
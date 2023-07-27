from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import schemas
import datetime
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix='/offerMapping',tags=['offerMapping'])

@router.get('')
def getofferMapping(offerMappingId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),offerId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getofferMapping] ?,?,?,?,?""",offerMappingId,parkingOwnerId,branchId,offerId,activeStatus)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")  

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postofferMapping(request:schemas.offerMapping):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[postofferMapping]
                                    @parkingOwnerId=?,
                                    @branchId=?,
                                    @offerId=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                                    (request.parkingOwnerId,
                                    request.branchId,
                                    request.offerId,
                                    request.activeStatus,
                                    request.createdBy))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteofferMapping(activeStatus:str,offerMappingId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE offerMapping SET activeStatus=? WHERE offerMappingId=?",activeStatus,offerMappingId)
            result.close()
            if result.rowcount>=1:
                if activeStatus =='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

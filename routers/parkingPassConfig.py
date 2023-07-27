from fastapi.routing import APIRouter
import routers
from routers.config import engine
from routers import Response
import datetime
from typing import Optional
from  fastapi import Query
import schemas
import json
from joblib import Parallel, delayed

router=APIRouter(prefix='/parkingPassConfig',tags=['parkingPassConfig'])


def callFunction(i):
    return i.dict()


@router.get('')
def getparkingPassConfig(parkingPassConfigId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),passCategory:Optional[str]=Query(None),passType:Optional[str]=Query(None),taxId:Optional[int]=Query(None),vehicleType:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect()as cur:
            result=cur.execute(f""" EXEC [dbo].[getparkingPassConfig] ?,?,?,?,?,?,?,?""",parkingPassConfigId,parkingOwnerId,branchId,passCategory,passType,taxId,vehicleType,activeStatus)
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
def postparkingPassConfig(request:schemas.parkingPassConfig):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[postparkingPassConfig]
                                    @parkingOwnerId=?,
                                    @branchId=?,
                                    @passCategory=?,
                                    @passType=?,
                                    @noOfDays=?,
                                    @parkingLimit=?,
                                    @totalAmount=?,
                                    @taxId=?,
                                    @vehicleType=?,
                                    @remarks=?,
                                    @activeStatus=?,
                                    @createdBy=?
                                    """,
                                    (request.parkingOwnerId,
                                    request.branchId,
                                    request.passCategory,
                                    request.passType,
                                    request.noOfDays,
                                    request.parkingLimit,
                                    request.totalAmount,
                                    request.taxId,
                                    request.vehicleType,
                                    request.remarks,
                                    request.activeStatus,
                                    request.createdBy))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')
def putparkingPassConfig(request:schemas.putparkingPassConfig):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[putparkingPassConfig]
                                    @passCategory=?,
                                    @passType=?,
                                    @noOfDays=?,
                                    @parkingLimit=?,
                                    @totalAmount=?,
                                    @taxId=?,
                                    @vehicleType=?,
                                    @remarks=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @parkingPassConfigId=?,
                                    @parkingOwnerId=?,
                                    @branchId=?""",
                                    (request.passCategory,
                                    request.passType, 
                                    request.noOfDays,
                                    request.parkingLimit,
                                    request.totalAmount,
                                    request.taxId,
                                    request.vehicleType,
                                    request.remarks,
                                    request.activeStatus,
                                    request.updatedBy,
                                    request.parkingPassConfigId,
                                    request.parkingOwnerId,
                                    request.branchId
                                   ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteparkingPassConfig(activestatus:str,parkingPassConfigId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE parkingPassConfig SET activestatus=? WHERE parkingPassConfigId=?",activestatus,parkingPassConfigId)
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
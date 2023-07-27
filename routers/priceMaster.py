from fastapi.routing import APIRouter
import schemas
from routers.config import engine
from routers import Response
from typing import Optional
from fastapi import Depends, Query
import json,ast
from joblib import Parallel, delayed

router=APIRouter(prefix="/priceMaster",tags=['priceMaster'])
router1 = APIRouter(prefix='/priceMaster1', tags=['priceMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
def getPriceMaster(floorId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),parkingOwnerId:Optional[int]=Query(None),timeType:Optional[str]=Query(None),userMode:Optional[str]=Query(None),idType:Optional[str]=Query(None), priceId: Optional[int] = Query(None), vehicleAccessories: Optional[int] = Query(None), type:Optional[str]=Query(None), configTypeId:Optional[int]=Query(None), vehicleConfigId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getPriceMaster] ?,?,?,?,?,?,?,?,?,?,?,?""",floorId,branchId,activeStatus,parkingOwnerId,timeType,userMode,idType, priceId,vehicleAccessories, type, configTypeId, vehicleConfigId)  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                # if type=='G':
                #     res=json.loads(rows[0].replace(r'\\',""))
                #     for i in res:
                #         i['priceDetailsHourly']=json.loads(i['priceDetailsHourly']) if i['priceDetailsHourly'] else []
                #         i['priceDetailsDaily']=json.loads(i['priceDetailsDaily']) if i['priceDetailsDaily'] else []
                # else:
                #     res=json.loads(rows[0])
                # return {"statusCode": 1,"response":res if rows[0] != None else []}
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":str(e)}

@router.post('')
def postPriceMaster(request:schemas.PriceMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postPriceMaster]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @floorId =?,
                                                @totalAmount =?,
                                                @idType =?,
                                                @vehicle_accessories =?,
                                                @timeType =?,
                                                @taxId =?,
                                                @userMode=?,
                                                @graceTime=?,
                                                @activeStatus =?,
                                                @remarks =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.floorId,
                                            request.totalAmount,
                                            request.idType,
                                            request.vehicle_accessories,
                                            request.timeType,
                                            request.taxId,
                                            request.userMode,
                                            request.graceTime,
                                            request.activeStatus,
                                            request.remarks,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putPriceMaster(request:schemas.PutPriceMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putPriceMaster]
                                                @totalAmount =?,
                                                @idType =?,
                                                @taxId =?,
                                                @userMode=?,
                                                @graceTime=?,
                                                @priceId=?,
                                                @updatedBy =?
                                                
                                                """,
                                            (
                                            request.totalAmount,
                                            request.idType,
                                            request.taxId,
                                            request.userMode,
                                            request.graceTime,
                                            request.priceId,
                                            request.updatedBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deletePriceMaster(priceId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE priceMaster SET activeStatus=? WHERE priceId=?",activeStatus,priceId) 
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


@router1.post('')
async def postPriceMaster1(request: schemas.PriceMaster1):
    try:
        r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.priceDetails)
        with engine.connect() as cur:
            result = cur.execute(f"""
                                    EXEC [dbo].[postPriceMaster1]
                                                                    @parkingOwnerId =?,
                                                                    @branchId =?,
                                                                    @floorId =?,
                                                                    @idType =?,
                                                                    @vehicle_accessories =?,
                                                                    @graceTime=?,
                                                                    @priceDetailsJson =?,
                                                                    @createdBy =?
                                    """, (
                                            request.parkingOwnerId ,
                                            request.branchId,
                                            request.floorId,
                                            request.idType,
                                            request.vehicle_accessories,
                                            request.graceTime,
                                            json.dumps(r,indent=4, sort_keys=True, default=str),
                                            request.createdBy
                                    ))
            row = result.fetchall()
            return {"statusCode":int(row[0][1]),"response":row[0][0]} 
    except Exception as e:
        return {
            'statusCode':0,
            'response':'Server Error'
        }

@router1.put('')
async def putPriceMaster1(request: schemas.PutPriceMaster1):
    try:
        r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.priceDetails)
        with engine.connect() as cur:
            result = cur.execute(f"""
                                    EXEC [dbo].[putPriceMaster1]
                                                                    @parkingOwnerId =?,
                                                                    @branchId =?,
                                                                    @floorId =?,
                                                                    @idType =?,
                                                                    @vehicle_accessories =?,
                                                                    @graceTime=?,
                                                                    @priceDetailsJson =?,
                                                                    @updatedBy =?
                                    """, (
                                            request.parkingOwnerId ,
                                            request.branchId,
                                            request.floorId,
                                            request.idType,
                                            request.vehicle_accessories,
                                            request.graceTime,
                                            json.dumps(r,indent=4, sort_keys=True, default=str),
                                            request.updatedBy
                                    ))
            row = result.fetchall()
            return {"statusCode":int(row[0][1]),"response":row[0][0]} 
    except Exception as e:
        return {
            'statusCode':0,
            'response':'Server Error'
        }
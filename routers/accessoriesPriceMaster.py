from optparse import Option
from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/accessoriesPriceMaster",tags=['accessoriesPriceMaster'])

@router.get('')
def getAccessoriesPriceMaster(parkingOwnerId:Optional[int]=Query(None), branchId:Optional[int]=Query(None),floorId:Optional[int]=Query(None),vehicleType:Optional[int]=Query(None),accessories:Optional[int]=Query(None),priceId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getAccessoriesPriceMaster] ?,?,?,?,?,?,?""",(priceId,parkingOwnerId, branchId,floorId,vehicleType,accessories,activeStatus))  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
       
        return {"statusCode": 0,"response": str(e)}

@router.post('')
def postAccessoriesPriceMaster(request:schemas.AccessoriesPriceMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postAccessoriesPriceMaster]
                                                @parkingOwnerId =?,
										@branchId =?,
										@floorId =?,
										@amount =?,
										@tax =?,
										@totalAmount =?,
										@vehicleType =?,
										@accessories =?,
										@taxId =?,
										@activeStatus =?,
										@remarks=?,
										@createdBy =?
                                                
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.floorId,
                                            request.amount,
                                            request.tax,
                                            request.totalAmount,
                                            request.vehicleType,
                                            request.accessories,
                                            request.taxId,
                                            request.activeStatus,
                                            request.remarks,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception as postAccessoriesPriceMaster ",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putAccessoriesPriceMaster(request:schemas.PutAccessoriesPriceMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putAccessoriesPriceMaster]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @floorId =?,
                                                @amount =?,
                                                @tax =?,
                                                @totalAmount =?,
                                                @vehicleType =?,
                                                @accessories =?,
                                                @taxId =?,
                                                @remarks=?,
                                                @updatedBy= ?,
                                                @priceId=?
                                                
                                                """,
                                            (
                                            request.parkingOwnerId,
                                            request.branchId,
                                            request.floorId,
                                            request.amount,
                                            request.tax,
                                            request.totalAmount,
                                            request.vehicleType,
                                            request.accessories,
                                            request.taxId,
                                            request.remarks,
                                            request.updatedBy,
                                            request.priceId
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception as putAccessoriesPriceMaster ",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteAccessoriesPriceMaster(priceId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE accessoriesPriceMaster SET activeStatus=? WHERE priceId=?",activeStatus,priceId) 
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
        return {"statusCode": 0,"response": str(e)}



from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
from fastapi import Query
import json
from joblib import Parallel, delayed
from typing import Optional

router = APIRouter(prefix='/floorFeatures',tags=['floorMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
def getfloorFeatures(featuresId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),floorId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getfloorFeatures] ?,?,?,?,?""",featuresId,parkingOwnerId,branchId,floorId,activeStatus)
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
def postfloorFeatures(request:schemas.PostfloorFeatures):
    try:
        with engine.connect() as cur:
            conn,cur=cursorCommit()
           
            cur.execute(f"""
                        EXEC [dbo].[postfloorFeatures] 
                        @parkingOwnerId=?,
                        @branchId=?,
                        @floorId=?,
                        @featureName=?,
                        @description=?,
                        @taxId=?,
                        @totalAmount=?,
                        @createdBy=?
                   
                      """,
                      (request.parkingOwnerId,
                        request.branchId,
                        request.floorId,
                        request.featureName,
                        request.description,
                        request.taxId,
                        request.totalAmount,
                        request.createdBy,
                      ))
            row=cur.fetchall()
            conn.commit()
            conn.close()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')
def putfloorFeatures(request:schemas.PutfloorFeaures):
    try:
        with engine.connect() as cur:
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putfloorFeatures] 
                               @featuresId=?,
                               @featureName=?,
                               @description=?,
                               @taxId=?,
                               @totalAmount=?,
                               @floorId=?,
                               @updatedBy=?
                               """,
                                (
                                 request.featuresId,
                                 request.featureName,
                                 request.description,
                                 request.taxId,
                                 request.totalAmount,
                                 request.floorId,
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
def deletefloorFeatures(featuresId:int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE floorFeatures SET activeStatus=? WHERE featuresId=?",activeStatus,featuresId) 
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
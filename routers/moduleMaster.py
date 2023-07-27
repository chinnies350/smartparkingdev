from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/moduleMaster',tags=['moduleMaster'])


@router.get('')
def getmoduleMaster(moduleId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getModuleMaster] ?,?""",moduleId,activeStatus)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            
           
                  
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.post('')
def postmoduleMaster(request:schemas.ModuleMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postModuleMaster]
                                                @parkingOwnerId=?,
                                                @moduleName=?,
                                                @imageURL=?,
                                                @activeStatus=?,
								                @createdBy=?
                                                """,
                        (
                            request.parkingOwnerId,
                            request.moduleName,
                            request.imageURL,
                            request.activeStatus,
                            request.createdBy  
                        ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}  
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putmoduleMaster(request: schemas.PutModuleMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putModuleMaster]
                                                @parkingOwnerId=?,
                                                @moduleName=?,
                                                @imageURL=?,
                                                @activeStatus=?,
								                @updatedBy=?,
                                                @moduleId=?
                                                """,
                        (
                            request.parkingOwnerId,
                            request.moduleName,
                            request.imageURL,
                            request.activeStatus,
                            request.updatedBy,
                            request.moduleId
                        ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}                  
        
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deletemoduleMaster(moduleId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE moduleMaster SET activeStatus=? WHERE moduleId=?",activeStatus,moduleId) 
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


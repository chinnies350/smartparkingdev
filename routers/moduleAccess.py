from datetime import datetime
from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
import datetime
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/moduleAccess',tags=['moduleAccess'])


@router.get('')
def getmoduleAccess(userId:Optional[int] = Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getModuleAccess] ?""",userId)
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
def postmoduleAccess(request:schemas.ModuleAccess):
    try:
        createdDate = datetime.datetime.now()
        with engine.connect() as cur:
            result=cur.execute(f"""DELETE moduleAccess WHERE userId={request.userId}""")
            result.close()
            if len(request.moduleId)>0:   
                for id in request.moduleId:
                    result=cur.execute("INSERT INTO moduleAccess (parkingOwnerId,userId,moduleId,activeStatus,createdBy,createdDate)" "VALUES(?,?,?,?,?,?)",(request.parkingOwnerId,request.userId,id,request.activeStatus,request.createdBy,createdDate))
                    result.close()
            if result.rowcount >= 1:
                return Response("AddMsg")
            else:
                return Response("NotAdd")
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putmoduleAccess(request: schemas.PutModuleAccess):
    try:
        updatedDate = datetime.datetime.now()
        with engine.connect() as cur:
            result=cur.execute("UPDATE moduleAccess SET parkingOwnerId=?,moduleId=?,userId=?,activeStatus=? ,updatedBy=?,updatedDate=? WHERE moduleAccessId=?",
                           request.parkingOwnerId,
                            request.moduleId,
                            request.userId,
                            request.activeStatus,
                            request.updatedBy,
                            updatedDate,
                            request.moduleAccessId
                            )
            result.close()
            if result.rowcount >= 1:
                return Response("updateMsg") 
            else:
               return Response("NotUpdate")                  
        
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deletemoduleAccess(moduleAccessId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE moduleAccess SET activeStatus=? WHERE moduleAccessId=?",activeStatus,moduleAccessId) 
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

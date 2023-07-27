from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/configMaster',tags=['configMaster'])

@router.get('')
def getconfig(configId:Optional[int]=Query(None),configTypeId:Optional[int]=Query(None),activestatus:Optional[str]=Query(None),configTypename:Optional[str]=Query(None),parkingOwnerId:Optional[int]=Query(None),blockId:Optional[int]=Query(None),type:Optional[str]=Query(None),idType:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                f"""EXEC [dbo].[getConfigMaster] ?,?,?,?,?,?,?,?""",configId,configTypeId,activestatus,configTypename,parkingOwnerId,blockId,type,idType)  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.post('')
def postconfig(request:schemas.ConfigMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postconfigMaster]
                                    @parkingOwnerId=?,
                                    @configTypeId=?,
                                    @configName=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                        (
                            # request.parkingOwnerId,
                            None,
                            request.configTypeId,
                            request.configName,
                            request.activeStatus,
                            request.createdBy                                                        
                        ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]), "response": row[0][0]}  
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.put('')
def putconfig(request: schemas.PutConfigMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putconfigMaster]
                                    @configName=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @parkingOwnerId=?,
                                    @configTypeId=?,
                                    @configId=?""",
                                                       
                            request.configName,
                            request.activeStatus,
                            request.updatedBy,  
                            None,        
                            # request.parkingOwnerId,
                            request.configTypeId,
                            request.configId
                           )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}                 
        
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
 

@router.delete('')
def deleteconfigType(configId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE ConfigMaster SET activeStatus=? WHERE configId=?",activeStatus,configId) 
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
        return{"statusCode":0,"response":"Server Error"}



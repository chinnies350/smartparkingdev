from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/configType',tags=['configType'])

@router.get('')
def getconfigType(configTypeId:Optional[int]=Query(None),typeName:Optional[str]=Query(None),activestatus:Optional[str]=Query(None), type:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getConfigType] ?,?,?,?""",configTypeId,typeName,activestatus, type)   
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
def postconfigType(request:schemas.ConfigType):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postconfigType]
                                    @typeName=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                                (                           
                                    request.typeName,
                                    request.activeStatus,
                                    request.createdBy,                            
                                ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]} 
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}



@router.put('')
def putconfigType(request: schemas.PutConfigType):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putconfigType]
                                    @typeName=?,
                                    @activeStatus=?,
                                    @updatedBy=?,
                                    @configTypeId=?""",
                                                                
                                    request.typeName,
                                    request.activeStatus,
                                    request.updatedBy,
                                    request.configTypeId)
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
  

@router.delete('')
def deleteconfigType(configTypeId: int,activeStatus:str):
    try:
        with engine.connect() as cur:
            if activeStatus == 'A':
                result = cur.execute("SELECT * FROM configType WHERE typeName=(SELECT typeName FROM configType WHERE configTypeId=?) AND activeStatus = 'A' AND configTypeId != ?", (configTypeId, configTypeId))
                row = result.fetchone()
                if row != None:
                    return {
                        'statusCode': 0,
                        'response': 'Data Already Exists'
                    }
            result=cur.execute("UPDATE ConfigType SET activeStatus=? WHERE configTypeId=?",activeStatus,configTypeId) 
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

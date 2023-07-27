from fastapi.routing import APIRouter
from routers.config import engine
from typing import Optional
from routers import Response
from fastapi import Query
import schemas
import json

router=APIRouter(prefix='/chargePinConfig',tags=['chargePinConfig'])

@router.get('')
def getconfig(chargePinId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getchargePinConfig] ?,?""",chargePinId,activeStatus)  
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
def postchargePinConfig(request:schemas.chargePinConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postchargePinConfig]
                                    @chargePinConfig=?,
                                    @chargePinImageUrl=?,
                                    @activeStatus=?,
                                    @createdBy=?""",
                        (
                            request.chargePinConfig,
                            request.chargePinImageUrl,
                            request.activeStatus,
                            request.createdBy                                                        
                        ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]), "response": row[0][0]}  
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putchargePinConfig(request:schemas.putchargePinConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putchargePinConfig]
                                    @chargePinConfig=?,
                                    @chargePinImageUrl=?,
                                    @updatedBy=?,
                                    @chargePinId=?""",
                        (
                            request.chargePinConfig,
                            request.chargePinImageUrl,
                            request.updatedBy,
                            request.chargePinId                                                        
                        ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]), "response": row[0][0]}  
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.delete('')
def deletechargePinConfig(chargePinId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE chargePinConfig SET activeStatus=? WHERE chargePinId=?",activeStatus,chargePinId) 
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

       

        


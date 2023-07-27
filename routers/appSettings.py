from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/appSettings",tags=['appSettings'])

router1 = APIRouter(prefix='/checkAppVersion',tags=['appSettings'])

@router.get('')
def getAppSettings(uniqueId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None), appVersion:Optional[float]=Query(None),appType:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getAppSettings] ?,?,?,?""",uniqueId,activeStatus,appVersion,appType)  
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
def postAppSettings(request:schemas.AppSettings):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postAppSettings]
                                                @privacyPolicy =?,
                                                @termsAndConditions =?,
                                                @appVersion =?,
                                                @appType=?,
                                                @activeStatus=?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.privacyPolicy,
                                            request.termsAndConditions,
                                            request.appVersion,
                                            request.appType,
                                            request.activeStatus,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putAppSettings(request:schemas.PutAppSettings):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putappSettings]
                                                @privacyPolicy =?,
                                                @termsAndConditions =?,
                                                @appVersion =?,
                                                @appType=?,
                                                @updatedBy =?,
                                                @uniqueId=?
                                                """,
                                            (
                                            request.privacyPolicy,
                                            request.termsAndConditions,
                                            request.appVersion,
                                            request.appType,
                                            request.updatedBy,
                                            request.uniqueId
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteAppSettings(uniqueId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE appSettings SET activeStatus=? WHERE uniqueId=?",activeStatus,uniqueId) 
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

@router1.get('')
def checkVersionDef(appVersion:float, appType:str):
    try:
        with engine.connect() as cur:
            result = cur.execute("EXEC [dbo].[checkAppVersion] @appType=?, @appversion=?", (appType, appVersion))
            row = result.fetchone()
            if row[0]:
                return {"statusCode":1, "response":row[0]}
            else:
                return {"statusCode":0, "response":row[0]}
    except Exception as e:
        print(f'checkApiVersion {str(e)}')
        return{"statusCode":0,"response":"Server Error"} 

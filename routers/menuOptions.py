from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router = APIRouter(prefix='/menuOptions',tags=['menuOptions'])


@router.get('')
def getmenuOptions(optionId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getMenuOption] ?,?""",optionId,activeStatus)    
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
def postmenuOptions(request:schemas.MenuOptions):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postMenuOption]
                                                @parkingOwnerId=?,
                                                @moduleId=?,
                                                @optionName=?,
                                                @activeStatus=?,
								                @createdBy=?
                                                """,
                        (
                            request.parkingOwnerId,
                            request.moduleId,
                            request.optionName,
                            request.activeStatus,
                            request.createdBy  
                        ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putmenuOptions(request: schemas.PutMenuOptions):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putMenuOption]
                                                @parkingOwnerId=?,
                                                @moduleId=?,
                                                @optionName=?,
                                                @activeStatus=?,
								                @updatedBy=?,
                                                @optionId=?
                                                """,
                        (
                            request.parkingOwnerId,
                            request.moduleId,
                            request.optionName,
                            request.activeStatus,
                            request.updatedBy,
                            request.optionId
                        ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}                  
        
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deletemenuOptions(optionId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE menuOptions SET activeStatus=? WHERE optionId=?",activeStatus,optionId) 
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


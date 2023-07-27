from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/cancellationRules",tags=['cancellationRules'])

@router.get('')
def getCancellationRules(uniqueId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getCancellationRules] ?,?""",uniqueId,activeStatus)  
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
def postCancellationRules(request:schemas.CancellationRules):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postCancellationRules]
                                                @type =?,
                                                @duration=?,
                                                @noOfTimesPerUser =?,
                                                @cancellationCharges=?,
                                                @activeStatus =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.type,
                                            request.duration,
                                            request.noOfTimesPerUser,
                                            request.cancellationCharges,
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
def putCancellationRules(request:schemas.PutCancellationRules):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putCancellationRules]
                                                @type =?,
                                                @duration=?,
                                                @noOfTimesPerUser =?,
                                                @cancellationCharges=?,
                                                @updatedBy =?,
                                                @uniqueId=?
                                                """,
                                            (
                                            request.type,
                                            request.duration,
                                            request.noOfTimesPerUser,
                                            request.cancellationCharges,
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
def deleteCancellationRules(uniqueId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE cancellationRules SET activeStatus=? WHERE uniqueId=?",activeStatus,uniqueId) 
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
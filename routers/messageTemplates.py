from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
from fastapi import Query
import json
from joblib import Parallel, delayed
from typing import Optional

router = APIRouter(prefix='/messageTemplates',tags=['messageTemplates'])


@router.get('')
def getMessageTemplates(uniqueId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getMessageTemplates] ?""",uniqueId)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound") 
    except Exception as e:
        return {"statusCode": 0,"response": f"Module Not Found {str(e)}"}


@router.post('')
def postMessageTemplates(request:schemas.PostMessageTemplates):
    try:
        with engine.connect() as cur:
            conn,cur=cursorCommit()
           
            cur.execute(f"""
                        EXEC [dbo].[postMessageTemplates] 
                        @messageHeader=?,
                        @subject=?,
                        @messageBody=?,
                        @templateType=?,
                        @peid=?,
                        @tpid=?,
                        @createdBy=?
                      """,
                      (request.messageHeader,
                        request.subject,
                        request.messageBody,
                        request.templateType,
                        request.peid,
                        request.tpid,
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
def putMessageTemplates(request:schemas.PutMessageTemplates):
    try:
        with engine.connect() as cur:
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putMessageTemplates] 
                               @messageHeader=?,
                               @subject=?,
                               @messageBody=?,
                               @templateType=?,
                               @peid=?,
                               @tpid=?,
                               @uniqueId=?,
                               @updatedBy=?
                               """,
                                (request.messageHeader,
                                 request.subject,
                                 request.messageBody,
                                 request.templateType,
                                 request.peid,
                                 request.tpid,
                                 request.uniqueId,
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
def deleteMessageTemplates(uniqueId:int):
    try:
       with engine.connect() as cur:
            result=cur.execute("delete from messageTemplates WHERE uniqueId=?",uniqueId) 
            result.close()
            if result.rowcount >= 1:
               return {"statusCode": 1,"response": "Data Deleted Successfully"}
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
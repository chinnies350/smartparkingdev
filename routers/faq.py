from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/faq",tags=['faq'])

@router.get('')
def getFaq(faqId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),offerId:Optional[int]=Query(None),questionType:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getFaq] ?,?,?,?""",faqId,activeStatus,offerId,questionType)  
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
       
        return {"statusCode": 0,"response": str(e)}

@router.post('')
def postFaq(request:schemas.Faq):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postFaq]
                                                @offerId =?,
                                                @question =?,
                                                @answer =?,
                                                @questionType =?,
                                                @activeStatus =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.offerId,
                                            request.question,
                                            request.answer,
                                            request.questionType,
                                            request.activeStatus,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putFaq(request:schemas.PutFaq):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putFaq]
                                                @offerId =?,
                                                @question =?,
                                                @answer =?,
                                                @questionType =?,
                                                @updatedBy =?,
                                                @faqId=?
                                                """,
                                            (
                                            request.offerId ,
                                            request.question,
                                            request.answer,
                                            request.questionType,
                                            request.updatedBy,
                                            request.faqId
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteFaq(faqId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE faq SET activeStatus=? WHERE faqId=?",activeStatus,faqId) 
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
        return {"statusCode": 0,"response": str(e)}
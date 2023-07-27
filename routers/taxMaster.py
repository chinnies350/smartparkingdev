from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import ast
from routers.config import engine,cursorCommit
import json

router = APIRouter(prefix='/taxMaster',tags=['taxMaster'])


@router.get('')
def gettaxMaster(taxId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getTaxMaster] ?,?""",taxId,activeStatus)
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
def posttaxMaster(request:schemas.TaxMaster):
    try:
        createdDate = datetime.datetime.now()
        with engine.connect() as cur:
            conn,cur=cursorCommit()
           
            result=cur.execute("""
                               DECLARE @varRes NVARCHAR(400);
                               DECLARE @varStatus NVARCHAR(1);
                               EXEC [dbo].[postTaxMaster] 
                                @serviceName=?,
                                @taxName=?,
                                @taxDescription=?,
                                @taxPercentage=?,
                                @activeStatus=?,
                                @effectiveFrom=?,
                                @effectiveTill=?,
                                @createdBy=?,
                                @outputVal = @varRes OUTPUT,
                                @outputStatus = @varStatus OUTPUT
                                SELECT @varRes AS varRes,@varStatus AS varStatus""",
                                (request.serviceName,
                                request.taxName,
                                request.taxDescription,
                                request.taxPercentage,
                                request.activeStatus,
                                request.effectiveFrom,
                                request.effectiveTill,
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
def puttaxMaster(request: schemas.PutTaxMaster):
    try:
        updatedDate = datetime.datetime.now()
        with engine.connect() as cur:
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putTaxMaster] 
                               @taxId=?,
                               @taxName=?,
                               @serviceName=?,
                               @taxDescription=?,
                               @taxPercentage=?,
                               @activeStatus=?,
                               @effectiveFrom=?,
                               @updatedBy=?
                               
                               
                               """,
                               (
                               request.taxId,
                               request.taxName,
                               request.serviceName,
                               request.taxDescription,
                               request.taxPercentage,
                               request.activeStatus,
                               request.effectiveFrom,
                               request.updatedBy)
                            )
            row=cur.fetchall()
            
            conn.commit()
            conn.close()
        
            return {"statusCode": int(row[0][1]), "response": row[0][0]} 
            
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deleteconfigType(taxId:int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE TaxMaster SET activeStatus=? WHERE taxId=?",activeStatus,taxId) 
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
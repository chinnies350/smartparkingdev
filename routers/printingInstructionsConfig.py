from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
from joblib import Parallel, delayed
import ast,json

router=APIRouter(prefix="/printingInstructionsConfig",tags=['printingInstructionsConfig'])
router1 = APIRouter(prefix="/printingInstructionsConfig1", tags=['printingInstructionsConfig'])

def callFunction(i):
    return i.dict()

@router.get('')
def getPrintingInstructionsConfig(uniqueId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None), instructionType: Optional[str] = Query(None), activeStatus: Optional[str]=Query(None), type:Optional[str] = Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getPrintingInstructionsConfig] ?,?,?,?,?,?""",(uniqueId,parkingOwnerId,branchId, instructionType, activeStatus, type) )
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
def postPrintingInstructionsConfig(request:schemas.PrintingInstructionsConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postPrintingInstructionsConfig]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @instructionType =?,
                                                @instructions=?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.instructionType,
                                            request.instructions,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putPrintingInstructionsConfig(request:schemas.PutPrintingInstructionsConfig):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putPrintingInstructionsConfig]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @instructionType =?,
                                                @instructions=?,
                                                @updatedBy =?,
                                                @uniqueId=?
                                                """,
                                            (
                                            request.parkingOwnerId,
                                            request.branchId,
                                            request.instructionType,
                                            request.instructions,
                                            request.updatedBy,
                                            request.uniqueId
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}  

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deletePrintingInstructionsConfig(uniqueId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE printingInstructionsConfig SET activeStatus=? WHERE uniqueId=?",activeStatus,uniqueId) 
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


@router1.post('')
def postPrintingInstructionsConfig1(request:schemas.PrintingInstructionsConfig1):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.instructionsDetails)
            
            result=cur.execute(f"""EXEC [dbo].[postPrintingInstructionsConfig1]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @instructionType =?,
                                                @PrintingInstructionsDetailsJson=?,
                                                @createdBy =?
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.instructionType,
                                            json.dumps(r,indent=4, sort_keys=True, default=str),
                                            request.createdBy
                                            )
                                            )
                                        
            row=result.fetchall()
            
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":str(e)}
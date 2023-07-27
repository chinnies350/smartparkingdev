from datetime import datetime
from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
import datetime
from typing import Optional
from fastapi import Query
import json
from joblib import Parallel, delayed


router = APIRouter(prefix='/menuOptionAccess',tags=['menuOptionAccess'])


def callFunction(i):
    return i.dict()


@router.get('')
def getmenuOptionAccess(moduleId:Optional[int]=Query(None),userId:Optional[int]=Query(None),branchId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getMenuOptionAccess] ?,?,?""",moduleId,userId,branchId)
            rows = result.fetchone()
            result.close()
            if rows[0]:
                
                return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.post('')
def postmenuOptionAccess(request:schemas.MenuOptionAccess):
    try:
        
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.optionDetails)
            conn,cur=cursorCommit()
            cur.execute(f"""DECLARE @varRes NVARCHAR(400);
                            DECLARE @varStatus NVARCHAR(1);
                            EXEC [dbo].[postMenuOptionAccess]
                            @parkingOwnerId=?,
                            @userId =?,
                            @moduleId =?,
                            @createdBy =?,
                            @optionDetailsJson =?,
                            @outputVal = @varRes OUTPUT,
                            @outputStatus = @varStatus OUTPUT
                            SELECT @varRes AS varRes,@varStatus AS varStatus""",
                            (
                                request.parkingOwnerId,
                                request.userId,
                                request.moduleId,
                                request.createdBy,
                                json.dumps(r)
                            ))
            row=cur.fetchall()
            conn.commit()
            conn.close()
        
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
             
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
        
# @router.put('')
# def putmenuOptionAccess(request: schemas.PutMenuOptionAccess):
#     try:
#         updatedDate = datetime.datetime.now()
#         with engine.connect() as cur:
#             result=cur.execute("UPDATE menuOptionAccess SET parkingOwnerId=?,userId=?,moduleId=?,optionId=?,activeStatus=?, updatedBy=?,updatedDate=? WHERE MenuOptionAccessId=?",
#                             request.parkingOwnerId,
#                             request.userId,
#                             request.moduleId,
#                             request.optionId,
#                             request.activeStatus,
#                             request.updatedBy,
#                             updatedDate,
#                             request.MenuOptionAccessId)
#             result.close()
#             if result.rowcount >= 1:
#                 return Response("updateMsg") 
#             else:
#                return Response("NotUpdate")                  
        
#     except Exception as e:
#         return {"statusCode": 0,"response": str(e)} 
@router.put('')
def putmenuOptionAccess(request: schemas.ListPutMenuOptionAccess):
    try:
        updatedDate = datetime.datetime.now()
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.menuOptionAccessDetails)
            # result=cur.execute("UPDATE menuOptionAccess SET parkingOwnerId=?,userId=?,moduleId=?,optionId=?,activeStatus=?, updatedBy=?,updatedDate=? WHERE MenuOptionAccessId=?",
            #                 request.parkingOwnerId,
            #                 request.userId,
            #                 request.moduleId,
            #                 request.optionId,
            #                 request.activeStatus,
            #                 request.updatedBy,
            #                 updatedDate,
            #                 request.MenuOptionAccessId)
            print('r', r, type(r))
            print('converted', json.dumps(r,indent=4, sort_keys=True, default=str), type(json.dumps(r,indent=4, sort_keys=True, default=str)))
            result = cur.execute(f" EXEC [dbo].[putMenuOptionAccess] @menuOptionJsonData=?", (json.dumps(r,indent=4, sort_keys=True, default=str)))
            row = result.fetchone()
            result.close()
            if row != None:
                return {
                    'statusCode':row[1],
                    'response': row[0]
                }
            # if result.rowcount >= 1:
            #     return Response("updateMsg") 
            # else:
            #    return Response("NotUpdate")                  
        
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deletemenuOptionAccess(MenuOptionAccessId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE menuOptionAccess SET activeStatus=? WHERE MenuOptionAccessId=?",activeStatus,MenuOptionAccessId) 
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


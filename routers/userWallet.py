
from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import ast
import json

router=APIRouter(prefix="/userWallet",tags=['userWallet'])

@router.get('')
def getUserWallet(uniqueId:Optional[int]=Query(None),userId:Optional[int]=Query(None),status:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(
                    f"""EXEC [dbo].[getUserWallet] ?,?,?""",uniqueId,userId,status)  
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
def postUserWallet(request:schemas.UserWallet):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postUserWallet]
                                                @userId =?,
                                                @walletAmt =?,
                                                @loyaltyPoints =?,
                                                @status=?,
                                                @expiryDate =?,
                                                @creditedDate =?,
                                                @reasonToCredit =?
                                                
                                                """,
                                            (request.userId,
                                            request.walletAmt,
                                            request.loyaltyPoints,
                                            request.status,
                                            request.expiryDate,
                                            request.creditedDate,
                                            request.reasonToCredit
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}
                
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

# @router.put('')
# def putUserWallet(request:schemas.PutUserWallet):
#     try:
#         with engine.connect() as cur:
#             result=cur.execute(f"""EXEC [dbo].[putUserWallet]
#                                                 @userId =?,
#                                                 @walletAmt =?,
#                                                 @loyaltyPoints =?,
                                                
#                                                 @expiryDate =?,
#                                                 @creditedDate =?,
#                                                 @reasonToCredit =?,
#                                                 @uniqueId=?
#                                                 """,
#                                             (
#                                             request.userId,
#                                             request.walletAmt,
#                                             request.loyaltyPoints,
                                           
#                                             request.expiryDate,
#                                             request.creditedDate,
#                                             request.reasonToCredit,
#                                             request.uniqueId
#                                             )
#                                             )
#             row=result.fetchall()
#             return{"statusCode":int(row[0][1]),"response":row[0][0]}    
#     except Exception as e:
#         return{"statusCode":0,"response":"Server Error"}


# @router.delete('')
# def deleteUserWallet(uniqueId: int,activeStatus:str):
#     try:
#        with engine.connect() as cur:
#             result=cur.execute("UPDATE userWallet SET activeStatus=? WHERE uniqueId=?",activeStatus,uniqueId) 
#             result.close()
#             if result.rowcount >= 1:
#                if activeStatus=='D':
#                    return Response("deactiveMsg")
#                else:
#                    return Response("ActiveMsg")
#             else:
#                 return Response("NotFound")

#     except Exception as e:
#         return {"statusCode": 0,"response": str(e)}
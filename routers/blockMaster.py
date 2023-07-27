from fastapi.routing import APIRouter
import schemas
from routers.config import engine
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix="/blockMaster",tags=['blockMaster'])

@router.get('')
def getBlockMaster(blockId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),approvalStatus:Optional[str]=Query(None),configId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getBlockMaster] ?,?,?,?,?,?""",(blockId,parkingOwnerId,branchId,activeStatus,approvalStatus,configId))
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}        

@router.post('')
def postBlockMaster(request:schemas.BlockMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postBlockMaster]
                                                @parkingOwnerId=?,
                                                @branchId=?,
                                                @blockName=?,
                                                @activeStatus=?,
                                                @approvalStatus=?,
                                                @createdBy=?
                                                """,
                                            (request.parkingOwnerId,
                                            request.branchId,
                                            request.blockName,
                                            request.activeStatus,
                                            request.approvalStatus,
                                            request.createdBy)
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.put('')
def putBlockMaster(request:schemas.PutBlockMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putBlockMaster]
                                                @blockId=?,
                                                @parkingOwnerId=?,
                                                @branchId=?,
                                                @blockName=?,
                                                @approvalStatus=?,
                                                @updatedBy=?
                                """,
                                (
                                request.blockId,
                                request.parkingOwnerId,
                                request.branchId,
                                request.blockName,
                                request.approvalStatus,
                                request.updatedBy))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}   
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.delete('')     
def deleteBlokMaster(blockId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            if activeStatus == 'A':
                result = cur.execute(f"""
                        DECLARE @branchId INT, 
                        @blockName nvarchar(50),
                        @blockId INT = ?
                        SELECT @branchId=branchId, @blockName = blockName FROM blockMaster
                        WHERE blockId= @blockId

                        SELECT * FROM blockMaster 
                        WHERE branchId = @branchId AND blockName = @blockName AND activeStatus = 'A' AND blockId != @blockId
                """, (blockId))
                row = result.fetchone()
                if row != None:
                    return {
                        'statusCode':0,
                        "response": 'Data Already Exists'
                    }


            result=cur.execute(f"""UPDATE blockMaster SET activeStatus=? WHERE blockId=?""",(activeStatus,blockId))
            if result.rowcount>=1:
                if activeStatus=="D":
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"} 
            
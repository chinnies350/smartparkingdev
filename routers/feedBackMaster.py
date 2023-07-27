from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json

router=APIRouter(prefix='/feedBackMaster',tags=['feedBackMaster'])

@router.get('')
def getfeedBackMaster(FeedbackId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),bookingId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getFeedBackMaster] ?,?,?,?""",FeedbackId,parkingOwnerId,branchId,bookingId)
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
def postfeedBackMaster(request:schemas.FeedBackMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postfeedBackMaster]
                                    @parkingOwnerId=?,
                                    @branchId=?,
                                    @bookingId=?,
                                    @feedbackRating=?,
                                    @feedbackComment=?,
                                    @createdBy=?""",
                                (request.parkingOwnerId,
                                request.branchId,
                                request.bookingId,
                                request.feedbackRating,
                                request.feedbackComment,
                                request.createdBy
                                ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putfeedBackMaster(request:schemas.PutFeedBackMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putFeedBackMaster]
                                    @feedbackRating=?,
                                    @feedbackComment=?,
                                    @updatedBy=?,
                                    @FeedbackId=?,
                                    @parkingOwnerId=?,
                                    @branchId=?,
                                    @bookingId=?""",
                                (request.feedbackRating,
                                request.feedbackComment,
                                request.updatedBy,
                                request.FeedbackId,
                                request.parkingOwnerId,
                                request.branchId,
                                request.bookingId))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.delete('')
def deleteFeedBackMaster(FeedbackId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("DELETE FROM feedBackMaster WHERE FeedbackId=?",FeedbackId)
            result.close()
            if result.rowcount>=1:
                return Response("deleteMsg")
            else:
                return Response("deleteMsg")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

    

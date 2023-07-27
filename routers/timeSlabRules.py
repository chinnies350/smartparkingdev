from fastapi.routing import APIRouter
import schemas
from routers.config import engine
from routers import Response
from typing import Optional
from fastapi import Query
import ast

router=APIRouter(prefix="/timeSlabRules",tags=['timeSlabRules'])

@router.post('')
def postTimeSlabRules(request:schemas.TimeSlabRules):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postTimeSlabRules]
                                                @priceId =?,
                                                @fromDate =?,
                                                @toDate =?,
                                                @activeStatus =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.priceId,
                                            request.fromDate,
                                            request.toDate,
                                            request.activeStatus,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
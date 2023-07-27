from fastapi.routing import APIRouter
import schemas
from routers.config import engine


router=APIRouter(prefix="/extraFees",tags=['extraFees'])


@router.post('')
def postExtraFees(request:schemas.PostExtraFees):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postExtraFees]
                                                @bookingPassId =?,
                                                @bookingIdType=?,
                                                @priceId=?,
                                                @count=?,
                                                @extraFee =?,
                                                @extraFeesDetails =?,
                                                @createdBy =?
                                                
                                                """,
                                            (request.bookingPassId,
                                            request.bookingIdType,
                                            request.priceId,
                                            request.count,
                                            request.extraFee,
                                            request.extraFeesDetails,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
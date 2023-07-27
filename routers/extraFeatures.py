from fastapi.routing import APIRouter
import schemas
from routers.config import engine


router=APIRouter(prefix="/extraFeatures",tags=['extraFeatures'])


@router.post('')
def postextraFeatures(request:schemas.PostExtraFeatures):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postextraFeatures]
                                                @bookingPassId =?,
                                                @bookingIdType=?,
                                                @floorFeaturesId =?,
                                                @count=?,
                                                @extraDetail =?
                                                """,
                                            (request.bookingPassId,
                                            request.bookingIdType,
                                            request.floorFeaturesId,
                                            request.count,
                                            request.extraDetail
                                            
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        return{"statusCode":0,"response":"Server Error"}

@router.put('')
def putExtraFeatures(extraFeatureId:int,extraDetail:str):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putExtraFeatures] ?,?""",(extraFeatureId,extraDetail))
            rows=result.fetchall()
            return{"statusCode":rows[0][1],"response":rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

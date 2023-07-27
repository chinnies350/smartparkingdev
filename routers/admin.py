from fastapi.routing import APIRouter
from routers.config import engine
import schemas

router = APIRouter(prefix='/admin',tags=['admin'])

@router.post('')
def postAdmin(request: schemas.PostAdmin):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""
                                EXEC [dbo].[postAdmin] 
                                @userName =?,
								@password =?,
								@emailId =?,
								@phoneNumber =?,
                                @imageUrl=?,
								@activeStatus =?,
								@createdBy =?,
                                @parkingName=?,
                                @shortName=?,
                                @founderName=?,
                                @logoUrl=?,
                                @websiteUrl=?,
                                @gstNumber=?,
                                @placeType=?
                                """,
                        (   request.userName,
                            request.password,
                            request.emailId,
                            request.phoneNumber,
                            request.imageUrl,
                            request.activeStatus,
                            request.createdBy,
                            request.parkingName,
                            request.shortName,
                            request.founderName,
                            request.logoUrl,
                            request.websiteUrl,
                            request.gstNumber,
                            request.placeType
                            ))
            
            row=result.fetchall()
            print(row)
            return {"statusCode": int(row[0][1]), "response": row[0][0],"userId":row[0][2]}
              
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}



   
 



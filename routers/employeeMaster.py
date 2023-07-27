from fastapi.routing import APIRouter
import schemas
from routers.config import engine


router=APIRouter(prefix="/employeeMaster",tags=['employeeMaster'])


@router.post('')
def postEmployeeMaster(request:schemas.postEmployeeMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postEmployeeMaster]
                                                @parkingOwnerId =?,
                                                @branchId =?,
                                                @blockId =?,
                                                @floorId =?,
                                                @userId =?,
                                                @DOJ =?,
                                                @empType =?,
                                                @empDesignation =?,
                                                @shiftId=?,
                                                @createdBy =?
                                                """,
                                                (request.parkingOwnerId,
                                            request.branchId,
                                            request.blockId,
                                            request.floorId,
                                            request.userId,
                                            request.DOJ,
                                            request.empType,
                                            request.empDesignation,
                                            request.shiftId,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}    
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
    

@router.put('')
def putEmployeeMaster(request:schemas.PutEmployeeMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putEmployeeMaster]
                                    @employeeId =?,
                                    @branchId =?,
                                    @blockId =?,
                                    @floorId =?,
                                    @empType =?,
                                    @empDesignation =?,
                                    @shiftId=?,
                                    @updatedBy =?,
                                    @DOJ=?""",
                                (request.employeeId,
                                request.branchId,
                                request.blockId,
                                request.floorId,
                                request.empType,
                                request.empDesignation,
                                request.shiftId,
                                request.updatedBy,
                                request.DOJ))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
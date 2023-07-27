from fastapi.routing import APIRouter
from routers.config import engine

router=APIRouter(prefix='/userSlot',tags=["userSlot"])

@router.put('')
def putUserSlot(userSlotId:int,slotId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putUserSlot] ?,?""",(userSlotId,slotId))
            rows=result.fetchall()
            return{"statusCode":rows[0][1],"response":rows[0][0]}
            
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}
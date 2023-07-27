from re import S
from sys import prefix
from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response

router = APIRouter(prefix='/generatePin')


@router.get('')
def generatePin():
    try:
        with engine.connect() as cur:
            result = cur.execute(f""" EXEC [dbo].[generatePin]""")

            row = result.fetchone()
            if row[0] != None:
                return {
                    "response":row[0],
                    "statusCode":1
                }
            return Response("NotUpdate")
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}



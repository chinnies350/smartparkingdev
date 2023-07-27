from fastapi.routing import APIRouter
from routers.config import engine,cursorCommit
import schemas
from routers import Response
from fastapi import Query
import json
from joblib import Parallel, delayed
from typing import Optional

router = APIRouter(prefix='/floorImageMaster',tags=['floorMaster'])


def callFunction(i):
    return i.dict()
    
    
@router.put('')
def putfloorImageMaster(request:schemas.PutfloorImageMaster):
    try:
        with engine.connect() as cur:
            if request.floorImageMasterDetails:
                floorImageMasterJson= Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.floorImageMasterDetails)
                floorImageMasterJson=json.dumps(floorImageMasterJson)
            else:
                floorImageMasterJson=None
            conn,cur=cursorCommit()
            result=cur.execute("""
                               EXEC [dbo].[putfloorImageMaster] 
                               @floorImageMasterJson=?,
                               @floorId=?,
                               @updatedBy=?
                               """,
                                (floorImageMasterJson,
                                 request.floorId,
                                 request.updatedBy
                                ))
            row=cur.fetchall()
            conn.commit()
            conn.close()
        
            return {"statusCode": int(row[0][1]), "response": row[0][0]} 

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

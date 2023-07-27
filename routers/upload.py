from fastapi.routing import APIRouter
from routers.config import db, Base_Url
from fastapi import File, UploadFile
import gridfs
from bson import ObjectId
from starlette.responses import StreamingResponse
import io

router = APIRouter(prefix='/Upload', tags=['Upload'])


@router.get('')
def getimage(fileId: str):
    try:
        fileId = fileId.split("=")[-1]
        fileId, fileEtension = fileId.split(".")
        image = fileId
        fs = gridfs.GridFS(db)
        img = fs.get(ObjectId(image))
        return StreamingResponse(io.BytesIO(img.read()), media_type=f"image/{fileEtension}")
    except Exception as e:
        return {"statusCode": 0, "response": str(e)}


@router.post('')
async def create_upload_file(image: UploadFile = File(...)):
    try:
        fileExtension = image.filename.split(".")[-1]
        contents = await image.read()
        fs = gridfs.GridFS(db)
        img = fs.put(contents)
        img_url = Base_Url+"Upload?fileId="+str(img) + '.'+str(fileExtension)
        return {'response': img_url, 'statusCode': 1}
    except Exception as e:
        return {'response': str(e), 'statusCode': 0}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi.middleware.cors import CORSMiddleware

# Inicializa el cliente de Amazon Rekognition
session = boto3.Session(profile_name='default', region_name='us-east-1')
client = session.client('rekognition')

app = FastAPI()

# Configurar CORS para permitir que el frontend se comunique con el backend
origins = ["http://localhost:3000"]  # Cambia esto por el dominio de tu frontend si es necesario
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionIdRequest(BaseModel):
    sessionId: str

@app.get("/api/create-liveness-session")
async def create_liveness_session():
    try:
        response = client.create_face_liveness_session(Settings={"AuditImagesLimit": 2,
                                                                 "OutputConfig": {"S3Bucket": "capturarostro"}})
        session_id = response.get("SessionId")
        return {"sessionId": session_id}
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get-liveness-results")
async def get_liveness_results(sessionId: str):
    try:
        response = client.get_face_liveness_session_results(SessionId=sessionId)
        confidence = response.get("Confidence")
        status = response.get("Status")
        # print(response)
        return {"confidence": confidence, "status": status}
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

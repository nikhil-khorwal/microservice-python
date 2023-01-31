from fastapi import FastAPI,status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from api.api import  orders

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request,exc):
    error_dict={}
    for error in exc.errors():
       error_dict[error['loc'][-1]]=error['msg']
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": error_dict,"code":400}),
    )



@app.get("/")
def check():
    return {"root":"Order service is working"}


app.include_router(orders,prefix="/orders")

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8001,reload=True)




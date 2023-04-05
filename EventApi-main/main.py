from fastapi import FastAPI,Request, status
from config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.feedback_process.organisation import organisation_route
from app.feedback_process.venue import venue_route
from app.feedback_process.meetup import meetup_route
from app.feedback_process.user import user_login_route
from app.feedback_process.event import event_route
from app.feedback_process.organisationdetail import organisationdetail_route
import uvicorn
from fastapi import APIRouter
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from app.auth.auth_bearer import JWTBearer



app = FastAPI()

router = APIRouter()

origins = ["*"]


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    bearer_token = request.headers.get("Authorization")
    print(bearer_token)
    customResponse = {
        "status": False,
        "message": "Not Authenticated !",
        "data": None,
    }
    if not bearer_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=customResponse,
        )
    else:
        if not JWTBearer.verify_jwt(exec, bearer_token):
            customResponse['message'] = "Invalid token or expired token"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=customResponse
            )
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(organisation_route.router)
app.include_router(venue_route.router)
app.include_router(meetup_route.router)
app.include_router(organisationdetail_route.router)
app.include_router(user_login_route.router)
app.include_router(event_route.router)

@app.get("/")
def welcome():
    return "Welcome to Event"


if __name__ == '__main__':
    uvicorn.run("main:app", host='192.168.1.65', port=8000, log_level="info", reload=True)
    print("running")




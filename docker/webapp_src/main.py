from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, String, Integer, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import jwt
import os
import logging


logging.basicConfig(filename="fastapi.log", format='%(asctime)s %(client)s %(levelname)s %(request_method)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DATABASE = os.environ.get("DATABASE", "")
USER = os.environ.get("USER", "admin")
PASSWORD = os.environ.get("PASSWORD", "password")
HOST = os.environ.get("HOST", "")
PORT = os.environ.get("PORT", "5432")
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

# SQLAlchemy Configuration
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, index=True)
    name = Column(String, index=True)
    email = Column(String, primary_key=True, index=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_client(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_data = payload["sub"]
        if client_data is None:
            logger.error("Client data is None")
            raise credentials_exception
        logger.info(f"Token decoded successfully: {payload}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        logger.error("JWT error occurred")
        raise credentials_exception
    return client_data

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "msg": "hello"})


@app.post("/register")
async def signup(request: Request, username: str = Form(), password: str = Form(), email: str = Form()):
    try:
        db = SessionLocal()
        # Check if the user already exists
        user_exists = db.query(exists().where(Client.email == email)).scalar()

        if user_exists:
            logger.warning(f"{request.client.host} {email} user already exists")
            return templates.TemplateResponse("index.html", {"request": request, "register_msg": "User already exists, Please login"})
        else:
            # Create a new user
            new_user = Client(name=username, email=email, password=password)
            db.add(new_user)
            db.commit()

        logger.info(f"{request.client.host} {email} Successfully registered")
        return templates.TemplateResponse("index.html", {"request": request, "msg": "Successfully registered, please login"})
    except Exception as e:
        logger.critical(f"{request.client.host} Internal server error: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "status_code": "500", "msg": "Server under maintenance"})


@app.post("/login")
async def login(request: Request, password: str = Form(), email: str = Form()):
    try:
        db = SessionLocal()
        # print("session created")
        # print(request)
        # Check if the user exists with the correct password
        user = db.query(Client).filter(Client.email == email, Client.password == password).first()

        if user:
            #logger.info(f"{request.client.host} {email} Successfully logged in")
            token_data = {"sub": {"id": user.id, "name": user.name, "email": user.email}}
            token = create_access_token(token_data)
            response = RedirectResponse(url="/dashboard")
            response.set_cookie("token", token)  # Set the token in a cookie if needed
            return response
            # return templates.TemplateResponse("dashboard.html", {"request": request, "username": user.name, "email": user.email, "token": token})
        else:
            # No user exists or incorrect password
            logger.info(f"{request.client.host} {email} Wrong credentials")
            return templates.TemplateResponse("index.html", {"request": request, "msg": "Incorrect Password"})
    except Exception as e:
        logger.critical(f"{request.client.host} Sorry for the Inconvenience, there is some problem from our side: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "status_code": "500", "msg": "Sorry for the Inconvenience, there is some problem from our side"})

@app.get("/dashboard")
async def dashboard(request: Request, current_client: dict = Depends(get_current_client)):
    try:
        # You can access the current client information using the current_client parameter
        username = current_client.get("name")
        email = current_client.get("email")

        return templates.TemplateResponse("dashboard.html", {"request": request, "username": username, "email": email})
    except Exception as e:
        logger.critical(f"{request.client.host} Sorry for the Inconvenience, there is some problem from our side: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "status_code": "500", "msg": "Sorry for the Inconvenience, there is some problem from our side"})


@app.get("/logout")
async def logout(request: Request, current_client: dict = Depends(get_current_client)):
    try:
        logger.info(f"Logout request received")
        # You can perform additional checks related to the token here
        return templates.TemplateResponse("index.html", {"request": request, "msg": "Successfully logged out"})
    except Exception as e:
        logger.critical(f"{request.client.host} Sorry for the Inconvenience, there is some problem from our side: {str(e)}")
        return templates.TemplateResponse("error.html", {"request": request, "status_code": "500", "msg": "Sorry for the Inconvenience, there is some problem from our side"})

@app.get("/read_request_info")
async def read_request_info(request: Request,current_client: dict = Depends(get_current_client)):
    # Accessing request information
    client_host = request.client.host
    http_method = request.method
    url = request.url
    query_parameters = request.query_params
    cookies = request.cookies
    headers = request.headers
    client = request.client

    return {
        "client_host": client_host,
        "http_method": http_method,
        "url": url,
        "query_parameters": query_parameters,
        "cookies": cookies,
        "headers": headers,
        "client": client,
    }

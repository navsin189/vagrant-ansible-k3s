from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
import psycopg2,os
import logging

logging.basicConfig(filename="webapp.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATABASE = os.environ.get("DATABASE"," ")
USER = os.environ.get("USER"," ")
PASSWORD = os.environ.get("PASSWORD"," ")
HOST = os.environ.get("HOST", " ")
PORT = os.environ.get("PORT"," ")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/register/")
async def signup(request: Request,username: str = Form(),password: str = Form(),email: str = Form()):
    try:
        try:
            connection = psycopg2.connect(database=DATABASE, user = USER, password = PASSWORD, host = HOST, port = PORT)
        except:
            logger.critical(f"{request.client.host} {email} Not able to conect to database")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS client(NAME TEXT NOT NULL,PASSWORD TEXT NOT NULL,EMAIL TEXT NOT NULL UNIQUE);''')
        cursor.execute("SELECT EXISTS(SELECT 1 from client WHERE email='{email}' );".format(email=email))
        user_exists = cursor.fetchone()[0]
        #connection.commit()
        if user_exists:
            logger.warning(f"{request.client.host} {email} user already exists")
            return templates.TemplateResponse("index.html",{"request": request,"register_msg":"User already exist, Please login"})
        else:
            cursor.execute("""INSERT INTO client(NAME,EMAIL,PASSWORD) VALUES ('{username}','{email}','{passwd}')""".format(username=username,email=email,passwd=password))
        logger.info(f"{request.client.host} {email} Successfully registered")
        connection.commit()
        connection.close()
        return templates.TemplateResponse("index.html",{"request": request,"msg":"Successfully registered, please login"})
    except:
        logger.critical(f"{request.client.host} intenral server error")
        return templates.TemplateResponse("error.html",{"request": request,"status_code":"500","msg":"Server under maintenance"})


@app.post("/login/")
async def signup(request: Request,password: str = Form(),email: str = Form()):
    try:
        try:
            connection = psycopg2.connect(database=DATABASE, user = USER, password = PASSWORD, host = HOST, port = PORT)
        except:
            logger.critical(f"{request.client.host} Not able to conect to database")
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 from client WHERE email='{email}' );".format(email=email))
        user_exists = cursor.fetchone()[0]
        cursor.execute("SELECT EXISTS(SELECT 1 from client WHERE email='{email}' AND password='{passwd}');".format(email=email,passwd=password))
        user_exists_with_correct_password = cursor.fetchone()[0]
        #connection.close()
        if  user_exists  and user_exists_with_correct_password : # user exists
            cursor.execute("SELECT name from client WHERE email='{email}';".format(email=email))
            username = cursor.fetchone()[0]
            logger.info(f"{request.client.host} {email} Successfully loggedin")
            return templates.TemplateResponse("dashboard.html",{"request": request,"username": username,"email": email})
        elif user_exists_with_correct_password != user_exists: # incorrect password
            logger.info(f"{request.client.host} {email} Wrong credentials")
            return templates.TemplateResponse("index.html",{"request": request,"msg":"Incorrect Password"})
        else: # no user exists
            logger.info(f"{request.client.host} {email} User not exist")
            return templates.TemplateResponse("error.html",{"request": request,"status_code":"403","msg":"User not exist"})

    except:
        logger.critical(f"{request.client.host} Sorry for the Inconvinence, there is some problem from our side")
        return templates.TemplateResponse("error.html",{"request": request,"status_code":"500","msg":"Sorry for the Inconvinence, there is some problem from our side"})
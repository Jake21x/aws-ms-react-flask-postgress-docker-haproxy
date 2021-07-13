
from typing import List
from fastapi import Body,Form,FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import ModelLogin,ModelPromoCompetitor
from .utils import server_generated_id
import databases 
import os,base64
from itertools import chain

app = FastAPI()

# database = databases.Database('postgresql://postgres:mysuperpassword@localhost/youtube')
database = databases.Database('postgres://postgres:jmgtechplays21x@db.pcrwpfgzubsfyfbrczlj.supabase.co:6543/postgres')
UPLOAD_FOLDER = 'uploads' 

auth_handler = AuthHandler()
users = []


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post('/register', status_code=201)
def register(auth_details: ModelLogin):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return


@app.post('/login')
def login(auth_details: ModelLogin):
    user = None
    print('auth_details',auth_details)
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.post('/auth' )
async def auth(data:ModelLogin = Depends()): 
    # vs = data.values()
    # ks = data.keys()
    # return { 'data': data , ks:ks,  vs: vals }
    # item = dict(data)
    # print(item.values())
    # print(item.keys())
    return { 'data': data }


@app.post('/api/promo_competitor' )
async def promo_competitor(json_dict:List[ModelPromoCompetitor]): 
    photo_name = []

    APP_ROOT_UPLOAD = os.path.dirname(os.path.abspath('api-service'))

    print('APP_ROOT_UPLOAD',APP_ROOT_UPLOAD)

    count = len(json_dict)
    for i in chain(range(0,count )): 
        use_id = server_generated_id() 
        if json_dict[i].photo !=".":
            rfile = str('uploads/' + use_id + ".jpg")
            with open(rfile, "wb") as fh:
                photo_name.append( rfile, )
                fh.write(base64.b64decode(json_dict[i].photo))
        else:
            print('no photo')

    list = os.listdir(UPLOAD_FOLDER)
    number_files = len(list) 

    print('json_dict > ', count, number_files)
    return {"FILE ":"ok "}

@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }


@app.get("/db")
async def db():
    return await database.execute('select version()') 
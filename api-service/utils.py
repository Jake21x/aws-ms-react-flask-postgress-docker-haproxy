import datetime,time,random
from random import randint 
import os

BASE_API_URI = '/api/gmsi/mobiletracker'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT_UPLOAD = os.path.dirname(os.path.abspath('api-service'))
UPLOAD_FOLDER = 'uploads' 
UPLOAD_FOLDER_PHOTO = 'uploads/photo/' 
UPLOAD_FOLDER_MEDIA = 'uploads/media/' 
UPLOAD_FOLDER_TEMPLATES = 'uploads/templates/' 

DEV_ROOTPASSPORT = 'root.admin-'
DEV_PASSPORT = 'dev.admin-'


excludeLogin = (
        '9032849083',
        'c_test003',
        'ctorg1001',
        'storg1001',
        'mtorg1001',
        'mgrtorg1001',
        'mtorg10005',
        'rm9999',
    )

def server_generated_id(name="SR",rand=7): 
    candidateChars = "0123456789abcdefghijklmnopqrstuvwxyz"
    length = rand
    sb = ""
    for i in range(0, length):
        sb = sb + str(candidateChars[random.randint(0, len(candidateChars)-1)])
    return name.upper() +(str(datetime.datetime.now().strftime("%y%m%d%H%M%S%f"))+str(sb)).upper()
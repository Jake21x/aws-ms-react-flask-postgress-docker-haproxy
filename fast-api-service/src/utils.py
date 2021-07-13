import datetime,random
from random import randint 

def server_generated_id(): 
    candidateChars = "0123456789abcdefghijklmnopqrstuvwxyz"
    length = 7
    sb = ""
    for i in range(0, length):
        sb = sb + str(candidateChars[random.randint(0, len(candidateChars)-1)])
    return 'SR'+(str(datetime.datetime.now().strftime("%y%m%d%H%M%S%f"))+str(sb)).upper()
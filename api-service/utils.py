import datetime,time,random
from random import randint 

def server_generated_id(name="SR",rand=7): 
    candidateChars = "0123456789abcdefghijklmnopqrstuvwxyz"
    length = rand
    sb = ""
    for i in range(0, length):
        sb = sb + str(candidateChars[random.randint(0, len(candidateChars)-1)])
    return name.upper() +(str(datetime.datetime.now().strftime("%y%m%d%H%M%S%f"))+str(sb)).upper()
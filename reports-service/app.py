from flask import Flask
import time
import os

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    port = int(os.environ.get('PORT', 5000))
    return { "time":time.time() , "port":port }

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
from flask_restful import Resource
from database import Database 

class ApiAppVersion(Resource):
    def get(self):
        conn = Database() 

        cursor = conn.execute("select version,mdc,coor_mgr from app_versions order by date_created desc limit 1",result=True)
        version = cursor.fetchall()
        # print('ApiAppVersion > version',version)
        
        return  [{
                'version': version[0][0],
                'mdc':version[0][1],
                'coor_mgr':version[0][2],
                'pdf':'http://gmsi.torgph.com:5000/static/uploads/pdf/mnc_bread_planogram.pdf'

            }]
import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER
from flask_restful import Resource,request
from database import Database 

class ApiUploadArea(Resource):
    def post(self):   
        conn = Database() 
        template = request.files['file']  
        return UploadArea(conn,template)

def UploadArea(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
        
    if template.filename != '':
        filename = server_generated_id('area',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        for r in range(1, sheet.nrows):
            id = str(sheet.cell(r, 0).value).replace('.0', '')
            name = str(sheet.cell(r, 1).value).replace('.0', '')
            agencyid = str(sheet.cell(r, 2).value).replace('.0', '')
            data.append((id,name,agencyid))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into areas (areaid,name,agencyid) values {}
            ON CONFLICT (areaid) DO UPDATE 
            SET (name,agencyid,date_updated) = (EXCLUDED.name,EXCLUDED.agencyid,now());
            """.format(args_str) , data , commit=True)  
        except psycopg2.OperationalError as err:
            # print('err',err)
            result = {
                'status': 'error',
                'message':'Please check your network '+str(err)
            }
        except psycopg2.errors.SyntaxError as err:
            print('err',err)
            result = {
                'status': 'error',
                'message':'Transcation Query '+str(err)
            } 
        except psycopg2.errors.DuplicateColumn as err:
            print('err',err)
            result = {
                'status': 'error',
                'message':'Duplicated '+str(err)
            } 
        print('result',query) 
    return result 
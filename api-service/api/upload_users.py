import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER
import hashlib
from flask_restful import Resource,request
from database import Database 

class ApiUploadUsers(Resource):
    def post(self):
        conn = Database()  
        template = request.files['file']  
        return UploadUsers(conn,template) 

def UploadUsers(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
    
        
    if template.filename != '':
        filename = server_generated_id('users',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0) 

        for r in range(1, sheet.nrows):
            code = str(sheet.cell(r, 0).value).replace('.0', '')
            agencyid = str(sheet.cell(r, 1).value).replace('.0', '')
            posid = str(sheet.cell(r, 2).value).replace('.0', '')
            username = str(sheet.cell(r, 3).value).replace('.0', '')
            
            password = str(sheet.cell(r, 4).value).replace('.0', '') 
            encryped_password = hashlib.md5(password.encode()).hexdigest()
            
            firstname = str(sheet.cell(r, 5).value).replace('.0', '')
            lastname = str(sheet.cell(r, 6).value).replace('.0', '')
            
            active_row = 'Yes'
            try:
                active_row = str(sheet.cell(r, 7).value).replace('.0', '')
            except:
                print('n column')
            active = 'Yes' if str(active_row).strip() == '' else active_row 
            print(active)
            
            data.append((code,code,posid,username,encryped_password,firstname,lastname,agencyid,active))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into users (employeeid,userid,roleid,username,password,firstname,lastname,agencyid,active) values {}
            ON CONFLICT (userid) DO UPDATE 
            SET (employeeid,roleid,username,password,firstname,lastname,agencyid,active,date_updated) = 
                (
                    EXCLUDED.employeeid,
                    EXCLUDED.roleid,
                    EXCLUDED.username,
                    EXCLUDED.password,
                    EXCLUDED.firstname,
                    EXCLUDED.lastname,
                    EXCLUDED.agencyid,
                    EXCLUDED.active,
                    now()
                );
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
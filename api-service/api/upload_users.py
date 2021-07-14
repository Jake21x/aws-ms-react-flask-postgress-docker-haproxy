import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER
import hashlib

def UploadUsers(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
    
        
    if template.filename != '':
        filename = server_generated_id('users_',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER, filename)
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
            data.append((code,code,posid,username,encryped_password,firstname,lastname,agencyid))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into users (employeeid,userid,roleid,username,password,firstname,lastname,agencyid) values {}
            ON CONFLICT (userid) DO UPDATE 
            SET (employeeid,roleid,username,password,firstname,lastname,agencyid) = 
                (
                    EXCLUDED.employeeid,
                    EXCLUDED.roleid,
                    EXCLUDED.username,
                    EXCLUDED.password,
                    EXCLUDED.firstname,
                    EXCLUDED.lastname,
                    EXCLUDED.agencyid
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
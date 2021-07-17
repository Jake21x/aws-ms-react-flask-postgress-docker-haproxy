import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER

def UploadUsersSchedules(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
        
    if template.filename != '':
        filename = server_generated_id('usersscheds',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0) 

        for r in range(1, sheet.nrows):
            storeid = str(sheet.cell(r, 0).value).replace('.0', '')
            userid = str(sheet.cell(r, 1).value).replace('.0', '')
            sched_type = str(sheet.cell(r, 2).value).replace('.0', '')
            working_time = str(sheet.cell(r, 3).value).replace('.0', '')
            dayoff = str(sheet.cell(r, 4).value).replace('.0', '')
            shift = str(sheet.cell(r, 5).value).replace('.0', '')

            data.append((storeid,userid,sched_type,working_time,dayoff,shift))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into users_schedules (storeid,userid,schedule_type,working_time,day_off,shift) values {}
            ON CONFLICT (storeid,userid) DO UPDATE 
            SET (schedule_type,working_time,day_off,shift) = 
                (
                    EXCLUDED.schedule_type,
                    EXCLUDED.working_time,
                    EXCLUDED.day_off,
                    EXCLUDED.shift
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
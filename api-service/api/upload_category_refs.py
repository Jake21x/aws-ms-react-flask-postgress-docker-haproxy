import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER
import hashlib

def UploadCategoryRefs(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
    
        
    if template.filename != '':
        filename = server_generated_id('catrefs',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0) 

        for r in range(1, sheet.nrows):
            refid = str(sheet.cell(r, 0).value).replace('.0', '')
            catid = str(sheet.cell(r, 1).value).replace('.0', '')
            cat_name = str(sheet.cell(r, 2).value).replace('.0', '')
            segment = str(sheet.cell(r, 3).value).replace('.0', '') 
            brand = str(sheet.cell(r, 5).value).replace('.0', '')
            percent_share = str(sheet.cell(r, 6).value).replace('.0', '')
            facing_count = str(sheet.cell(r, 7).value).replace('.0', '')
            pulloutday = str(sheet.cell(r, 8).value).replace('.0', '')
            facing_segment = str(sheet.cell(r, 9).value).replace('.0', '')
            facing_brand = str(sheet.cell(r, 10).value).replace('.0', '')
            data.append((refid,catid,cat_name,segment,brand,percent_share,facing_count,pulloutday,facing_segment,facing_brand))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into category_refs (refsid,catid,cat_name,segment,brand,percent_share,facing_count,pulloutday,facing_segment,facing_brand) values {}
            ON CONFLICT (catid,refsid) DO UPDATE 
            SET (segment,brand,percent_share,facing_count,pulloutday,facing_segment,facing_brand,date_updated) = 
                (
                    EXCLUDED.segment,
                    EXCLUDED.brand,
                    EXCLUDED.percent_share,
                    EXCLUDED.facing_count,
                    EXCLUDED.pulloutday,
                    EXCLUDED.facing_segment,
                    EXCLUDED.facing_brand,
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
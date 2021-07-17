import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER

def UploadStores(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
        
    if template.filename != '':
        filename = server_generated_id('stores',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        for r in range(1, sheet.nrows):
            code = str(sheet.cell(r, 0).value).replace('.0', '') 
            agencyid = str(sheet.cell(r, 1).value).replace('.0', '')
            chainid = str(sheet.cell(r, 2).value).replace('.0', '')
            areaid = str(sheet.cell(r, 3).value).replace('.0', '')
            channelid = str(sheet.cell(r, 4).value).replace('.0', '')
            name = str(sheet.cell(r, 5).value).replace('.0', '')
            longitude = str(sheet.cell(r, 6).value).replace('.0', '')
            latitude = str(sheet.cell(r, 7).value).replace('.0', '')
            geofence = str(sheet.cell(r, 8).value).replace('.0', '')
            geofence = '1000' if geofence == '' else geofence
            address = str(sheet.cell(r, 9).value).replace('.0', '')
            zipcode = str(sheet.cell(r, 10).value).replace('.0', '') 
            data.append((channelid,chainid,areaid,code,code,name,zipcode,geofence,longitude,latitude,address,agencyid))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into stores (channelid,chainid,areaid,storecode,storeid,name,zipcode,geofence,longitude,latitude,address,agencyid) values {}
            ON CONFLICT (storeid) DO UPDATE 
            SET (channelid,chainid,areaid,storecode,name,zipcode,geofence,longitude,latitude,address,agencyid) = 
                (
                    EXCLUDED.channelid,
                    EXCLUDED.chainid,
                    EXCLUDED.areaid,
                    EXCLUDED.storecode,
                    EXCLUDED.name,
                    EXCLUDED.zipcode,
                    EXCLUDED.geofence,
                    EXCLUDED.longitude,
                    EXCLUDED.latitude,
                    EXCLUDED.address,
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
import os
from utils import server_generated_id
import psycopg2
import xlrd
from utils import UPLOAD_FOLDER 
import datetime
from flask_restful import Resource,request
from database import Database  

class ApiUploadSKUs(Resource):
    def post(self):   
        conn = Database()  
        template = request.files['file']  
        return UploadSKUs(conn,template) 

def UploadSKUs(conn,template): 
    data = []
    result = {'status': 'success','message':'sucess'}
        
    if template.filename != '':
        filename = server_generated_id('skus',2)+'.'+ template.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_FOLDER+'/templates', filename)
        template.save(file_path)

        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        for r in range(1, sheet.nrows):
            refid = str(sheet.cell(r, 0).value).replace('.0', '')
            catid = str(sheet.cell(r, 1).value).replace('.0', '') 
            skuid = str(sheet.cell(r, 2).value).replace('.0', '')
            sap_name = str(sheet.cell(r, 3).value).replace('.0', '')
            case_barcode = str(sheet.cell(r, 4).value).replace('.0', '')
            product_barcode = str(sheet.cell(r, 5).value).replace('.0', '')
            gross_price_case = str(sheet.cell(r, 6).value).replace('.0', '')
            gross_price_piece = str(sheet.cell(r, 7).value).replace('.0', '')
            quantity_per_case = str(sheet.cell(r, 8).value).replace('.0', '')
            packsize = str(sheet.cell(r, 9).value).replace('.0', '')
            unit_of_measure = str(sheet.cell(r, 10).value).replace('.0', '')
            active = str(sheet.cell(r, 11).value).replace('.0', '')
            image_path = str(sheet.cell(r, 12).value).replace('.0', '')
            size = str(sheet.cell(r, 13).value).replace('.0', '')
            form = str(sheet.cell(r, 14).value).replace('.0', '')
            packaging_description = str(sheet.cell(r, 15).value).replace('.0', '')
            remarks = str(sheet.cell(r, 16).value).replace('.0', '')
            packs_or_bags = str(sheet.cell(r, 17).value).replace('.0', '')
            data.append((refid,catid,skuid,skuid,sap_name,case_barcode,product_barcode,gross_price_case,gross_price_piece,quantity_per_case,packsize,unit_of_measure,active,image_path,size,form,packaging_description,remarks,packs_or_bags))
            
    print('template',data)
    query = None
    if len(data) != 0:
        
        args_str = ','.join(['%s'] * len(data)) 
        try:
            query = conn.mogrify("""
            insert into skus (refid,catid,skucode,skuid,sap_name,case_barcode,product_barcode,gross_price_case,gross_price_piece,quantity_per_case,packsize,unit_of_measure,active,image_path,size,form,packaging_description,remarks,packs_or_bags) values {}
            ON CONFLICT (skuid) DO UPDATE 
            SET (refid,catid,skucode,sap_name,case_barcode,product_barcode,gross_price_case,gross_price_piece,quantity_per_case,packsize,unit_of_measure,active,image_path,size,form,packaging_description,remarks,packs_or_bags,date_updated) = 
                (
                    EXCLUDED.refid,
                    EXCLUDED.catid,
                    EXCLUDED.skucode,
                    EXCLUDED.sap_name,
                    EXCLUDED.case_barcode,
                    EXCLUDED.product_barcode,
                    EXCLUDED.gross_price_case,
                    EXCLUDED.gross_price_piece,
                    EXCLUDED.quantity_per_case,
                    EXCLUDED.packsize,
                    EXCLUDED.unit_of_measure,
                    EXCLUDED.active,
                    EXCLUDED.image_path,
                    EXCLUDED.size,
                    EXCLUDED.form,
                    EXCLUDED.packaging_description,
                    EXCLUDED.remarks,
                    EXCLUDED.packs_or_bags,
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
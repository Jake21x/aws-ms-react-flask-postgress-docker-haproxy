from flask_restful import Resource,request
from utils import server_generated_id,UPLOAD_FOLDER_MEDIA
from database import Database  
from itertools import chain 
import psycopg2 
import os

class ApiPostStoreAuditData(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mobile_generated_id'] 
                json_dict[i]['mobile_generated_id'] = server_generated_id() if gid in ('.','') else gid

                data.append((
                    json_dict[i]['store_id'],
                    json_dict[i]['store_name'],
                    json_dict[i]['auditor_usercode'],
                    json_dict[i]['auditor_name'],
                    json_dict[i]['ac_usercode'],
                    json_dict[i]['ac_name'],
                    json_dict[i]['tl_usercode'],
                    json_dict[i]['tl_name'],
                    json_dict[i]['agency'],
                    json_dict[i]['avail_refil_per_sku'],
                    json_dict[i]['avail_refil_per_sku_remarks'],
                    json_dict[i]['bo_mgt_per_category'],
                    json_dict[i]['bo_mgt_per_category_remarks'],
                    json_dict[i]['vst_and_p_completed'],
                    json_dict[i]['vst_and_p_completed_remarks'],
                    json_dict[i]['vm_and_p_mass_display'],
                    json_dict[i]['vm_and_p_mass_display_remarks'],
                    json_dict[i]['vm_and_p_tactical_bin'],
                    json_dict[i]['vm_and_p_tactical_bin_remarks'],
                    json_dict[i]['vm_and_p_in_store_exec'],
                    json_dict[i]['vm_and_p_in_store_exec_remarks'],
                    json_dict[i]['vm_and_p_in_store_promo'],
                    json_dict[i]['vm_and_p_in_store_promo_remarks'],
                    json_dict[i]['bp_acp_total_acp_score'],
                    json_dict[i]['bp_acp_acp_1'],
                    json_dict[i]['bp_acp_type_of_acp_1'],
                    json_dict[i]['bp_acp_location_1'],
                    json_dict[i]['bp_acp_acp_1_score'],
                    json_dict[i]['bp_acp_acp_2'],
                    json_dict[i]['bp_acp_type_of_acp_2'],
                    json_dict[i]['bp_acp_location_2'],
                    json_dict[i]['bp_acp_acp_2_score'],
                    json_dict[i]['bp_acp_acp_3'],
                    json_dict[i]['bp_acp_type_of_acp_3'],
                    json_dict[i]['bp_acp_location_3'],
                    json_dict[i]['bp_acp_acp_3_score'],
                    json_dict[i]['bp_acp_acp_4'],
                    json_dict[i]['bp_acp_type_of_acp_4'],
                    json_dict[i]['bp_acp_location_4'],
                    json_dict[i]['bp_acp_acp_4_score'],
                    json_dict[i]['bp_acp_acp_5'],
                    json_dict[i]['bp_acp_type_of_acp_5'],
                    json_dict[i]['bp_acp_location_5'],
                    json_dict[i]['bp_acp_acp_5_score'],
                    json_dict[i]['bp_acp_acp_6'],
                    json_dict[i]['bp_acp_type_of_acp_6'],
                    json_dict[i]['bp_acp_location_6'],
                    json_dict[i]['bp_acp_acp_6_score'],
                    json_dict[i]['other_remarks'],
                    json_dict[i]['total_score'],
                    json_dict[i]['media'],
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['date_created'],
                    json_dict[i]['date_updated'],
                    json_dict[i]['vst_and_p_implemented'],
                    json_dict[i]['vst_and_p_implemented_remarks'],
                ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_storeaudit (store_id, store_name, auditor_usercode, auditor_name, ac_usercode, ac_name, tl_usercode, tl_name, agency, avail_refil_per_sku, avail_refil_per_sku_remarks, bo_mgt_per_category, bo_mgt_per_category_remarks, vst_and_p_completed, vst_and_p_completed_remarks, vm_and_p_mass_display, vm_and_p_mass_display_remarks, vm_and_p_tactical_bin, vm_and_p_tactical_bin_remarks, vm_and_p_in_store_exec, vm_and_p_in_store_exec_remarks, vm_and_p_in_store_promo, vm_and_p_in_store_promo_remarks, bp_acp_total_acp_score, bp_acp_acp_1, bp_acp_type_of_acp_1, bp_acp_location_1, bp_acp_acp_1_score, bp_acp_acp_2, bp_acp_type_of_acp_2, bp_acp_location_2, bp_acp_acp_2_score, bp_acp_acp_3, bp_acp_type_of_acp_3, bp_acp_location_3, bp_acp_acp_3_score, bp_acp_acp_4, bp_acp_type_of_acp_4, bp_acp_location_4, bp_acp_acp_4_score, bp_acp_acp_5, bp_acp_type_of_acp_5, bp_acp_location_5, bp_acp_acp_5_score, bp_acp_acp_6, bp_acp_type_of_acp_6, bp_acp_location_6, bp_acp_acp_6_score, other_remarks, total_score, media, mobile_generated_id, date_created, date_updated,vst_and_p_implemented,vst_and_p_implemented_remarks) values {}
                ON CONFLICT (mobile_generated_id) DO NOTHING;
                """.format(args_str) , data , commit=True) 
        
            return {'status' : 'success', 'message' : 'success'}

        except psycopg2.ProgrammingError as exc:
            return {'status' : 'failed', 'message' : str(exc)}
            
        except BaseException as e:
            return {'status' : 'failed', 'message' : str(e)}
        except Exception as e:
            x = str(e)
            x.replace('\n', '')
            return {'status' : 'failed', 'message' : str(x)}
        finally:
            print("completed")


class ApiPostStoreAuditImages(Resource):
    def post(self):

        conn = Database() 
        sitelink = '/uploads/media/'
        # try: 

        data = []

        print(request.form['store_id'])
        
        store_id = request.form['store_id']
        store_name = request.form['store_name']
        auditor_usercode = request.form['auditor_usercode']
        auditor_name = request.form['auditor_name']
        ac_usercode = request.form['ac_usercode']
        ac_name = request.form['ac_name']
        tl_usercode = request.form['tl_usercode']
        tl_name = request.form['tl_name']
        agency = request.form['agency'] 
        mobile_generated_id = request.form['mobile_generated_id']

        filename1 = ''
        try:
            media1 = request.files['media1']
            if media1.filename != '':
                print('media1', media1)
                filename1 = str(mobile_generated_id) + '_acp1.' + \
                    media1.filename.split(".")[-1]
                media1.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename1))
                filename1 = sitelink + filename1
        except:
            print('no file or invalid 1')

        filename2 = ''
        try:
            media2 = request.files['media2']
            if media2.filename != '':
                print('media2', media2)
                filename2 = str(mobile_generated_id) + '_acp2.' + \
                    media2.filename.split(".")[-1]
                media2.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename2))
                filename2 = sitelink + filename2
        except:
            print('no file or invalid 2')

        filename3 = ''
        try:
            media3 = request.files['media3']
            if media3.filename != '':
                print('media3', media3)
                filename3 = str(mobile_generated_id) + '_acp3.' + \
                    media3.filename.split(".")[-1]
                media3.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename3))
                filename3 = sitelink + filename3
        except:
            print('no file or invalid 3')

        filename4 = ''
        # try:
        media4 = request.files['media4'] 
        if media4.filename != '':
            print('media4', media4)
            filename4 = str(mobile_generated_id) + '_acp4.' + \
                media4.filename.split(".")[-1]
            media4.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename4))
            filename4 = sitelink + filename4
        # except:
        #     print('no file or invalid 4')

        filename5 = ''
        try:
            media5 = request.files['media5']
            if media5.filename != '':
                print('media5', media5)
                filename5 = str(mobile_generated_id) + '_acp5.' + \
                    media5.filename.split(".")[-1]
                media5.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename5))
                filename5 = sitelink + filename5
        except:
            print('no file or invalid 5')

        filename6 = ''
        try:
            media6 = request.files['media6']
            if media6.filename != '':
                print('media6', media6)
                filename6 = str(mobile_generated_id) + '_acp6.' + \
                    media6.filename.split(".")[-1]
                media6.save(os.path.join(UPLOAD_FOLDER_MEDIA, filename6))
                filename6 = sitelink + filename6

        except:
            print('no file or invalid 6')

        date_created = request.form['date_created']
        date_updated = request.form['date_updated']
        
        data.append((store_id,
                store_name,
                auditor_usercode,
                auditor_name,
                ac_usercode,
                ac_name,
                tl_usercode,
                tl_name,
                agency,
                filename1,
                filename2,
                filename3,
                filename4,
                filename5,
                filename6,
                mobile_generated_id,
                date_created,
                date_updated))

        args_str = ','.join(['%s'] * len(data)) 
        query = conn.mogrify("""
            insert into m_storeaudit_media (store_id, store_name, auditor_usercode, auditor_name, ac_usercode, ac_name, tl_usercode, tl_name, agency, media,media1,media2,media3,media4,media5, mobile_generated_id, date_created, date_updated) values {}
            """.format(args_str) , data , commit=True) 
    
        return {'status' : 'success', 'message' : 'success'}

        # except psycopg2.ProgrammingError as exc:
        #     return {'status' : 'failed', 'message' : str(exc)}
            
        # except BaseException as e:
        #     return {'status' : 'failed', 'message' : str(e)}
        # except Exception as e:
        #     x = str(e)
        #     x.replace('\n', '')
        #     return {'status' : 'failed', 'message' : str(x)}
        # finally:
        #     print("completed")
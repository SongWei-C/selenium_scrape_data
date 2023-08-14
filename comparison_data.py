import json
import logging
from Teams_webhook import TeamsAlerter
import time
class Data_Verification:
    def __init__(self, std_sample, verify_data):
        self.total_message = []
        if isinstance(std_sample, str) and isinstance(verify_data, str):
            with open(std_sample, newline='') as jsonfile:
                self.std_sample:dict = json.load(jsonfile)
            with open(verify_data, newline='') as jsonfile:
                self.verify_data:dict = json.load(jsonfile)
        elif isinstance(std_sample, dict) and isinstance(verify_data, dict):
            self.std_sample:dict = std_sample
            self.verify_data:dict = verify_data
        elif isinstance(std_sample, str) and isinstance(verify_data, dict):
            with open(std_sample, newline='') as jsonfile:
                self.std_sample:dict = json.load(jsonfile)
            self.verify_data:dict = verify_data
        else:
            raise TypeError('std_sample and verify_data must be str(Json file path) or dict types')

    def verification_with_json(self,):
        report_dict = {
            'verification': False,
            'logging':[],
            'message':[]
        }

        for lang_code in self.std_sample.keys():
            temp_log = {
                'language': lang_code,
                'verification': False,
                'url': self.verify_data[lang_code]['url'],
                'table_logging': {'verify': False},
                'content_logging': {'verify': False}
            }
            # get different language object
            std_lang_obj = self.std_sample[lang_code]
            verify_lang_obj = self.verify_data[lang_code]

            # 判斷 Table 內容是否相同
            if std_lang_obj['table'] != verify_lang_obj['table']:
                warn = "Warning:[Table](" + lang_code + ") The standard sample is not the same as the verification data."
                logging.warning(warn)
                # print('table!')
                # print(std_lang_obj['table'])
                # print(verify_lang_obj['table'])
                temp_log['table_logging']['verify'] = False
                temp_log['table_logging']['error_message'] = []

                if std_lang_obj['table'] == None and verify_lang_obj['table'] != None:
                    message = '[The number of Table is different]:\nStandard Sample('+std_lang_obj['url']+') not find any table.'
                    temp_log['table_logging']['error_message'].append(message)
                elif std_lang_obj['table'] != None and verify_lang_obj['table'] == None:
                    message = '[The number of Table is different]:\nValidation Data(' + verify_lang_obj['url'] + ') not find any table.'
                    temp_log['table_logging']['error_message'].append(message)
                else: # 檢查彼此表格 1.表格數量 2.table head 3. table body
                    if len(std_lang_obj['table']) != len(verify_lang_obj['table']):
                        message = '[The number of Table is different]:'+str(len(std_lang_obj['table'])) + \
                                  'tables found in Standard sample('+std_lang_obj['url'] + ')but\n '+ \
                            str(len(verify_lang_obj['table'])) + 'tables found in Validation Data(' + verify_lang_obj['url'] + ')'
                        temp_log['table_logging']['error_message'].append(message)

                    else:
                        for i in range(len(std_lang_obj['table'])):
                            std_table = std_lang_obj['table'][i]
                            val_table = verify_lang_obj['table'][i]
                            # 檢查table head row數量
                            if std_table['thead'] == None and val_table['thead'] != None:
                                message = '[The number of Table head rows is different]:\nIn'+ str(i)+'Table in Standard Sample(' + std_lang_obj[
                                    'url'] + ') not find any table head row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['thead'] != None and val_table == None:
                                message = '[The number of Table head rows is different]:\nIn'+ str(i)+'Table in Validation Data(' + verify_lang_obj[
                                    'url'] + ') not find any table head row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['thead'] != None and val_table['thead'] != None:  # 檢查彼此表格 1.表格數量 2.table head 3. table body
                                if len(std_table['thead']) != len(val_table['thead']):
                                    message = '[The number of Table head rows is different]:\nIn'+ str(i)+'Table ' + str(len(std_table['thead'])) + \
                                              'table head rows found in '+ str(i) +'Table in Standard sample(' + std_lang_obj['url'] + ')but\n ' + \
                                              str(len(val_table['thead'])) + 'table head rows found in '+ str(i) +'Table in Validation Data(' + \
                                              verify_lang_obj['url'] + ')'
                                    temp_log['table_logging']['error_message'].append(message)
                                else: # 檢查每個row元素
                                    for j in range(len(std_table['thead'])):
                                        std_row_th = std_table['thead'][j]['th']
                                        val_row_th = val_table['thead'][j]['th']

                                        if std_row_th == None and val_row_th != None:
                                            message = '[The number of thead <th> is different]:\nIn'+ str(i)+'Table '+ str(j) +'Thead Row in Standard Sample(' + \
                                                      std_lang_obj['url'] + ') not find any table head <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th == None:
                                            message = '[The number of thead <th> is different]:\nIn'+ str(i)+'Table '+ str(j) +'Thead Row in Validation Data(' + \
                                                      verify_lang_obj['url'] + ') not find any table head <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th != None:
                                            if len(std_row_th) != len(val_row_th):
                                                message = '[The number of thead <th> is different]:\nIn'+ str(i)+'Table ' + str(j) + 'Thead Row\n ->' +\
                                                          'Standard sample(' + std_lang_obj['url'] + ') find'+ str(len(std_row_th)) + ' <th>, \n ->' + \
                                                          'Validation Data(' + verify_lang_obj['url'] + ') find' + str(len(val_row_th)) + ' <th>'
                                                temp_log['table_logging']['error_message'].append(message)
                                            else:  # 檢查th元素
                                                for k in range(len(val_row_th)):
                                                    std_th_ele = std_row_th[k]
                                                    val_th_ele = val_row_th[k]

                                                    if std_th_ele == val_th_ele:
                                                        continue
                                                    else:
                                                        message = '[Table Content different]:\nIn '+ str(i)+'Table ' \
                                                                  + str(j) + 'Thead Row ' + str(k)+'<th> ->\n' \
                                                                  + 'Standard sample(' + std_lang_obj['url'] + '): '\
                                                                  + std_th_ele +'\n'\
                                                                  + 'Validation Data(' + verify_lang_obj['url'] + '): '\
                                                                  + val_th_ele + ''
                                                        temp_log['table_logging']['error_message'].append(message)


                            #----------------------------------------------------------------------------------------------
                            # 檢查table body row數量
                            if std_table['tbody'] == None and val_table['tbody'] != None:
                                message = '[The number of Table body rows is different]:\nStandard Sample(' + \
                                          std_lang_obj['url'] + ') not find any table body row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['tbody'] != None and val_table['tbody'] == None:
                                message = '[The number of Table body rows is different]:\nValidation Data(' + \
                                          verify_lang_obj[
                                              'url'] + ') not find any table body row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['tbody'] != None and val_table['tbody'] != None:
                                if len(std_table['tbody']) != len(val_table['tbody']):
                                    message = '[The number of Table body rows is different]:\n' + str(
                                        len(std_table['tbody'])) + 'table body rows found in '+ str(i) +\
                                              'Table in Standard sample(' + std_lang_obj['url'] +\
                                              ')but\n ' + str(len(val_table['tbody'])) + 'table body rows found in '+\
                                              str(i) +'Table in  Validation Data(' + verify_lang_obj['url'] + ')'
                                    temp_log['table_logging']['error_message'].append(message)
                                else: # 檢查每個row元素
                                    for j in range(len(std_table['tbody'])):
                                        std_row_th = std_table['tbody'][j]['th']
                                        val_row_th = val_table['tbody'][j]['th']
                                        std_row_td = std_table['tbody'][j]['td']
                                        val_row_td = val_table['tbody'][j]['td']

                                        # 檢查th list
                                        if std_row_th == None and val_row_th != None:
                                            message = '[The number of tbody <th> is different]:\nIn' + str(
                                                i) + 'Table '+ str(j) +'Tbody Row in Standard Sample(' + \
                                                      std_lang_obj['url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th == None:
                                            message = '[The number of tbody <th> is different]:\nIn' + str(
                                                i) + 'Table '+ str(j) +'Tbody Row in Validation Data(' + \
                                                      verify_lang_obj['url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th != None:
                                            if len(std_row_th) != len(val_row_th):
                                                message = '[The number of tbody <th> is different]:\nIn' + str(
                                                    i) + 'Table ' + str(j) + 'Tbody Row\n ->' + \
                                                          'Standard sample(' + std_lang_obj['url'] + ') find' + str(
                                                    len(std_row_th)) + ' <th>, \n ->' + \
                                                          'Validation Data(' + verify_lang_obj['url'] + ') find' + str(
                                                    len(val_row_th)) + ' <th>'
                                                temp_log['table_logging']['error_message'].append(message)
                                            else:  # 檢查th元素
                                                for k in range(len(val_row_th)):
                                                    std_th_ele = std_row_th[k]
                                                    val_th_ele = val_row_th[k]

                                                    if std_th_ele == val_th_ele:
                                                        continue
                                                    else:
                                                        message = '[Table Content different]:\nIn ' + str(i) + 'Table ' \
                                                                  + str(j) + 'Tbody Row ' + str(k) + '<th> ->\n' \
                                                                  + 'Standard sample(' + std_lang_obj['url'] + '): ' \
                                                                  + std_th_ele + '\n' \
                                                                  + 'Validation Data(' + verify_lang_obj['url'] + '): ' \
                                                                  + val_th_ele + ''
                                                        temp_log['table_logging']['error_message'].append(message)

                                        # 檢查td list
                                        if std_row_td == None and val_row_td != None:
                                            message = '[The number of tbody <td> is different]:\nIn' + str(
                                                i) + 'Table ' + str(
                                                j) + 'Tbody Row in Standard Sample(' + \
                                                      std_lang_obj[
                                                          'url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_td != None and val_row_td == None:
                                            message = '[The number of tbody <td> is different]:\nIn' + str(
                                                i) + 'Table ' + str(
                                                j) + 'Tbody Row in Validation Data(' + \
                                                      verify_lang_obj[
                                                          'url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_td != None and val_row_td != None:
                                            if len(std_row_td) != len(val_row_td):
                                                message = '[The number of tbody <td> is different]:\nIn' + str(
                                                    i) + 'Table ' + str(j) + 'Tbody Row\n ->' + \
                                                          'Standard sample(' + std_lang_obj[
                                                              'url'] + ') find' + str(
                                                    len(std_row_td)) + ' <td>, \n ->' + \
                                                          'Validation Data(' + verify_lang_obj[
                                                              'url'] + ') find' + str(
                                                    len(val_row_td)) + ' <td>'
                                                temp_log['table_logging']['error_message'].append(
                                                    message)
                                            else:  # 檢查td元素
                                                for k in range(len(val_row_td)):
                                                    std_td_ele = std_row_td[k]
                                                    val_td_ele = val_row_td[k]

                                                    if std_td_ele == val_td_ele:
                                                        continue
                                                    else:
                                                        message = '[Table Content different]:\nIn ' + str(
                                                            i) + 'Table ' \
                                                                  + str(j) + 'Tbody Row ' + str(
                                                            k) + '<td> ->\n' \
                                                                  + 'Standard sample(' + std_lang_obj[
                                                                      'url'] + '): "' \
                                                                  + std_td_ele + '"\n' \
                                                                  + 'Validation Data(' + \
                                                                  verify_lang_obj['url'] + '): "' \
                                                                  + val_td_ele + '"'
                                                        temp_log['table_logging'][
                                                            'error_message'].append(message)
            else:
                # print('Table 相同')
                temp_log['table_logging']['verify'] = True


            # 判斷(文字)內容是否相同
            if std_lang_obj['content'] != verify_lang_obj['content']:
                warn = "Warning:[Content](" + lang_code + ") The standard sample is not the same as the verification data."
                logging.warning(warn)
                temp_log['content_logging']['verify'] = False
                temp_log['content_logging']['error_message'] = []

                message = '[Content different]:\nStandard sample('+std_lang_obj['url']+'):\n'+ str(std_lang_obj['content']) \
                            + '\n\nValidation Data(' + verify_lang_obj['url'] +'):\n' + str(verify_lang_obj['content'])
                temp_log['content_logging']['error_message'].append(message)
                # print('content!')
                # print(std_lang_obj['content'])
                # print(verify_lang_obj['content'])

            else:
                # print('Content 相同')
                temp_log['content_logging']['verify'] = True

            if temp_log['content_logging']['verify'] and temp_log['table_logging']['verify']:
                temp_log['verification'] = True

            # 加入紀錄中
            report_dict['logging'].append(temp_log)

        validation_status = [ log['verification'] for log in report_dict['logging']]
        if all(validation_status):
            report_dict['verification'] = True

        return report_dict

class Reptile_Data_Verification:
    def __init__(self, std_sample, verify_data):
        self.total_message = []
        if isinstance(std_sample, str) and isinstance(verify_data, str):
            with open(std_sample, newline='', encoding='utf-8') as jsonfile:
                self.std_sample:dict = json.load(jsonfile)
            with open(verify_data, newline='', encoding='utf-8') as jsonfile:
                self.verify_data:dict = json.load(jsonfile)
        elif isinstance(std_sample, dict) and isinstance(verify_data, dict):
            self.std_sample:dict = std_sample
            self.verify_data:dict = verify_data
        elif isinstance(std_sample, str) and isinstance(verify_data, dict):
            with open(std_sample, newline='', encoding='utf-8') as jsonfile:
                self.std_sample:dict = json.load(jsonfile)
            self.verify_data:dict = verify_data
        else:
            raise TypeError('std_sample and verify_data must be str(Json file path) or dict types')

    def verification_with_json(self):
        report_dict = {
            'verification': True,
            'logging': []
        }
        for lang_code in self.std_sample.keys():
            temp_log = {
                'language': lang_code,
                'verification': True,
                'message': []
            }

            std_lang_dict = self.std_sample[lang_code]
            val_lang_dict = self.verify_data[lang_code]

            for key in std_lang_dict.keys():
                print()
                temp_log['url'] = val_lang_dict[key]['url']

                for content_idx, content_str in std_lang_dict[key].items():
                    # Content different
                    if isinstance(std_lang_dict[key][content_idx], str):
                        if std_lang_dict[key][content_idx] != val_lang_dict[key][content_idx]:
                            message = '[Content different]:\nStandard sample: ' + str(std_lang_dict[key][content_idx]) \
                                      + '\n\nValidation Data(' + val_lang_dict[key]['url'] + '): ' + str(val_lang_dict[key][content_idx])
                            # print('language:', lang_code)
                            # print('url:', self.verify_data[lang_code][key]['url'])
                            # print('\tContent Error')
                            # print('\t->', message)
                            temp_log['verification'] = False
                            report_dict['verification'] = False
                            temp_log['message'].append(message)


                    elif isinstance(std_lang_dict[key][content_idx], dict):
                        std_table = std_lang_dict[key][content_idx]
                        val_table = val_lang_dict[key][content_idx]

                        if len(std_table.keys()) != len(val_table.keys()):
                            message = '[The number of Table rows different]: \nSample table row num: ' + \
                                      str(len(std_table.keys())) + '\n\nValidation Data(' + val_lang_dict[key]['url'] + ') table row num: ' +\
                                        str(len(val_table.keys()))
                            # print('language:', lang_code)
                            # print('url:', self.verify_data[lang_code][key]['url'])
                            # print('\tTable row num Error')
                            # print('\t->', message)
                            temp_log['verification'] = False
                            report_dict['verification'] = False
                            temp_log['message'].append(message)
                        else:
                            for row, no in enumerate(std_table.keys()):
                                if list(std_table[no].keys()) != list(val_table[no].keys()):
                                    message = '[Table column different]:\nStandard sample table column: ' + str(
                                        list(std_table[no].keys())) \
                                              + '\n\nValidation Data(' + val_lang_dict[key]['url'] + ') table column: ' + str(
                                        list(val_table[no].keys()))
                                    # print('language:', lang_code)
                                    # print('url:', self.verify_data[lang_code][key]['url'])
                                    # print('\tTable column Error')
                                    # print('\t->', message)
                                    temp_log['verification'] = False
                                    report_dict['verification'] = False
                                    temp_log['message'].append(message)
                                else:
                                    if list(std_table[no].values()) != list(val_table[no].values()):
                                        for col in std_table[no].keys():
                                            if std_table[no][col] != val_table[no][col]:
                                                message = '[Table row Content different]: In ' + str(row) + 'Row, column:' + str(col)+\
                                                          '\nStandard sample table content:\n' + str(std_table[no][col]) \
                                                          + '\n\nValidation Data(' + val_lang_dict[key][
                                                              'url'] + ') table content:\n' + str(
                                                    val_table[no][col])
                                                # print('\nlanguage:', lang_code)
                                                # print('url:', self.verify_data[lang_code][key]['url'])
                                                # print('\tTable row content Error')
                                                # print('\trow:', row)
                                                # print('\t->', message)
                                                temp_log['verification'] = False
                                                report_dict['verification'] = False
                                                temp_log['message'].append(message)

            report_dict['logging'].append(temp_log)

        return report_dict














def compare_data():

    ta = TeamsAlerter()

    about_us_files = ['about_team', 'about_family', 'about_certification', 'about_stronghold']
    about_us_results = []
    for f in about_us_files:
        time.sleep(1)
        s_data = './scrape_data/previous_website_' + f + '.json'
        v_data = './scrape_data/www.hannstar.com_'+ f + '.json'
        dv = Data_Verification(std_sample=s_data, verify_data=v_data)
        final_report = dv.verification_with_json()
        if not final_report['verification']:
            print('#', f)
            for log in final_report['logging']:
                print('language:', log['language'])
                print('url:', log['url'])
                if not log['table_logging']['verify']:
                    print('\tTable Error')
                    print('\t-> Error_Message:', log['table_logging']['error_message'])
                    for error_info in log['table_logging']['error_message']:
                        error_info = error_info
                        ta.send_alert_to_teams(message=error_info, val_url=log['url'])
                if not log['content_logging']['verify']:
                    print('\tContent Error')
                    print('\t-> Error_Message:', log['content_logging']['error_message'])
                    for error_info in log['content_logging']['error_message']:
                        error_info = error_info
                        ta.send_alert_to_teams(message=error_info, val_url=log['url'])

                print()
            print('\n--------------------------------')

        about_us_results.append(final_report)

    ESG_files = ['董事會名單', '審計委員會', '內部稽核', '薪酬委員會', '誠信經營']#
    ESG_results = []
    for f in ESG_files:
        time.sleep(1)
        s_data = './scrape_data/previous_website_' + f + '.json'
        v_data = './scrape_data/www.hannstar.com_' + f + '.json'
        dv = Reptile_Data_Verification(std_sample=s_data, verify_data=v_data)
        final_report = dv.verification_with_json()
        if not final_report['verification']:
            print('#', f)
            for log in final_report['logging']:
                if not log['verification']:
                    print('language:', log['language'])
                    print('url:', log['url'])

                    for error_info in log['message']:
                        print(error_info)
                        ta.send_alert_to_teams(message=error_info, val_url=log['url'])
                print()
            print('\n--------------------------------')

        ESG_results.append(final_report)





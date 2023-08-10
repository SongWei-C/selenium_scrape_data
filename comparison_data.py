import json
import logging

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
        def check_diff_row(sample, verify_data):
            error_dict = {
                'error_category': [],
                'error_index': []
            }
            if len(sample) != len(verify_data):
                error_dict['error_category'].append('ITEM_NUM_NOT_MATCH')
                len_min = min(len(sample), len(verify_data))
                for i in range(len_min):
                    if sample[i] != verify_data[i]:
                        error_dict['error_category'].append('CONTENT_NOT_SAME')
                        error_dict['error_index'].append(i)
                        # print(sample[i])
                        # print(verify_data[i])
            else:
                for i in range(len(verify_data)):
                    if sample[i] != verify_data[i]:
                        error_dict['error_category'].append('CONTENT_NOT_SAME')
                        error_dict['error_index'].append(i)
                        # print(sample[i])
                        # print(verify_data[i])
            return error_dict

        report_dict = {
            'verification': False,
            'logging':[],
            'message':[]
        }

        for lang_code in self.std_sample.keys():
            temp_log = {
                'language': lang_code,
                'verification': False,
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
                print('table!')
                print(std_lang_obj['table'])
                print(verify_lang_obj['table'])
                temp_log['table_logging']['verify'] = False
                temp_log['table_logging']['error_message'] = []

                if std_lang_obj['table'] == None and verify_lang_obj['table'] != None:
                    message = '[The number of <table> is different]: Standard Sample('+std_lang_obj['url']+') not find any table.'
                    temp_log['table_logging']['error_message'].append(message)
                elif std_lang_obj['table'] != None and verify_lang_obj['table'] == None:
                    message = '[The number of <table> is different]: Validation Data(' + verify_lang_obj['url'] + ') not find any table.'
                    temp_log['table_logging']['error_message'].append(message)
                else: # 檢查彼此表格 1.表格數量 2.table head 3. table body
                    if len(std_lang_obj['table']) != len(verify_lang_obj['table']):
                        message = '[The number of <table> is different]:'+str(len(std_lang_obj['table'])) + \
                                  'tables found in Standard sample('+std_lang_obj['url'] + '),but '+ \
                            str(len(verify_lang_obj['table'])) + 'tables found in Validation Data(' + verify_lang_obj['url'] + ')'
                        temp_log['table_logging']['error_message'].append(message)

                    else:
                        for i in range(len(std_lang_obj['table'])):
                            std_table = std_lang_obj['table'][i]
                            val_table = verify_lang_obj['table'][i]
                            # 檢查table head row數量
                            if std_table['thead'] == None and val_table['thead'] != None:
                                message = '[The number of <table head rows> is different]: In'+ str(i)+'Table in Standard Sample(' + std_lang_obj[
                                    'url'] + ') not find any table head row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['thead'] != None and val_table == None:
                                message = '[The number of <table head rows> is different]: In'+ str(i)+'Table in Validation Data(' + verify_lang_obj[
                                    'url'] + ') not find any table head row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['thead'] != None and val_table['thead'] != None:  # 檢查彼此表格 1.表格數量 2.table head 3. table body
                                if len(std_table['thead']) != len(val_table['thead']):
                                    message = '[The number of <table head rows> is different]: In'+ str(i)+'Table ' + str(len(std_table['thead'])) + \
                                              'table head rows found in '+ str(i) +'Table in Standard sample(' + std_lang_obj['url'] + '),but ' + \
                                              str(len(val_table['thead'])) + 'table head rows found in '+ str(i) +'Table in Validation Data(' + \
                                              verify_lang_obj['url'] + ')'
                                    temp_log['table_logging']['error_message'].append(message)
                                else: # 檢查每個row元素
                                    for j in range(len(std_table['thead'])):
                                        std_row_th = std_table['thead'][j]['th']
                                        val_row_th = val_table['thead'][j]['th']

                                        if std_row_th == None and val_row_th != None:
                                            message = '[The number of thead <th> is different]: In'+ str(i)+'Table '+ str(j) +'Thead Row in Standard Sample(' + \
                                                      std_lang_obj['url'] + ') not find any table head <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th == None:
                                            message = '[The number of thead <th> is different]: In'+ str(i)+'Table '+ str(j) +'Thead Row in Validation Data(' + \
                                                      verify_lang_obj['url'] + ') not find any table head <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th != None:
                                            if len(std_row_th) != len(val_row_th):
                                                message = '[The number of thead <th> is different]: In'+ str(i)+'Table ' + str(j) + 'Thead Row\n ->' +\
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
                                                        message = 'Content different: In '+ str(i)+'Table ' \
                                                                  + str(j) + 'Thead Row ' + str(k)+'<th> ->\n' \
                                                                  + 'Standard sample(' + std_lang_obj['url'] + '): "'\
                                                                  + std_th_ele +'"\n'\
                                                                  + 'Validation Data(' + verify_lang_obj['url'] + '): "'\
                                                                  + val_th_ele + '"'
                                                        temp_log['table_logging']['error_message'].append(message)


                            #----------------------------------------------------------------------------------------------
                            # 檢查table body row數量
                            if std_table['tbody'] == None and val_table['tbody'] != None:
                                message = 'The number of <table body rows> is different: Standard Sample(' + \
                                          std_lang_obj['url'] + ') not find any table body row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['tbody'] != None and val_table['tbody'] == None:
                                message = 'The number of <table body rows> is different: Validation Data(' + \
                                          verify_lang_obj[
                                              'url'] + ') not find any table body row.'
                                temp_log['table_logging']['error_message'].append(message)
                            elif std_table['tbody'] != None and val_table['tbody'] != None:
                                if len(std_table['tbody']) != len(val_table['tbody']):
                                    message = 'The number of <table body rows> is different:' + str(
                                        len(std_table['tbody'])) + 'table body rows found in '+ str(i) +\
                                              'Table in Standard sample(' + std_lang_obj['url'] +\
                                              '),but ' + str(len(val_table['tbody'])) + 'table body rows found in '+\
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
                                            message = '[The number of tbody <th> is different]: In' + str(
                                                i) + 'Table '+ str(j) +'Tbody Row in Standard Sample(' + \
                                                      std_lang_obj['url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th == None:
                                            message = '[The number of tbody <th> is different]: In' + str(
                                                i) + 'Table '+ str(j) +'Tbody Row in Validation Data(' + \
                                                      verify_lang_obj['url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_th != None and val_row_th != None:
                                            if len(std_row_th) != len(val_row_th):
                                                message = '[The number of tbody <th> is different]: In' + str(
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
                                                        message = 'Content different: In ' + str(i) + 'Table ' \
                                                                  + str(j) + 'Tbody Row ' + str(k) + '<th> ->\n' \
                                                                  + 'Standard sample(' + std_lang_obj['url'] + '): "' \
                                                                  + std_th_ele + '"\n' \
                                                                  + 'Validation Data(' + verify_lang_obj['url'] + '): "' \
                                                                  + val_th_ele + '"'
                                                        temp_log['table_logging']['error_message'].append(message)

                                        # 檢查td list
                                        if std_row_td == None and val_row_td != None:
                                            message = '[The number of tbody <td> is different]: In' + str(
                                                i) + 'Table ' + str(
                                                j) + 'Tbody Row in Standard Sample(' + \
                                                      std_lang_obj[
                                                          'url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_td != None and val_row_td == None:
                                            message = '[The number of tbody <td> is different]: In' + str(
                                                i) + 'Table ' + str(
                                                j) + 'Tbody Row in Validation Data(' + \
                                                      verify_lang_obj[
                                                          'url'] + ') not find any table body <th>.'
                                            temp_log['table_logging']['error_message'].append(message)
                                        elif std_row_td != None and val_row_td != None:
                                            if len(std_row_td) != len(val_row_td):
                                                message = '[The number of tbody <td> is different]: In' + str(
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
                                                        message = 'Content different: In ' + str(
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

                message = 'Content different:'
                print('content!')
                print(std_lang_obj['content'])
                print(verify_lang_obj['content'])

            else:
                # print('Content 相同')
                temp_log['content_logging']['verify'] = True

            if temp_log['content_logging']['verify'] and temp_log['table_logging']['verify']:
                temp_log['verification'] = True

            # 加入紀錄中
            report_dict['logging'].append(temp_log)

        return report_dict



if __name__ == '__main__':
    # std_data = './scrape_data/previous_website_about_certification.json'
    # verify_data = './scrape_data/magento_about_certification.json'
    # dv = Data_Verification(std_sample=std_data, verify_data=verify_data)
    # final_report = dv.verification_with_json()

    files = ['about_us_team', 'about_family', 'about_certification', 'financial_profile', 'about_stronghold']
    results = []
    for f in files:
        s_data = './scrape_data/previous_website_' + f + '.json'
        v_data = './scrape_data/magento_'+ f + '.json'
        dv = Data_Verification(std_sample=s_data, verify_data=v_data)
        final_report = dv.verification_with_json()
        results.append(final_report)

        if final_report['verification'] == False:
            print('#', f)


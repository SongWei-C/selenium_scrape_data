import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import random
from multiprocessing.pool import ThreadPool as Pool
import json

class CustomerScraper:
    """Scrape the website url by customer name"""
    # service = Service('../driver/chromedriver.exe')
    ua = UserAgent()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    def __init__(self, domain_url:str='https://www.hannstar.com', language_code:list[str] = ['en', 'tw', 'cn']) -> None:
        """Active Chrome Drivers(.exe)"""
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument(f'user-agent={self.ua.random}')
        # self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument("--disable-popup-blocking")
        # self.options.add_argument('--lang=en')
        print('init chrome driver...')
        self.driver = uc.Chrome(
            # service=self.service,
            options=self.options
        )
        print('Complete !\n')
        if domain_url[-1] != '/':
            domain_url += '/'
        self.domain_url = domain_url
        self.language_codes = language_code

    def scrape_financial_profile(self, web_path:str='/investors/summary', output_json:bool = True) -> None:
        # 會直接將爬蟲存成類別變數(Dict)
        financial_profile_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        if self.domain_url == 'https://www.hannstar.com/':
            financial_profile_dict['tw']['url'] = str(financial_profile_dict['tw']['url']).replace('/tw', '')

        print('\n- page financial_profile -')
        # 爬取表格資料
        self.scrape_table(financial_profile_dict)

        # 無內文Content資料直接設成None
        for key, ele in financial_profile_dict.items():
            ele['content'] = None

        self.financial_profile_dict = financial_profile_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/previous_website_financial_profile.json" \
                if self.domain_url == 'https://www.hannstar.com/' else './scrape_data/magento_financial_profile.json'
            with open(file_path, "w") as final:
                json.dump(financial_profile_dict, final, indent=4)

    def scrape_click_pages(self, input_dict):
        def get_table(input_element):
            self.driver.implicitly_wait(0.5)
            try:
                tables = self.driver.find_elements(
                    By.XPATH, '//table'
                )
                input_element['table'] = []

                for j,table in enumerate(tables):
                    table_dict = {}

                    # table head
                    print('Table head:')
                    try:
                        head_rows = table.find_elements(
                            By.XPATH, '//table['+ str(j+1) +']/thead/tr'
                        )
                        table_dict['thead'] = []
                        for thead in head_rows:
                            tr = {'th':[]}
                            ths = thead.find_elements(
                                By.XPATH, '//table['+ str(j+1) +']/thead/tr/th'
                            )
                            if ths == []:
                                continue
                            else:
                                for th in ths:
                                    tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                    print(th.text)
                                table_dict['thead'].append(tr)
                                print('------------------')
                    except NoSuchElementException as e:
                        print('Not find table head')
                        table_dict['thead'] = None

                    if table_dict['thead'] == []:
                        table_dict['thead'] = None
                    # table body
                    print('Table body:')
                    try:
                        tbody_rows = table.find_elements(
                            By.XPATH, '//table['+ str(j+1) +']/tbody/tr'
                        )
                        table_dict['tbody'] = []
                        for i,trow in enumerate(tbody_rows):
                            tr = {'th': [], 'td': []}
                            # th
                            try:
                                ths = trow.find_elements(
                                    By.XPATH, '//table['+ str(j+1) +']/tbody/tr['+ str(i+1) +']/th'
                                )
                                if ths == []:
                                    tr['th'] = None
                                else:
                                    for th in ths:
                                        tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                        print(th.text)
                            except NoSuchElementException:
                                print('Not find th')
                                tr['th'] = None
                            # td
                            tds = trow.find_elements(
                                By.XPATH, '//table['+ str(j+1) +']/tbody/tr['+ str(i+1) +']/td'
                            )
                            if tds == []:
                                tr['td'] = None

                            else:
                                for td in tds:
                                    tr['td'].append(str(td.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                    print(td.text)

                            if tr['th'] == None and tr['td'] == None:
                                continue
                            table_dict['tbody'].append(tr)

                            print('------------------')
                    except NoSuchElementException:
                        print('Not find Table body!')
                        table_dict['tbody'] = None
                    if table_dict['tbody'] == []:
                        table_dict['tbody'] = None
                    if table_dict['tbody'] == None and table_dict['thead'] == None:
                        continue
                    input_element['table'].append(table_dict)

                if input_element['table'] == []:
                    input_element['table'] = None
            except NoSuchElementException as e:
                print('Not find Table !')
                input_element['table'] = None

        for lang, element in input_dict.items():
            base_url = element['url']
            self.driver.implicitly_wait(1)
            self.driver.get(base_url)
            time.sleep(0.5)
            if lang != 'tw':
                self.driver.get(base_url)
                time.sleep(0.5)

            click_list = element['click_list']
            element['pages'] = []

            for i,click_btn in enumerate(click_list):
                child_page = {
                    'page_name': click_btn
                }
                click_element = self.driver.find_element(
                    By.XPATH, '//a[text()="'+ click_btn+'"]'
                )
                print("Find click btn to click:", click_element.text)

                ActionChains(driver=self.driver).click(click_element).pause(5).perform()
                self.driver.implicitly_wait(2)
                time.sleep(0.5)

                # try:
                #     _ = WebDriverWait(self.driver, 10).until(
                #         EC.presence_of_element_located((By.XPATH, "//table"))
                #     )
                #     get_table(child_page)
                #     element['pages'].append(child_page)
                # finally:
                #     self.driver.quit()

    def scrape_investors_summary(self, click_list:list[list[str]], web_path:str='/investors/summary', output_json:bool = True) -> None:
        # 會直接將爬蟲存成類別變數(Dict)
        investors_summary_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        if self.domain_url == 'https://www.hannstar.com/':
            investors_summary_dict['tw']['url'] = str(investors_summary_dict['tw']['url']).replace('/tw', '')

        # 加上子頁
        investors_summary_dict['tw']['click_list'] = ['財務基本資料', '營運報告行事曆', '主要股東名單']
        investors_summary_dict['en']['click_list'] = ['Financial Information', 'Financial Calendar', 'List of major shareholders']
        investors_summary_dict['cn']['click_list'] = ['財務基本資料', '营运报告行事历', '主要股东名单']
        self.scrape_click_pages(investors_summary_dict)
        self.investors_summary_dict = investors_summary_dict

    def scrape_table(self, input_dict:dict):
        print('\nScraping Table ...')
        for key, element in input_dict.items():
            # if str(key) != 'tw':
            #     continue
            url = element['url']
            print('\n# ', key.upper())
            print('Start scrape Url:', url)
            try:
                self.driver.implicitly_wait(1)
                self.driver.get(url)
                time.sleep(0.5)
                if key != 'tw':
                    self.driver.get(url)
                    time.sleep(0.5)
                tables = self.driver.find_elements(
                    By.XPATH, '//table'
                )
                element['table'] = []

                for j,table in enumerate(tables):
                    table_dict = {}

                    # table head
                    print('Table head:')
                    try:
                        head_rows = table.find_elements(
                            By.XPATH, '//table['+ str(j+1) +']/thead/tr'
                        )
                        table_dict['thead'] = []
                        for thead in head_rows:
                            tr = {'th':[]}
                            ths = thead.find_elements(
                                By.XPATH, '//table['+ str(j+1) +']/thead/tr/th'
                            )
                            if ths == []:
                                continue
                            else:
                                for th in ths:
                                    tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                    print(th.text)
                                table_dict['thead'].append(tr)
                                print('------------------')
                    except NoSuchElementException as e:
                        print('Not find table head')
                        table_dict['thead'] = None

                    if table_dict['thead'] == []:
                        table_dict['thead'] = None
                    # table body
                    print('Table body:')
                    try:
                        tbody_rows = table.find_elements(
                            By.XPATH, '//table['+ str(j+1) +']/tbody/tr'
                        )
                        table_dict['tbody'] = []
                        for i,trow in enumerate(tbody_rows):
                            tr = {'th': [], 'td': []}
                            # th
                            try:
                                ths = trow.find_elements(
                                    By.XPATH, '//table['+ str(j+1) +']/tbody/tr['+ str(i+1) +']/th'
                                )
                                if ths == []:
                                    tr['th'] = None
                                else:
                                    for th in ths:
                                        tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                        print(th.text)
                            except NoSuchElementException:
                                print('Not find th')
                                tr['th'] = None
                            # td
                            tds = trow.find_elements(
                                By.XPATH, '//table['+ str(j+1) +']/tbody/tr['+ str(i+1) +']/td'
                            )
                            if tds == []:
                                tr['td'] = None

                            else:
                                for td in tds:
                                    tr['td'].append(str(td.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                                    print(td.text)

                            if tr['th'] == None and tr['td'] == None:
                                continue
                            table_dict['tbody'].append(tr)

                            print('------------------')
                    except NoSuchElementException:
                        print('Not find Table body!')
                        table_dict['tbody'] = None
                    if table_dict['tbody'] == []:
                        table_dict['tbody'] = None
                    if table_dict['tbody'] == None and table_dict['thead'] == None:
                        continue
                    element['table'].append(table_dict)

                if element['table'] == []:
                    element['table'] = None
            except NoSuchElementException as e:
                print('Not find Table !')
                element['table'] = None

    def scrape_content(self,input_dict:dict, xpath:str, group:bool):
        print('\nScraping Content ...')
        for key, element in input_dict.items():
            # if str(key) != 'tw':
            #     continue
            url = element['url']
            print('\n# ', key.upper())
            print('Start scrape Url:', url)
            try:
                self.driver.get(url)
                time.sleep(0.5)
                if key != 'tw':
                    self.driver.implicitly_wait(1)
                    self.driver.get(url)
                    time.sleep(0.5)

                if group:
                    element['content'] = []
                    contents = self.driver.find_elements(
                        By.XPATH, xpath
                    )
                    for i,content in enumerate(contents):
                        idx_content = content.find_element(
                            By.XPATH, xpath+'['+str(i+1)+']'
                        )
                        print(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                        if str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '')!= '':
                            element['content'].append(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                    if element['content'] == []:
                        element['content'] = None
                else:
                    text = ''
                    contents = self.driver.find_elements(
                        By.XPATH, xpath
                    )
                    for i, content in enumerate(contents):
                        idx_content = content.find_element(
                            By.XPATH, xpath + '[' + str(i + 1) + ']'
                        )
                        print(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', ''))
                        if str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '') != '':
                            text += str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '')
                    if text != '':
                        element['content']= text
                    else:
                        element['content'] = None

            except NoSuchElementException:
                print('Not find Content !')
                element['content'] = None

    def scrape_about_team(self, web_path:str='/about/team/', output_json:bool = True) -> None:
        # 會直接將爬蟲存成類別變數(Dict)
        about_team_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        if self.domain_url == 'https://www.hannstar.com/':
            about_team_dict['tw']['url'] = str(about_team_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/team -')
        # 爬取表格資料
        self.scrape_table(about_team_dict)

        # 無內文Content資料直接設成None
        for key, ele in about_team_dict.items():
            ele['content'] = None

        self.about_team_dict = about_team_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/previous_website_about_us_team.json" \
                if self.domain_url == 'https://www.hannstar.com/' else './scrape_data/magento_about_us_team.json'
            with open(file_path, "w") as final:
                json.dump(about_team_dict, final, indent=4)

    def scrape_about_family(self, list_content:bool, web_path:str='/about/family', xpath:str='', output_json:bool = True) -> None:
        # 會直接將爬蟲存成類別變數(Dict)
        about_family_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        if self.domain_url == 'https://www.hannstar.com/':
            about_family_dict['tw']['url'] = str(about_family_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/family -')
        # 爬取表格資料
        self.scrape_table(about_family_dict)

        # 爬取Content資料
        self.scrape_content(input_dict=about_family_dict, xpath=xpath, group=list_content)


        self.about_family_dict = about_family_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/previous_website_about_family.json" \
                if self.domain_url == 'https://www.hannstar.com/' else './scrape_data/magento_about_family.json'
            with open(file_path, "w") as final:
                json.dump(about_family_dict, final, indent=4)

    def scrape_about_certification(self,content_xpath:str, web_path:str='/about/certification', output_json:bool=True):
        # 會直接將爬蟲存成類別變數(Dict)
        about_certification_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        if self.domain_url == 'https://www.hannstar.com/':
            about_certification_dict['tw']['url'] = str(about_certification_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/certification -')
        # 爬取表格資料
        self.scrape_table(about_certification_dict)

        # 爬取Content資料
        self.scrape_content(input_dict=about_certification_dict, xpath=content_xpath, group=False)

        self.about_certification_dict = about_certification_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/previous_website_about_certification.json" \
                if self.domain_url == 'https://www.hannstar.com/' else './scrape_data/magento_about_certification.json'
            with open(file_path, "w") as final:
                json.dump(about_certification_dict, final, indent=4)

    def scrape_about_stronghold(self,content_xpath:str, web_path:str='/about/stronghold', output_json:bool=True):
        # 會直接將爬蟲存成類別變數(Dict)
        about_stronghold_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        #if self.domain_url == 'https://www.hannstar.com/':
#            about_stronghold_dict['tw']['url'] = str(about_stronghold_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/stronghold -')
        # 爬取表格資料
        self.scrape_table(about_stronghold_dict)

        # 爬取Content資料
        self.scrape_content(input_dict=about_stronghold_dict, xpath=content_xpath, group=False)

        self.about_stronghold_dict = about_stronghold_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/previous_website_about_stronghold.json" \
                if self.domain_url == 'https://www.hannstar.com/' else './scrape_data/magento_about_stronghold.json'
            with open(file_path, "w") as final:
                json.dump(about_stronghold_dict, final, indent=4)

    def __del__(self) -> None:
        """Close the driver"""
        self.driver.quit()

if __name__ == '__main__':
    '''https://www.hannstar.com(舊)'''
    # cs = CustomerScraper()
    # 關於翰宇彩晶
    # cs.scrape_about_team() # 關於團隊
    # cs.scrape_about_family(list_content=True,xpath='//div[@class="mainArea noPB"]/ul/li',output_json=True) # 關於關係企業
    # cs.scrape_about_certification(web_path='/about/certification/', content_xpath='//div[@class="itemAllType itemOnlyText itemWrap"]/div', output_json=True)
    # cs.scrape_about_stronghold(content_xpath='//div[@class="strongholdBox"]', output_json=True) # 全球據點
    #投資人關係
    # cs.scrape_financial_profile(web_path='/investors/article/financial-summary/') # 公司概況-財務基本資料
    # clicks = [['Financial Information', 'Financial Calendar', 'List of major shareholders'],
    #           ['財務基本資料', '營運報告行事曆', '主要股東名單'], ['財務基本資料', '营运报告行事历', '主要股东名单']]
    # cs.scrape_investors_summary(web_path='/investors/article/financial-summary/', click_list=clicks)

    '''magento'''
    new_cs = CustomerScraper(domain_url='https://magentoprd.hannstar.com')
    # 關於翰宇彩晶
    new_cs.scrape_about_team() # 關於團隊
    new_cs.scrape_about_family(list_content=True,xpath='//div[@class="Graphics3Content"]/div',output_json=True) # 關於關係企業
    new_cs.scrape_about_certification(content_xpath='//div[@class="D360TemplatesModuleBlock"]', output_json=True) # 關於認證
    new_cs.scrape_about_stronghold(content_xpath='//div[@class="AboutStrongholdBlock"]', output_json=True) # 關於全球據點
    # 投資人關係
    # new_cs.scrape_financial_profile() # 公司概況-財務基本資料

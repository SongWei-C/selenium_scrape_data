import pandas as pd
import time
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from multiprocessing.pool import ThreadPool as Pool
import json
import jsbeautifier
class CustomerScraper:
    """Scrape the website url by customer name"""
    ua = UserAgent()
    chromedriver_path = ChromeDriverManager(version="114.0.5735.16").install()
    service = Service(executable_path=chromedriver_path)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    def __init__(self, domain_url:str='https://www.hannstar.com', language_code:list[str] = ['en', 'tw', 'cn']) -> None:
        """Active Chrome Drivers(.exe)"""
        self.options = Options()
        # self.options = uc.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument(f'user-agent={self.ua.random}')
        # self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument("--disable-popup-blocking")
        # self.options.add_argument('--lang=en')
        print('init chrome driver...')
        self.driver = webdriver.Chrome(
            service=self.service,
            options=self.options)
        # self.driver = uc.Chrome(options=self.options)
        self.driver.maximize_window()
        print('Complete !\n')
        if domain_url[-1] != '/':
            domain_url += '/'
        self.domain_url = domain_url
        self.language_codes = language_code

    def save2json(self,
            SAVE_PATH: str,
            Dict_json_output_final: dict):

        options = jsbeautifier.default_options()
        options.indent_size = 4

        with open(SAVE_PATH, 'w', encoding='utf-8') as json_file:
            json_file.write(jsbeautifier.beautify(json.dumps(Dict_json_output_final, ensure_ascii=False), options))

    def soup_get_text(self,
            table_element,
            no,
            Dict_json):

        table_html = table_element.get_attribute('outerHTML')
        soup = BeautifulSoup(table_html, 'html.parser')
        text_content = soup.get_text()

        Dict_json['Content{}'.format(no)] = text_content.replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')

    def table2json3(self,
            df, Dict_json):

        json_data = {}
        Lst_column_names = list(df.columns)
        for index, row in df.iterrows():
            json_data_tmp = {}
            json_data_tmp['{}'.format(Lst_column_names[0])] = row['{}'.format(Lst_column_names[0])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data_tmp['{}'.format(Lst_column_names[1])] = row['{}'.format(Lst_column_names[1])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data_tmp['{}'.format(Lst_column_names[2])] = row['{}'.format(Lst_column_names[2])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data['No.{}'.format(index + 1)] = json_data_tmp

        return json_data

    # ESG-公司治理
    def board_directors_supervisors(self,
            Dict_json_output,
            LANGUAGE):

        url = "https://www.hannstar.com/{}/sustainability/governance".format(LANGUAGE)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        if LANGUAGE != 'tw':
            self.driver.get(url)
            time.sleep(0.5)
        Dict_json = {}

        # ----------------------------- 內容1 ----------------------------------------------------
        time.sleep(5)
        if (LANGUAGE == 'tw' or LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]/p")
        elif (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]")

        no = 1
        Dict_json['url'] = url
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 表格1 ----------------------------------------------------

        # 定位表格元素
        time.sleep(5)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[2]/table")
        table_html = table_element.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]

        json_data = self.table2json3(df, Dict_json)
        Dict_json['Table1'] = json_data

        Dict_json_output['董事會名單'] = Dict_json

        print("{} process SUCCESS".format(url))

        return Dict_json_output

    def audit_committee(self, # 審計委員會
            Dict_json_output,
            LANGUAGE):

        url = "https://www.hannstar.com/{}/sustainability/governance?esgTab=Audit".format(LANGUAGE)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        if LANGUAGE != 'tw':
            self.driver.get(url)
            time.sleep(0.5)

        Dict_json = {}

        # ----------------------------- 內容1 ----------------------------------------------------
        time.sleep(5)
        if (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[1]/p/span[2]")
        elif (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[1]/p/span[4]")
        Dict_json['url'] = url
        no = 1
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 表格1 ----------------------------------------------------

        # 定位表格元素
        time.sleep(5)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[2]/table")
        table_html = table_element.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]

        json_data = self.table2json3(df, Dict_json)
        Dict_json['Table1'] = json_data

        # ----------------------------- 內容2 ----------------------------------------------------
        time.sleep(5)
        if (LANGUAGE == 'tw' or LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p")

        no = 2
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 表格2 ----------------------------------------------------

        # 定位表格元素
        time.sleep(5)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[2]/table")
        table_html = table_element.get_attribute('outerHTML')
        df = pd.read_html(table_html, header=0)[0]

        json_data = {}
        Lst_column_names = list(df.columns)
        for index, row in df.iterrows():
            json_data_tmp = {}
            json_data_tmp['{}'.format(Lst_column_names[0])] = row['{}'.format(Lst_column_names[0])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data_tmp['{}'.format(Lst_column_names[1])] = row['{}'.format(Lst_column_names[1])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data_tmp['{}'.format(Lst_column_names[2])] = row['{}'.format(Lst_column_names[2])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')
            json_data_tmp['{}'.format(Lst_column_names[3])] = row['{}'.format(Lst_column_names[3])].replace('\t',
                                                                                                            '').replace(
                '\r', '').replace('\n', '').replace('\\', '')

            json_data['No.{}'.format(index + 1)] = json_data_tmp

        Dict_json['Table2'] = json_data

        Dict_json_output['審計委員會'] = Dict_json

        print("{} process SUCCESS".format(url))

        return Dict_json_output

    def remuneration_committee(self, # 薪酬委員會
            Dict_json_output,
            LANGUAGE):

        url = "https://www.hannstar.com/{}/sustainability/governance?esgTab=Salary".format(LANGUAGE)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        if LANGUAGE != 'tw':
            self.driver.get(url)
            time.sleep(0.5)

        Dict_json = {}
        Dict_json['url'] = url
        # ----------------------------- 內容1 ----------------------------------------------------
        time.sleep(5)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[1]/span[2]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[1]/span[1]")

        no = 1
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容2 ----------------------------------------------------
        time.sleep(5)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[2]")

        no = 2
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 表格1 ----------------------------------------------------

        # 定位表格元素
        time.sleep(5)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[2]/table")

        table_html = table_element.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]

        json_data = self.table2json3(df, Dict_json)
        Dict_json['Table1'] = json_data

        Dict_json_output['薪酬委員會'] = Dict_json

        print("{} process SUCCESS".format(url))

        return Dict_json_output

    def auditor(self, # 內部稽核
            Dict_json_output,
            LANGUAGE):

        url = "https://www.hannstar.com/{}/sustainability/governance?esgTab=Check".format(LANGUAGE)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        if LANGUAGE != 'tw':
            self.driver.get(url)
            time.sleep(0.5)

        Dict_json = {}
        Dict_json['url'] = url
        # ----------------------------- 內容1 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[1]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[1]")

        no = 1
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容2 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span[1]")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[3]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span/span[1]")

        no = 2
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容3 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span[2]")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[4]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span/span[2]")

        no = 3
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容4 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[5]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[3]")

        no = 4
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容5 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[6]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[4]")

        no = 5
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容6 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[7]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[5]")

        no = 6
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容7 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[8]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[6]")

        no = 7
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容8 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[1]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[1]/span[1]")

        no = 8
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容9 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[9]")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[2]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[2]")

        no = 9
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容10 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[4]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[4]/span[1]")

        no = 10
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 表格1 ----------------------------------------------------

        # 定位表格元素
        time.sleep(2)
        table_element = self.driver.find_element('xpath',
                                            "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[2]")

        table_html = table_element.get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]

        json_data = self.table2json3(df, Dict_json)
        Dict_json['Table1'] = json_data

        # ----------------------------- 內容11 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[1]")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[1]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]")

        no = 11
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容12 ----------------------------------------------------
        time.sleep(2)

        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]")
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]")
        else:
            table_element = self.driver.find_element('xpath',
                                                "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[3]")

        no = 12
        self.soup_get_text(table_element, no, Dict_json)

        Dict_json_output['內部稽核'] = Dict_json

        print("{} process SUCCESS".format(url))

        return Dict_json_output

    def ethical_rule(self, # 誠信經營
            Dict_json_output,
            LANGUAGE):

        url = "https://www.hannstar.com/{}/sustainability/governance?esgTab=Operate".format(LANGUAGE)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        time.sleep(0.5)
        if LANGUAGE != 'tw':
            self.driver.get(url)
            time.sleep(0.5)

        Dict_json = {}
        Dict_json['url'] = url
        # ----------------------------- 內容1 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[1]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[1]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]')

        no = 1
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容2 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[1]')
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[1]')

        no = 2
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容3 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'cn'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[2]')
        elif (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '/html/body/div[3]/main/div[3]/div/div/div[2]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[2]')

        no = 3
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容4 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[3]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[3]')

        no = 4
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容5 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]')

        no = 5
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容6 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[7]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]')

        no = 6
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容7 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[8]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]')

        no = 7
        self.soup_get_text(table_element, no, Dict_json)

        # ----------------------------- 內容8 ----------------------------------------------------
        time.sleep(2)
        if (LANGUAGE == 'en'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[9]')
        elif (LANGUAGE == 'tw'):
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]/span/span')
        else:
            table_element = self.driver.find_element('xpath',
                                                '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[7]/span/span')

        no = 8
        self.soup_get_text(table_element, no, Dict_json)

        Dict_json_output['誠信經營'] = Dict_json

        print("{} process SUCCESS".format(url))

        return Dict_json_output

    def scrape_financial_profile(self, web_path:str='/investors/summary', output_json:bool = True) -> None:
        # 會直接將爬蟲存成類別變數(Dict)
        financial_profile_dict = {
            lang: {
                'language': lang,
                'url': self.domain_url + lang + web_path
            } for lang in self.language_codes
        }
        # 新官網上線後要拿掉
        # if self.domain_url == 'https://www.hannstar.com/':
        #     financial_profile_dict['tw']['url'] = str(financial_profile_dict['tw']['url']).replace('/tw', '')

        print('\n- page financial_profile -')
        # 爬取表格資料
        self.scrape_table(financial_profile_dict)

        # 無內文Content資料直接設成None
        for key, ele in financial_profile_dict.items():
            ele['content'] = None

        self.financial_profile_dict = financial_profile_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/" + self.domain_url.replace('/', '').replace('https:', '') + "_financial_profile.json"
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
                                    tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', '').replace('&nbsp;', ''))
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
                                        tr['th'].append(str(th.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
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
                                    tr['td'].append(str(td.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
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
        # if self.domain_url == 'https://www.hannstar.com/':
        #     investors_summary_dict['tw']['url'] = str(investors_summary_dict['tw']['url']).replace('/tw', '')

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

                # ele = WebDriverWait(self.driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '//table'))
                # )

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
                                    soup = BeautifulSoup(th.get_attribute("innerHTML"), 'html.parser')
                                    tr['th'].append(str(soup.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
                                    print(soup.text)
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
                                        soup = BeautifulSoup(th.get_attribute("innerHTML"), 'html.parser')
                                        tr['th'].append(str(soup.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
                                        print(soup.text)
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
                                    soup = BeautifulSoup(td.get_attribute("innerHTML"), 'html.parser')
                                    tr['td'].append(str(soup.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
                                    print(soup.text)

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
                        print(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
                        if str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', '')!= '':
                            element['content'].append(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
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
                        print(str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', ''))
                        if str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', '') != '':
                            text += str(idx_content.text).strip().replace('\n', '').replace(' ', '').replace('\x01', '').replace('\t', '').replace('&nbsp;', '')
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

        print('\n- page about-us/team -')
        # 爬取表格資料
        self.scrape_table(about_team_dict)

        # 無內文Content資料直接設成None
        for key, ele in about_team_dict.items():
            ele['content'] = None

        self.about_team_dict = about_team_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/" + self.domain_url.replace('/', '').replace('https:', '') + "_about_team.json"
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
        # # 新官網上線後要拿掉
        # if self.domain_url == 'https://www.hannstar.com/':
        #     about_family_dict['tw']['url'] = str(about_family_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/family -')
        # 爬取表格資料
        self.scrape_table(about_family_dict)

        # 爬取Content資料
        self.scrape_content(input_dict=about_family_dict, xpath=xpath, group=list_content)


        self.about_family_dict = about_family_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/" + self.domain_url.replace('/', '').replace('https:', '') + "_about_family.json"
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
        # # 新官網上線後要拿掉
        # if self.domain_url == 'https://www.hannstar.com/':
        #     about_certification_dict['tw']['url'] = str(about_certification_dict['tw']['url']).replace('/tw', '')

        print('\n- page about-us/certification -')
        # 爬取表格資料
        self.scrape_table(about_certification_dict)

        # 爬取Content資料
        self.scrape_content(input_dict=about_certification_dict, xpath=content_xpath, group=False)

        self.about_certification_dict = about_certification_dict

        # 輸出為JSON file
        if output_json:
            file_path = "./scrape_data/" + self.domain_url.replace('/', '').replace('https:', '') + "_about_certification.json"
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
            file_path = "./scrape_data/" + self.domain_url.replace('/', '').replace('https:', '') +"_about_stronghold.json"
            with open(file_path, "w") as final:
                json.dump(about_stronghold_dict, final, indent=4)

    def __del__(self) -> None:
        """Close the driver"""
        self.driver.quit()

def scrape_website():
    '''magento'''
    # 爬蟲物件實體化
    new_cs = CustomerScraper(domain_url='https://www.hannstar.com/')
    # # 關於翰宇彩晶
    new_cs.scrape_about_team() # 關於團隊
    new_cs.scrape_about_family(list_content=True,xpath='//div[@class="Graphics3Content"]/div',output_json=True) # 關於關係企業
    new_cs.scrape_about_certification(content_xpath='//div[@class="D360TemplatesModuleBlock"]', output_json=True) # 關於認證
    new_cs.scrape_about_stronghold(content_xpath='//div[@class="AboutStrongholdBlock"]', output_json=True) # 關於全球據點

    # ESG - 公司治理
    Lst_language_mode = ['tw', 'cn', 'en']

    """ # 董事會名單 """
    Dict_json_output_final = {}
    print("董事會名單 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):

        Dict_json_output = {}
        Dict_json_output = new_cs.board_directors_supervisors(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output

    SAVE_PATH = './scrape_data/www.hannstar.com_董事會名單.json'
    new_cs.save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")


    """ 審計委員會 """
    Dict_json_output_final = {}
    print("審計委員會 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        Dict_json_output = {}
        Dict_json_output = new_cs.audit_committee(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output

    SAVE_PATH = './scrape_data/www.hannstar.com_審計委員會.json'
    new_cs.save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")


    """ 薪酬委員會 """
    Dict_json_output_final = {}
    print("薪酬委員會 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):

        Dict_json_output = {}
        Dict_json_output = new_cs.remuneration_committee(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output

    SAVE_PATH = './scrape_data/www.hannstar.com_薪酬委員會.json'
    new_cs.save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")

    """ # 內部稽核 """
    Dict_json_output_final = {}
    print("內部稽核 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):

        Dict_json_output = {}
        Dict_json_output = new_cs.auditor(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output


    SAVE_PATH = './scrape_data/www.hannstar.com_內部稽核.json'
    new_cs.save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")

    """ # 誠信經營 """
    Dict_json_output_final = {}
    print("誠信經營 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):

        Dict_json_output = {}
        Dict_json_output = new_cs.ethical_rule(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output


    #print(Dict_json_output_final)
    SAVE_PATH = './scrape_data/www.hannstar.com_誠信經營.json'
    new_cs.save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")


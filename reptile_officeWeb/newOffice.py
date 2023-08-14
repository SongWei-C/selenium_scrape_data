from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd 
from bs4 import BeautifulSoup
import json
import jsbeautifier

options = Options()
options.binary_location = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)

def table2json3(
        df, Dict_json):

    json_data = {}
    Lst_column_names = list(df.columns)
    for index, row in df.iterrows():
        json_data_tmp = {}
        json_data_tmp['{}'.format(Lst_column_names[0])] = row['{}'.format(Lst_column_names[0])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data_tmp['{}'.format(Lst_column_names[1])] = row['{}'.format(Lst_column_names[1])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data_tmp['{}'.format(Lst_column_names[2])] = row['{}'.format(Lst_column_names[2])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data['No.{}'.format(index+1)] = json_data_tmp

    return json_data

def soup_get_text(
        table_element, 
        no, 
        Dict_json):
    
    table_html = table_element.get_attribute('outerHTML')
    soup = BeautifulSoup(table_html, 'html.parser')
    text_content = soup.get_text()
    
    Dict_json['Content{}'.format(no)] = text_content.replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
    
def ethical_rule(
        Dict_json_output,
        LANGUAGE):
    
    url = "https://magentoprd.hannstar.com/{}/sustainability/governance?esgTab=Operate".format(LANGUAGE)
    driver.get(url)
    
    time.sleep(5)
    driver.get(url)
    
    Dict_json = {}
    
    # ----------------------------- 內容1 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[1]')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[1]')
    else:
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span')
        
        
    no = 1
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容2 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[1]')
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span/span')
    else:
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[1]')
    
    no = 2
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容3 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[2]')
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '/html/body/div[3]/main/div[3]/div/div/div[2]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]/span/span/span')
    else:
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[2]')
   
    no = 3
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容4 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]/span/span/span')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[2]/span/span[2]/span[3]')
    else:
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span[2]/span[3]')

        
    no = 4
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容5 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]/span/span/span')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[3]/span/span/span')
    else:
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]/span/span/span')
   
    no = 5
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容6 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[7]/span/span/span')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[4]/span/span/span')
    else:
       table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]/span/span/span')
  
    no = 6
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容7 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[8]/span/span/span')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[5]/span/span/span')
    else:
       table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]/span/span/span')
   
    no = 7
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容8 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[9]/span/span')
    elif (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[6]/span/span')
    else:
       table_element = driver.find_element('xpath', '//*[@id="root_SustainabilityGovernance"]/div[2]/div/div[1]/div[5]/div/div/div/div/div/p[7]/span/span')
       
    no = 8
    soup_get_text(table_element, no, Dict_json)
    
    Dict_json_output['誠信經營'] = Dict_json
    
    print("{} process SUCCESS".format(url))
    
    return Dict_json_output
    
def auditor(
        Dict_json_output,
        LANGUAGE):
    
    url = "https://magentoprd.hannstar.com/{}/sustainability/governance?esgTab=Check".format(LANGUAGE)
    driver.get(url)
    
    time.sleep(5)
    driver.get(url)
    
    Dict_json = {}
    
    # ----------------------------- 內容1 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[1]/span/span/strong")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[1]/span/strong")
    
    no = 1
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容2 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span[1]")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[3]")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span/span[1]")
    
    no = 2
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容3 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span[2]/span/span/strong")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[4]/span/span/strong")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[2]/span/span[2]/span/strong")
   
    no = 3
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容4 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[5]/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[3]/span/span")
   
    no = 4
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容5 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[6]/span/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[4]/span/span")
   
    no = 5
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容6 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[7]/span/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[5]/span/span")
   
    no = 6
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容7 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[8]/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[6]/span")
   
    no = 7
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容8 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[1]/span/span/strong")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[1]/span[1]/span/strong")
   
    no = 8
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容9 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div/p[9]/span")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[2]/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[2]/span")
   
    no = 9
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容10 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p/span/span/strong")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[4]/span/strong")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p[4]/span[1]/strong")
   
    no = 10
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 表格1 ----------------------------------------------------
    
    # 定位表格元素
    time.sleep(2)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[2]")
    
    table_html = table_element.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    
    json_data = table2json3(df, Dict_json)
    Dict_json['Table1'] = json_data
    
    
    # ----------------------------- 內容11 ----------------------------------------------------
    time.sleep(2)
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[1]/span/span/strong")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[1]/strong/span")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]/span/span/strong")
   
    no = 11
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容12 ----------------------------------------------------
    time.sleep(2)
    
    if (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]")
    elif (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[2]")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[3]/div/p[3]")
   
    no = 12
    soup_get_text(table_element, no, Dict_json)
    
    Dict_json_output['內部稽核'] = Dict_json
    
    print("{} process SUCCESS".format(url))
    
    return Dict_json_output


def remuneration_committee(
        Dict_json_output,
        LANGUAGE):
    
    url = "https://magentoprd.hannstar.com/{}/sustainability/governance?esgTab=Salary".format(LANGUAGE)
    driver.get(url)
    
    time.sleep(5)
    driver.get(url)
    
    Dict_json = {}
    
    # ----------------------------- 內容1 ----------------------------------------------------
    time.sleep(5)
    if (LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[1]/span[2]/strong")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[1]/span[1]/strong")

   
    no = 1
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 內容2 ----------------------------------------------------
    time.sleep(5)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]/p[2]/span")

    
    no = 2
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 表格1 ----------------------------------------------------
    
    # 定位表格元素
    time.sleep(5)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[4]/div/div/div/div/div[2]/table")
    
    table_html = table_element.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    
    json_data = table2json3(df, Dict_json)
    Dict_json['Table1'] = json_data
    
    Dict_json_output['薪酬委員會'] = Dict_json
    
    print("{} process SUCCESS".format(url))
    
    return Dict_json_output
    
def audit_committee(
        Dict_json_output,
        LANGUAGE):
    
    url = "https://magentoprd.hannstar.com/{}/sustainability/governance?esgTab=Audit".format(LANGUAGE)
    driver.get(url)
    
    time.sleep(5)
    driver.get(url)
    
    Dict_json = {}
    
    # ----------------------------- 內容1 ----------------------------------------------------
    time.sleep(5)
    if (LANGUAGE == 'tw'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[1]/p/span[2]")
    elif (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]")
    else:
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[1]/p/span[4]")
        
    
    no = 1
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 表格1 ----------------------------------------------------
    
    # 定位表格元素
    time.sleep(5)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[1]/div[2]/table")
    table_html = table_element.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    
    json_data = table2json3(df, Dict_json)
    Dict_json['Table1'] = json_data

    # ----------------------------- 內容2 ----------------------------------------------------
    time.sleep(5)
    if (LANGUAGE == 'tw' or LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[1]/p/span/strong")
    
    no = 2
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 表格2 ----------------------------------------------------

    # 定位表格元素
    time.sleep(5)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div[2]/div[2]/table")
    table_html = table_element.get_attribute('outerHTML')
    df = pd.read_html(table_html, header=0)[0]
    
    json_data = {}
    Lst_column_names = list(df.columns)
    for index, row in df.iterrows():
        json_data_tmp = {}
        json_data_tmp['{}'.format(Lst_column_names[0])] = row['{}'.format(Lst_column_names[0])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data_tmp['{}'.format(Lst_column_names[1])] = row['{}'.format(Lst_column_names[1])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data_tmp['{}'.format(Lst_column_names[2])] = row['{}'.format(Lst_column_names[2])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')
        json_data_tmp['{}'.format(Lst_column_names[3])] = row['{}'.format(Lst_column_names[3])].replace('\t', '').replace('\r', '').replace('\n', '').replace('\\', '')

        json_data['No.{}'.format(index+1)] = json_data_tmp
        
    Dict_json['Table2'] = json_data    
    
    Dict_json_output['審計委員會'] = Dict_json
    
    print("{} process SUCCESS".format(url))
    
    return Dict_json_output

def board_directors_supervisors(
        Dict_json_output,
        LANGUAGE):
    
    url = "https://magentoprd.hannstar.com/{}/sustainability/governance".format(LANGUAGE)
    driver.get(url)
    
    time.sleep(5)
    driver.get(url)

    Dict_json = {}
    
    # ----------------------------- 內容1 ----------------------------------------------------
    time.sleep(5)
    if (LANGUAGE == 'tw' or LANGUAGE == 'en'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]/p/span")
    elif (LANGUAGE == 'cn'):
        table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]")
    
    no = 1
    soup_get_text(table_element, no, Dict_json)
    
    # ----------------------------- 表格1 ----------------------------------------------------
    
    # 定位表格元素
    time.sleep(5)
    table_element = driver.find_element('xpath', "//*[@id='root_SustainabilityGovernance']/div[2]/div/div[1]/div[5]/div/div/div/div/div[2]/table")
    table_html = table_element.get_attribute('outerHTML')
    df = pd.read_html(table_html)[0]
    
    json_data = table2json3(df, Dict_json)
    Dict_json['Table1'] = json_data
    
    Dict_json_output['董事會名單'] = Dict_json
    
    print("{} process SUCCESS".format(url))
    
    return Dict_json_output

def save2json(
        SAVE_PATH: str,
        Dict_json_output_final: dict):
    
    options = jsbeautifier.default_options()
    options.indent_size = 4
    
    with open(SAVE_PATH, 'w', encoding='utf-8') as json_file:
         json_file.write(jsbeautifier.beautify(json.dumps(Dict_json_output_final, ensure_ascii=False), options))
         
if __name__ == '__main__':

    
    Lst_language_mode = ['tw', 'cn', 'en']
    
    """ # 董事會名單
    Dict_json_output_final = {}
    print("董事會名單 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        
        Dict_json_output = {}
        Dict_json_output = board_directors_supervisors(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
    
    SAVE_PATH = './新官網_公司治理/董事會名單.json'
    save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")
    """
    
    #""" # 審計委員會
    Dict_json_output_final = {}
    print("審計委員會 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        
        Dict_json_output = {}
        Dict_json_output = audit_committee(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
        
    SAVE_PATH = './新官網_公司治理/審計委員會.json'
    save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")
    #"""
    
    """ # 薪酬委員會
    Dict_json_output_final = {}
    print("薪酬委員會 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        
        Dict_json_output = {}
        Dict_json_output = remuneration_committee(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
    
    SAVE_PATH = './新官網_公司治理/薪酬委員會.json'
    save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")
    """
    
    """ # 內部稽核
    Dict_json_output_final = {}
    print("內部稽核 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        
        Dict_json_output = {}
        Dict_json_output = auditor(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
        
    
    SAVE_PATH = './新官網_公司治理/內部稽核.json'
    save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")
    """
    """
    # 誠信經營
    Dict_json_output_final = {}
    print("誠信經營 process ...")
    for i, LANGUAGE in enumerate(Lst_language_mode):
        
        Dict_json_output = {}
        Dict_json_output = ethical_rule(Dict_json_output, LANGUAGE)
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
        Dict_json_output_final['{}'.format(LANGUAGE)] = Dict_json_output
        
    
    #print(Dict_json_output_final)
    SAVE_PATH = './新官網_公司治理/誠信經營.json'
    save2json(SAVE_PATH, Dict_json_output_final)
    print("---------------------------------------------------")
    """
    
    driver.quit()  # 關閉瀏覽器，釋放資源
    
    
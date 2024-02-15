from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import FirefoxOptions #for Firefox 
import time
import requests
import json


def sp_test():
    
    #for Edge
    
    #option = webdriver.EdgeOptions()
    #option.add_argument("headless")
    #driver = webdriver.Edge(options=option)
    driver = webdriver.Edge()
    
    #for Firefox
    '''
    option = FirefoxOptions()
    option.add_argument("-headless")
    driver = webdriver.Firefox(options=option)
    '''
    for i in range (0,23):
    
        driver.get('https://sp.tanet.edu.tw/')
        time.sleep(5)
        select_server_btn = driver.find_element(by = By.XPATH , value="//div[@id='test__params']/ul/li/div[2]")
        select_server_btn.click()
        
        value_ = '//div[@data-value="'+str(i)+'"]'
        
        select_server = driver.find_element(by = By.XPATH , value=value_)
        ActionChains(driver).move_to_element(select_server).click(select_server).perform()
        #滑鼠要滑過去才會顯示元件所以要這樣寫
        #select_server.click()
        start_btn = driver.find_element(by = By.XPATH , value='//button[@id="btn-start"]')
        start_btn.click()
        time.sleep(5)
        data = html.fromstring(driver.page_source)
        txt = data.xpath(value_+'/text()')
        print(txt[0])
        popup_txt = data.xpath('//div[@id="popup-info__text"]/text()')
        if 'The target server is unreachable!' in popup_txt :
            srever_ = data.xpath(value_+'/text()')
            print(srever_[0])
            line_notify('test fail' +srever_[0]) 
        time.sleep(20)

        data = html.fromstring(driver.page_source)
        
        v4_data = data.xpath('//span[@id="jit__value--ipv4"]/text()')
        #v6_data = data.xpath('//span[@id="jit__value--ipv6"]/text()')
        print(v4_data[0])
        if '-' in v4_data[0]:
            srever_ = data.xpath(value_+'/text()')
            line_notify('test fail'+srever_)
        #print(v6_data[0])
        

        
def line_notify(text): 
    config_file = open(r'C:\config_1.json','r',encoding='utf-8')
    config_file = json.loads(config_file.read())
    token = config_file['token']
    headers = {
            "Authorization": "Bearer " + ""+token+"",
            "Content-Type": "application/x-www-form-urlencoded"} 

    params = {'message':'\n'+text}

    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)





if __name__ == "__main__":
    sp_test()
    #line_notify('test')
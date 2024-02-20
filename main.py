from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import json


def sp_test():
    
    #for Edge
    
    #option = webdriver.EdgeOptions()
    #option.add_argument("headless")
    #driver = webdriver.Edge(options=option)
    driver = webdriver.Edge()
    srever_ = ['init']
    #for Firefox
    '''
    option = FirefoxOptions()
    option.add_argument("-headless")
    driver = webdriver.Firefox(options=option)
    '''
    try:
        for i in range (0,23):
            driver.get('https://sp.tanet.edu.tw/')
            count = 0
            while True :
                data = html.fromstring(driver.page_source)
                text = data.xpath("//div[@data-value='1']")
                count += 1 
                time.sleep(1)
                if str(text[0].text) == '基隆市':
                    break
                if count > 30 :
                    line_notify('init test failed '+srever_[0])
                    quit()
                time.sleep(1)

            #time.sleep(10)

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
            #popup_txt = data.xpath('//div[@id="popup-info__text"]/text()')
            popup_txt = driver.find_element(by = By.XPATH , value='//div[@id="popup-info__text"]')
            srever_ = data.xpath(value_+'/text()')
            #print(popup_txt)          
            if popup_txt.text != '' :
                
                #print(srever_[0])
                line_notify('test failed ' +srever_[0]) 
                continue

            time.sleep(80)

            #data = html.fromstring(driver.page_source)
            #v4_data = driver.find_element(by = By.XPATH , value='//span[@id="jit__value--ipv4"]')
            #print(v4_data.text)
            #v4_data = data.xpath('//span[@id="jit__value--ipv4"]/text()')
            #v4_data = data.xpath('//span[@id="upl__value--ipv4"]/text()')
            #v6_data = data.xpath('//span[@id="jit__value--ipv6"]/text()')
            v4_data = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv4"]')
            v6_data = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv6"]')
            #print(v4_data[0])


            try:
                float(v4_data.text)
            except:
                srever_ = data.xpath(value_+'/text()')
                line_notify('test v4 failed by value '+srever_[0])
                continue
            try:
                float(v6_data.text)
            except:
                srever_ = data.xpath(value_+'/text()')
                line_notify('test v6 failed by value '+srever_[0])
                continue

    except Exception as e :
        line_notify(str(e))
        driver.close()
    driver.close()

        #line_notify('test all failed')

        #print(v6_data[0])
        
def test():
    driver = webdriver.Edge()
    driver.get('https://sp.tanet.edu.tw/')
    count = 0
    while True :
        #print('E')
        data = html.fromstring(driver.page_source)
        text = data.xpath("//div[@data-value='1']")
        #print(text[0].text)

        #text = driver.find_element(by=By.XPATH , value="//div[@data-value='1']")
        #print(text.text)
        
        count += 1 
        time.sleep(1)

        
        if str(text[0].text) == '基隆市':
            print(text[0].text)
            break
        #print('E')
        print(text[0].text)
        time.sleep(1)
    
    print('use  ' +str(count)  + 's') 
def line_notify(text): 
    config_file = open(r'C:\config.json','r',encoding='utf-8')
    config_file = json.loads(config_file.read())
    token = config_file['token']
    headers = {
            "Authorization": "Bearer " + ""+token+"",
            "Content-Type": "application/x-www-form-urlencoded"} 

    params = {'message':'\n'+text}

    requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)





if __name__ == "__main__":
    sp_test()
    line_notify('測試完成')

        
 
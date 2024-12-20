from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import html
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import json
import sys

def sp_test():
    
    #for Edge
    option = webdriver.EdgeOptions()
    option.add_argument("headless")
    option.add_argument("--blink-settings=imagesEnabled=false")
    option.add_argument("--disable-gpu")
    """ option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1,
    }) """
    driver = webdriver.Edge(options=option)
    """ driver.execute_cdp_cmd('Network.enable', {})
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'latency': 0,  
        'downloadThroughput': 1000 * 1024,  
        'uploadThroughput': 1000 * 1024,    
    }) """
    #driver = webdriver.Edge()
    server_value = [18 , 204 , 191 , 192 , 193 , 208 , 201 , 194 , 195 , 196 , 205 , 203 , 197 , 198 , 206 , 202 , 190 , 200 , 199 , 207 , 20 , 1 , 19 , 21 , 22 , 23 , 
                    24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 15 , 34 , 35 , 36 , 37 , 38]
    
    server_ = ['init']
    re_test_list = []
    except_count = 0
    retry_count = 0
    init_retry = 0
    #for Firefox
    '''
    option = FirefoxOptions()
    option.add_argument("-headless")
    driver = webdriver.Firefox(options=option)
    '''
    for i in server_value:
    #for i in range (-1,1):
        try:
            count = 0
            while True :
                driver.get('https://sp.tanet.edu.tw/')
                time.sleep(5)
                data = html.fromstring(driver.page_source)
                text = data.xpath("/html/body/div[1]/main/section[1]/div/div/ul/li[2]/div[2]/div[1]/div")
                count += 1        
                time.sleep(1)
                if  '教網中心' in str(text[0].text) or str(text[0].text) == '教育部' :
            
                    break
                if count > 30 :
                    if init_retry > 10 :
                        line_notify('伺服器列表讀取失敗')
                        sys.exit()
                    else:
                        init_retry = init_retry + 1
                        i = i - 1
                        continue
                else:
                    continue
                time.sleep(1)
            
            #time.sleep(10)

            select_server_btn = driver.find_element(by = By.XPATH , value="//div[@id='test__params']/ul/li/div[2]")

            select_server_btn.click()
            
            #value_ = '//div[@class="choices__list choices__list--dropdown"]/div[1]/div['+str(i)+']'
            #choices--server__select-item-choice-1
            value_ = '//li[@data-item-value='+str(i)+']'
            
            select_server = driver.find_element(by = By.XPATH , value=value_)
            ActionChains(driver).move_to_element(select_server).click(select_server).perform()
            #滑鼠要滑過去才會顯示元件所以要這樣寫
            #select_server.click()
            start_btn = driver.find_element(by = By.XPATH , value='//button[@id="btn-start"]')
            start_btn.click()
            time.sleep(10)
            #popup_txt = data.xpath('//div[@id="popup-info__text"]/text()')
            popup_txt = driver.find_element(by = By.XPATH , value='//div[@id="popup-info__text"]')
            server_ = data.xpath(value_+"/div")
     
            #srever_ = data.xpath("//div[@data-value='1']/text()")
            
            #print(popuv6p_txt)
            print(server_[0].text)
            if popup_txt.text != '' :
                
                #print(server_[0])
                #line_notify('測試失敗 ' +srever_[0]+' '+popup_txt.text) 
                re_test_list.append(i)
                continue

            time.sleep(75)

            #data = html.fromstring(driver.page_source)
            #v4_data = driver.find_element(by = By.XPATH , value='//span[@id="jit__value--ipv4"]')
            #print(v4_data.text)
            v4_ping = driver.find_element(by= By.XPATH , value='//span[@id="ping__value--ipv4"]')
            v4_jit = driver.find_element(by= By.XPATH , value='//span[@id="jit__value--ipv4"]')
            v4_upl = driver.find_element(by= By.XPATH , value='//span[@id="upl__value--ipv4"]')
            v4_down = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv4"]')
            v6_ping = driver.find_element(by= By.XPATH , value='//span[@id="ping__value--ipv6"]')
            v6_jit =driver.find_element(by= By.XPATH , value='//span[@id="jit__value--ipv6"]')
            v6_down = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv6"]')
            v6_upl = driver.find_element(by= By.XPATH , value='//span[@id="upl__value--ipv6"]')
            #print(v4_data[0])
            print(v4_ping.text , v4_jit.text , v4_down.text , v4_upl.text , v6_ping.text , v6_jit.text , v6_down.text , v6_upl.text)
            #print(type(v6_down.text))
            try:
                float(v4_ping.text)
                float(v4_jit.text)
                float(v4_down.text)
                float(v4_upl.text)
                if v6_ping.text != '' :
                    float(v6_ping.text)
                    float(v6_jit.text)
                    float(v6_down.text)
                    float(v6_upl.text)
            except:
                re_test_list.append(i)
                continue
        

        except NoSuchElementException as e:
            except_count = except_count + 1
            print(e)
            if except_count > 2 :
                line_notify('伺服器選擇失敗')
                driver.close()
                sys.exit()

        except Exception as e :
            if 'CONNECTION_REFUSED' in str(e) or 'CONNECTION_TIMED_OUT' in str(e):
                retry_count = retry_count + 1
                if retry_count > 3 :
                    line_notify('連線失敗 connection refused')
                    driver.close()
                    sys.exit()
                
            else:
                line_notify(str(e))
            continue

    driver.close()
    return re_test_list
        #line_notify('test all failed')

        #print(v6_data[0])
def re_sp_test(re_test_list):
    option = webdriver.EdgeOptions()
    option.add_argument("headless")
    option.add_argument("--blink-settings=imagesEnabled=false")
    option.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=option)
    server_ = ['init']
    init_retry = 0
    #for Firefox
    '''
    option = FirefoxOptions()
    option.add_argument("-headless")
    driver = webdriver.Firefox(options=option)
    '''
    for i in re_test_list:
        try:
            count = 0
            while True :
                driver.get('https://sp.tanet.edu.tw/')
                time.sleep(5)
                data = html.fromstring(driver.page_source)
                text = data.xpath("/html/body/div[1]/main/section[1]/div/div/ul/li[2]/div[2]/div[1]/div")
                count += 1        
                time.sleep(1)
                if  '教網中心' in str(text[0].text) or str(text[0].text) == '教育部' :
            
                    break
                if count > 30 :
                    if init_retry > 10 :
                        line_notify('伺服器列表讀取失敗')
                        sys.exit()
                    else:
                        init_retry = init_retry + 1
                        i = i - 1
                        continue
                else:
                    continue
                time.sleep(1)

            #time.sleep(10)

            select_server_btn = driver.find_element(by = By.XPATH , value="//div[@id='test__params']/ul/li/div[2]")

            select_server_btn.click()
            
            value_ = '//li[@data-item-value='+str(i)+']'
            #value_ = '//div[@data-value="5"]'
            select_server = driver.find_element(by = By.XPATH , value=value_)
            ActionChains(driver).move_to_element(select_server).click(select_server).perform()
            #滑鼠要滑過去才會顯示元件所以要這樣寫
            #select_server.click()
            start_btn = driver.find_element(by = By.XPATH , value='//button[@id="btn-start"]')
            start_btn.click()
            time.sleep(10)
            #popup_txt = data.xpath('//div[@id="popup-info__text"]/text()')
            popup_txt = driver.find_element(by = By.XPATH , value='//div[@id="popup-info__text"]')
            server_ = data.xpath(value_+"/div")
     
            #srever_ = data.xpath("//div[@data-value='1']/text()")
            
            #print(popuv6p_txt)
            print(server_[0].text)
            if popup_txt.text != '' :
                
                #print(server_[0])
                line_notify('測試失敗 ' +server_[0].text+' '+popup_txt.text) 
                continue

            time.sleep(75)

            #data = html.fromstring(driver.page_source)
            #v4_data = driver.find_element(by = By.XPATH , value='//span[@id="jit__value--ipv4"]')
            #print(v4_data.text)
            v4_ping = driver.find_element(by= By.XPATH , value='//span[@id="ping__value--ipv4"]')
            v4_jit = driver.find_element(by= By.XPATH , value='//span[@id="jit__value--ipv4"]')
            v4_upl = driver.find_element(by= By.XPATH , value='//span[@id="upl__value--ipv4"]')
            v4_down = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv4"]')
            v6_ping = driver.find_element(by= By.XPATH , value='//span[@id="ping__value--ipv6"]')
    
            v6_jit =driver.find_element(by= By.XPATH , value='//span[@id="jit__value--ipv6"]')
            v6_down = driver.find_element(by = By.XPATH , value='//span[@id="down__value--ipv6"]')
            v6_upl = driver.find_element(by= By.XPATH , value='//span[@id="upl__value--ipv6"]')
            #print(v4_data[0])
            print(v4_ping.text , v4_jit.text , v4_down.text , v4_upl.text , v6_ping.text , v6_jit.text , v6_down.text , v6_upl.text)
           
            try:
                float(v4_ping.text)
            except:
                line_notify(server_[0].text+'v4 ping 測試失敗  text = '+v4_ping.text)
                continue
            try:
                float(v4_jit.text)
            except:
                line_notify(server_[0].text+'v4 jitter 測試失敗  text = '+v4_jit.text)
                continue
            try:
                float(v4_down.text)
            except:
                line_notify(server_[0].text+'v4 download 測試失敗  text = '+v4_down.text)
                continue
            try:
                float(v4_upl.text)
            except:
                line_notify(server_[0].text+'v4 upload 測試失敗  text = '+v4_upl.text)
                continue
            if v6_ping.text != '' :
                try:
                    float(v6_ping.text)
                except:
                    line_notify(server_[0].text+'v6 ping 測試失敗  text = '+v6_ping.text)
                    continue
                try:
                    float(v6_jit.text)
                except:
                    line_notify(server_[0].text+'v6 jitter 測試失敗  text = '+v6_jit.text)
                    continue
                try:
                    float(v6_down.text)
                except:
                    line_notify(server_[0].text+'v6 download 測試失敗  text = '+v6_down.text)
                    continue
                try:
                    float(v6_upl.text)
                except:
                    line_notify(server_[0].text+'v6 upload 測試失敗  text = '+v6_upl.text)
                    continue

        except Exception as e :
            if 'CONNECTION_REFUSED' in str(e):
                retry_count = retry_count + 1
                if retry_count > 3 :
                    line_notify('連線失敗')
                    driver.close()
                    sys.exit()
                
            else:
                line_notify(str(e))
            continue
    driver.close()

def line_notify(text): 
    
    config_file = open(r'C:\config.json','r',encoding='utf-8')
    config_file = json.loads(config_file.read())
    token = config_file['token']
    headers = {
            "Authorization": "Bearer " + ""+token+"",
            "Content-Type": "application/x-www-form-urlencoded"} 

    params = {'message':'\n'+text}

    requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    
    #print('\n\n\n\n\n\nexception\n\n\n\n\n\n'+text)
    
    #print(text)
def test():
    '''
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
    '''
    v4_ping = '1.0'
    v4_jit = '2.0'
    v4_down = '-'
    try:
        float(v4_ping)
        float(v4_jit)
        float(v4_down)
    except Exception as e:
        print(str(e))


def main():
    re_test_list = sp_test()
    if re_test_list == []:
        line_notify('測試完成')
    else:
        re_sp_test(re_test_list=re_test_list)
        line_notify('測試完成(複測)')



if __name__ == "__main__":
    #test()
    #sp_test()
    #line_notify('測試完成')
    main()
 
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv

#ヘッドレスモード
#options = Options()
#options.add_argument('--headless')
#driver = webdriver.Chrome#('/Users/gst/AppData/Local/Programs/Python/Python37/chromedriver', #chrome_options=options)

#ヘッドありモード
driver = webdriver.Chrome()

url = 'https://www.alis-ac.jp/FarmSearch'

driver.implicitly_wait(10)

driver.get(url)

def get_results(number):
    nouti_list = []
    print('checking'+str(number+1))
    shosai = driver.find_elements_by_class_name('button_small')[number]
    shosai.click()
    time.sleep(2)
    farm_adress = driver.find_element_by_id('selectedfarm_address')
    farmer_number = driver.find_element_by_id('selectedfarm_farmer_indication_number_hash')
    land_code = driver.find_element_by_id('selectedfarm_classification_of_land_code_name')
    farm_area = driver.find_element_by_id('selectedfarm_disp_area_on_registry')
    tyukanken = driver.find_element_by_id('selectedfarm_right_setting_contents_code_name')
    yukyu_nou = driver.find_element_by_id('selectedfarm_usage_situation_investigation_result_code_name')
    tinshaku  = driver.find_element_by_id('selectedfarm_kind_of_right_code_name')
    list_area = farm_area.text.split('(')
    time.sleep(2)
    area_b = list_area[1]
    area_a = area_b.strip("a)")
    jav_text = driver.find_element_by_xpath('/html/body/script[7]')
    ja_text = jav_text.get_attribute('innerHTML')
    list_text = ja_text.split(';')
    strin = list_text[19]
    lonlat = strin.split(':')
    lon = lonlat[2]
    lat = lonlat[3]
    longitude = lon[0:13]
    latitude = lat[0:12]
    nouti_list.append(farm_adress.text)
    nouti_list.append(farmer_number.text)
    nouti_list.append(land_code.text)
    nouti_list.append(area_a)
    nouti_list.append(longitude)
    nouti_list.append(latitude)
    nouti_list.append(tyukanken.text)
    nouti_list.append(yukyu_nou.text)
    nouti_list.append(tinshaku.text)
    with open('nouti.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(nouti_list)


def nisiwaki_results(shuraku_num):
    #参照ボタンをクリック
    driver.find_element_by_id('addressLinkA').click()
    #小窓ブラウザに移動
    new_window = driver.window_handles[1]
    driver.switch_to_window(new_window)
    #兵庫県をクリック
    driver.find_element_by_xpath("//*[text()=\"兵庫県\"]").click()
    #市町村をクリック
    driver.find_element_by_xpath("//*[text()=\"姫路市\"]").click()
    #集落をクリック
    driver.find_elements_by_xpath("//a")[shuraku_num].click()
    #小窓ブラウザから移動
    old_window = driver.window_handles[-1]
    driver.switch_to_window(old_window)
    #検索して一覧を表示するをクリック
    driver.execute_script("submitSearch(); return false;")
    
    #途中で止まった頁（page）まで行く
    #val = 1
    #page = 8
    #while val < page:
    #    print(val)
    #    driver.find_element_by_class_name('next').click()
    #    val = val + 1

    page_num = 1
    while True:
        if len(driver.find_elements_by_class_name('next'))>0:
            print("-----------------------page",page_num)
            for number in range(0, 30):
                get_results(number)
                driver.back()
            page_num += 1
            driver.find_element_by_class_name('next').click()
        else:
            print("----------------------last_page")
            limit = len(driver.find_elements_by_class_name('button_small'))
            print(limit)
            for number in range(0, limit):
                get_results(number)
                driver.back()
            #戻るボタンを押す
            driver.execute_script("submitFromLink(0, '/FarmSearch'); return false;")
            print("--------------shuraku finished!--------------")
            break

#range(1,集落の数+1)
#
for shuraku_num in range(117,182):
    nisiwaki_results(shuraku_num)
input('Press ENTER to close the automated browser')
driver.quit()
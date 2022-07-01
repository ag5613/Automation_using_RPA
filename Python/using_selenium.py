import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import re
import os

options = Options()

options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path=r'chromedriver',chrome_options=options)
url = 'https://www.google.com/maps/@31.2999936,75.5826688,14z'
'''
with open("input_file.txt","r",encoding="utf8") as f:
    shipper = f.read().split("\n")
'''

input_data = pd.read_csv("test2.csv",encoding='utf-8')
shipper = list(input_data.iloc[:,0])[:10000]
address = list(input_data.iloc[:,1])[:10000]

for indexx,s_details in enumerate(shipper[:10]):
    driver.get(url)
    time.sleep(2)
    aa = driver.find_element(By.XPATH,"//input[@class = 'tactile-searchbox-input']")
##    print(aa)
    aa.send_keys(s_details)
    aa.send_keys(Keys.ENTER)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    aaa = [i.text for i in soup.findAll(class_ = 'Io6YTe fontBodyMedium')]
##    print(aaa)
##    print(len(aaa))
    a,p,m,w = (" ",)*4
    if(len(aaa)!=0):
        a = aaa[0]
    for i in aaa:
        ph = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',i)
        ma = re.findall(r'\S+@\S+',i)
        we = re.findall(r'(?: |//|^)([A-Za-z0-9]{1,}\.[A-Za-z0-9]{1,10}\.?[A-Za-z]{0,}\.?[A-Za-z]{1,})(?: |/|$)',i)
        if(p == " " and len(ph) != 0):
            p = ph[0]
        if(m == " " and len(ma) != 0):
            m = ma[0]
        if(w == " " and len(we) != 0):
            w = we[0]
    data= {"Name" : [s_details],"Address":[a],"Phone":[p],"Website":[w],"Mail":[m],"Original_Address":[address[indexx]]}
    print(data)
    df = pd.DataFrame(data)
    if(os.path.isfile("existing1.csv")):
        df.to_csv('existing1.csv', mode='a', index=False, header=False)
    else:
        df.to_csv('existing1.csv',index=False)
##    print(f"Name {s_details}\nPhone : {p}\nWebsite : {w}\nMail : {m}")
##    print("\n\n")
        
    '''
    
    a,b,c,d =(" ",)*4
    try:
        a = [i.text for i in soup.findAll(class_ = 'Io6YTe fontBodyMedium')[0]]
    except:
        pass
    try:
        b = [i.text for i in soup.findAll(class_ = 'Io6YTe fontBodyMedium')[1]]
    except:
        pass
    try:
        c = [i.text for i in soup.findAll(class_ = 'Io6YTe fontBodyMedium')[2]]
    except:
        pass
    try:
        d = [i.text for i in soup.findAll(class_ = 'Io6YTe fontBodyMedium')[3]]
    except:
        pass
    temp = {"a" : a,"b" : b,"c" : c,"d": d}
    final_data= []
    final_data.append(temp)
    print(final_data)

'''






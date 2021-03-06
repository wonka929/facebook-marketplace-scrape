#!/usr/bin/env python
# coding: utf-8

# In[19]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from tqdm import trange, tqdm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
from thefuzz import process



with open('cities.pickle', 'rb') as f:
    cities = pickle.load(f)

    
def scrape(n_pag=5):
    for i in trange(n_pag):
        sleep(3)
        driver.find_element(by='tag name', value='html').send_keys(Keys.END)

    html = driver.page_source
    soup = BeautifulSoup(html)
    return soup


## Browser setup

try:
    brow = 'Chrome'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    #options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--window-size=1376,768')

    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
except:
    brow = 'Edge'
    print('Chrome non è presente, passo ad Edge...')
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-infobars")
    #options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--window-size=1376,768')

    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    options.add_argument("headless")
    driver = webdriver.Edge(options=options)


 ## Facebook Login



    
#driver.get('https://it-it.facebook.com/login/?next=%2Fmarketplace%2F')

driver.get('https://it-it.facebook.com/marketplace/turin/search/?query=')

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Consenti solo i cookie essenziali']"))).click()

print('\n //  Digitare "q" nella chiave di ricerca per uscire dal processo di scraping. // \n')

while True:
    
    chiave_ricerca = input("Inserisci la chiave di ricerca: ")
    if chiave_ricerca == 'q':
        break
    chiave_ricerca = chiave_ricerca.replace(' ',' ')
    
    citta = input("Inserisci la città: ")
    identified = process.extractOne(citta, cities.keys())
    print("Ho trovato questa città: procedo con essa...", "\n\t-", identified[0]), 
    
    id = str(cities[identified[0]])
    
    pagine = input("Inserisci il numero di pagine da analizzare: ")
    pagine = int(pagine)
    
    driver.get('https://it-it.facebook.com/marketplace/' + id + '/search/?query=' + chiave_ricerca)
    
    sleep(3)
    
    soup = scrape(pagine)
    
    with open( citta + '_' + chiave_ricerca.replace(' ','_') + ".html", "w", encoding='utf-8') as file:
        file.write(str(soup))

driver.quit()

for file in os.listdir():
    if file.endswith('.html'):
        with open(file, 'r', encoding='utf-8') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
        
        output = pd.DataFrame()
        a = soup.findAll("div", {"class" : "kbiprv82"})

        for elem in a:
            try:
                if brow == 'Chrome':
                    link = '<a href=https://it-it.facebook.com' + elem.findAll("a", {"class" : "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l"})[0]['href'] + '>' + 'Link annuncio' + '</a>'
                    prezzo = elem.findAll("span", {"class" : "d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 tia6h79c iv3no6db a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"})[0].text
                    descrizione = elem.findAll("span", {"class" : "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7"})[0].text
                    location = elem.findAll("span", {"class" : "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5"})[0].text
                    prezzo = re.findall(r'\b\d+\b', prezzo)[0]
                    image = '<img src="'+ elem.find('img')['src'] + '">'
                    dic = {
                        'descrizione' : descrizione,
                        'prezzo' : prezzo,
                        'location' : location,
                        'link' : link,
                        'immagine' : image
                    }
                    
                    output = output.append(dic, ignore_index=True)
                
                elif brow == 'Edge':
                    link = '<a href=https://it-it.facebook.com' + elem.findAll("a", {"class" : "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l"})[0]['href'] + '>' + 'Link annuncio' + '</a>'
                    prezzo = elem.findAll("span", {"class" : "d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id"})[0].text
                    descrizione = elem.findAll("span", {"class" : "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7"})[0].text
                    location = elem.findAll("span", {"class" : "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5 ojkyduve"})[0].text
                    prezzo = re.findall(r'\b\d+\b', prezzo)[0]
                    image = '<img src="'+ elem.find('img')['src'] + '">'
                    dic = {
                        'descrizione' : descrizione,
                        'prezzo' : prezzo,
                        'location' : location,
                        'link' : link,
                        'immagine' : image
                    }
                    
                    output = output.append(dic, ignore_index=True)
                    
            except Exception as e:
                print(e)
                continue
        
        output['prezzo'] = pd.to_numeric(output['prezzo'], errors='coerce')
        output = output.sort_values(by='prezzo').reset_index(drop=True)
        output.to_csv(file.split('.')[0] + '.csv', sep=';')
        output.to_html(file.split('.')[0] + '_web.html', escape=False)


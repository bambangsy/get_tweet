#import library yang diperlukan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

#Ini adalah fungsi untuk scrap gmaps berdasarkan keyword, latitude, longitude
def scrapGmaps(keyword,namafile,latitude,longitude):
   #variable
   lat =  latitude
   long = longitude

   #buat instance chrome baru
   driver = webdriver.Chrome(r"C:\Program Files (x86)\chromedriver.exe")
   driver.get(f'https://www.google.com/maps/@{lat},{long},14z')

   WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
   
   #search ambulan
   search_bar = driver.find_element(By.XPATH,'//*[@id="searchboxinput"]')
   search_bar.send_keys(keyword)
   time.sleep(1)
   search_press = driver.find_element(By.XPATH,'//*[@id="searchbox-searchbutton"]')
   search_press.click()
   
   WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')))
  
   start_time = time.time()
   window = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
   
   while time.time() < start_time + 15:#waktu scroll 15 detik
      time.sleep(0.1)
      window.send_keys(Keys.END)

   #scrapping lahh
   detail_elements = driver.find_elements(By.XPATH,"//*[@class='Z8fK3b']/div[2]/div[4]")
   link_elements = driver.find_elements(By.XPATH,'//*[@class="hfpxzc"]')
   detail = [detail.text for detail in detail_elements]
   link = [link.get_attribute("href") for link in link_elements]
   title = [link.get_attribute("aria-label") for link in link_elements]

   titles = []
   details = []
   links = []
   data = []

   for i,j,k in zip(title,detail,link):
      j = re.sub(r"\n", " ", j)
      titles.append(i)
      details.append(j)
      links.append(k)
      data.append([i,j,k])

   if len(titles) == len(details) == len(links):
      pd.DataFrame(data).to_csv(namafile,index=False,mode="a",header=False)
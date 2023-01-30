import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import pandas as pd

#Code pour ouvrir la page web sur le navigateur grace à selenium
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
FireFoxDreiverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
FireFoxProfile = webdriver.FirefoxProfile()
FireFoxProfile.set_preference("general.useragent.override", user_agent)
browser = webdriver.Firefox(executable_path=FireFoxDreiverPath, firefox_profile=FireFoxProfile)
browser.implicitly_wait(7)

#l'url du site sur lequel nous allons scrapper les données
url = "https://fr.tradingview.com/markets/cryptocurrencies/prices-all/"
browser.get(url)

# création du fichier excel dans lequel on va enregistrer les tables
xlwriter = pd.ExcelWriter('TradingView Crypto Prices.xlsx')

#recupération des élément de l'ongle prix
categories = browser.find_elements("xpath",'//*[starts-with(@id, "") and contains(@class, "square-tab-button-Tm9B6mdh")]')

liste = []
for category in categories:
    liste.append(category.text)

del liste[-1]

for element in liste:
    try:
        #ici le script parcours chaque élement et clique dessus
        browser.find_element("xpath", f'//*[text()="{element}"]').click()
        time.sleep(2)
    except ElementNotInteractableException:
        pass

    while True:
        try:
            #le script click sur le bouton charger plus pour afficher plus de crypto-monnaie
            browser.find_element(By.XPATH , "//button[contains(text(),'Charger plus')]").click()
            time.sleep(1)
        except NoSuchElementException: 
            break     
    #le tableau est lu et enregistré dans le fichier 
    df = pd.read_html(browser.page_source)[1]
    df.to_excel(xlwriter, sheet_name=element, index=False)

xlwriter.save()

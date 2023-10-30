from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
import time

import csv

from datetime import datetime, timedelta

# Obtener la fecha actual
fecha_actual = datetime.now()

Tmin_Page = "https://www.meteorologia.gov.py/temperatura-minima/"

archivo = 'data_temperatura.csv'

if __name__ == "__main__":
       
    driver = webdriver.Edge()
    
    fechas = []
    
    for i in range(365):
        fecha = fecha_actual - timedelta(days=i)
        fecha_str = fecha.strftime("%d%m%Y")  # Formato de fecha: DDMMAAAA
        fechas.append(fecha_str)

    
    driver.get(Tmin_Page)
    
    with open(archivo, 'r') as archivo_lectura:
        with open('data_temperatura_new.csv','w',newline='') as archivo_escritura:
            reader = csv.reader(archivo_lectura)
            writer = csv.writer(archivo_escritura)
        
            for fecha in fechas:
                
                estaciones = []
                localidades = []
                tmin = []
                
                fila = []
                
                wait = WebDriverWait(driver,10)
                wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='date' and @class='form-control' and @id='fecha' and @name='fecha']")))

                fecha_input = driver.find_element(By.XPATH, "//input[@type='date' and @class='form-control' and @id='fecha' and @name='fecha']")
                fecha_input.send_keys(fecha)
                time.sleep(1)

                pyautogui.press('tab')
                pyautogui.press('enter')

                wait = WebDriverWait(driver,6)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.text-left.col-md-6")))

                etiquetas_tr = driver.find_elements(By.CSS_SELECTOR, "tr.odd, tr.even")

                for etiqueta_tr in etiquetas_tr:
                    etiqueta_td = etiqueta_tr.find_element(By.CSS_SELECTOR, "td.text-left.col-md-6")
                    estaciones.append(etiqueta_td.text.split('\n')[0])

                    etiqueta_td = etiqueta_tr.find_element(By.CSS_SELECTOR, "td.text-right.col-md-3")
                    tmin.append(etiqueta_td.text[:4])
                    
                fila = next(reader)
                fila.append(tmin[estaciones.index('CITEC - FIUNA Centro de Innovación Tecnológica')])

                writer.writerow(fila)
                
                print(f"La temperatura minima en la fecha {fecha} es {tmin[estaciones.index('CITEC - FIUNA Centro de Innovación Tecnológica')]} ")
                

        
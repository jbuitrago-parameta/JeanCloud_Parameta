##Validacion de facturas COPA

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import credenciales
import unittest
import HtmlTestRunner
import datetime

def funcion_uno():
    ###Inicio de sesion
    driver.get('https://copaair-test.coupahost.com/sessions/support_login')
    wait = WebDriverWait(driver, 10)
    nombre_usuario = driver.find_element_by_name("user[login]")
    nombre_usuario.clear()
    nombre_usuario.send_keys(credenciales.user)
    contrasena = driver.find_element_by_name("user[password]")
    contrasena.clear()
    contrasena.send_keys(credenciales.password)
    driver.find_element_by_class_name("button").click()
    
    #Buscar las facturas correspondientes
    
    try:
        driver.find_element_by_link_text('Facturas').click()
    except:
        driver.find_element_by_link_text('Invoices').click()
    try:
        driver.find_element_by_link_text('Líneas de facturas').click()
    except:
        driver.find_element_by_link_text('Invoice Lines').click()
    time.sleep(1)
    vista = driver.find_element_by_id('invoice_line_filter')
    vista.send_keys('UAT Creaci')
    time.sleep(2)
    # Aca comenzaría el ciclo
    cuadro = driver.find_element_by_id('sf_invoice_line')
    estan_ix = 0
    for ix_output in range(0,len(insumo_UAT)):
        item = str(insumo_UAT.loc[ix_output,'Invoice #'])
        try:
            cuadro.clear()
        except:
            time.sleep(2)
            cuadro = driver.find_element_by_id('sf_invoice_line')
            cuadro.clear()
        cuadro.send_keys(item)
        cuadro.send_keys(Keys.ENTER)
        time.sleep(2)
        prueba = 1
        encontrar = False
        tbody = driver.find_element_by_id('invoice_line_tbody')
        first_row = tbody.find_element_by_tag_name('tr')
        tds = first_row.find_elements_by_tag_name('td')
        while True and prueba< 10:
            if tds[0].text == 'No se encontraron coincidencias para tu búsqueda.':
                prueba = prueba + 1
            elif tds[0].text == 'No se encontraron coincidencias para tu búsqueda.':
                prueba = prueba + 1
            else:
                if item in tds[1].text:
                    estan.loc[estan_ix,'Invoice'] = item
                    estan_ix=estan_ix+1
                    screenshot_1 = False
                    try:
                        tabla_facturas.loc[ix_output,'Supplier'] = tds[0].text
                        tabla_facturas.loc[ix_output,'Invoice #'] =tds[1].text
                        tabla_facturas.loc[ix_output,'Invoice Date'] =tds[2].text
                        tabla_facturas.loc[ix_output,'Currency'] =tds[3].text
                        tabla_facturas.loc[ix_output,'Date of Invoice Received'] =tds[4].text
                        tabla_facturas.loc[ix_output,'Key reference for SAP'] =tds[5].text
                        tabla_facturas.loc[ix_output,'From'] =tds[6].text
                        tabla_facturas.loc[ix_output,'To'] =tds[7].text
                        tabla_facturas.loc[ix_output,'Line #'] =tds[8].text
                        tabla_facturas.loc[ix_output,'Description'] =tds[9].text
                        tabla_facturas.loc[ix_output,'Price'] =tds[10].text
                        tabla_facturas.loc[ix_output,'Total tax (Header)'] =tds[11].text
                        tabla_facturas.loc[ix_output,'Contract'] =tds[12].text
                        for z in list(insumo_UAT.columns)[:-2]:
                            if tabla_facturas.loc[ix_output,z] != insumo_UAT.loc[ix_output,z]:
                                screenshot_1 = True
                        
                        if screenshot_1:
                            driver.save_screenshot('Screenshots/Invoice_' + tabla_facturas.loc[ix_output,'Invoice #'] +"_1_" + str(now).replace(" ","_").replace(':','-')[0:19] + ".png")
                            screenshot_1 = False
                    except:
                        time.sleep(3)
                        tabla_facturas.loc[ix_output,'Supplier'] = tds[0].text
                        tabla_facturas.loc[ix_output,'Invoice #'] =tds[1].text
                        tabla_facturas.loc[ix_output,'Invoice Date'] =tds[2].text
                        tabla_facturas.loc[ix_output,'Currency'] =tds[3].text
                        tabla_facturas.loc[ix_output,'Date of Invoice Received'] =tds[4].text
                        tabla_facturas.loc[ix_output,'Key reference for SAP'] =tds[5].text
                        tabla_facturas.loc[ix_output,'From'] =tds[6].text
                        tabla_facturas.loc[ix_output,'To'] =tds[7].text
                        tabla_facturas.loc[ix_output,'Line #'] =tds[8].text
                        tabla_facturas.loc[ix_output,'Description'] =tds[9].text
                        tabla_facturas.loc[ix_output,'Price'] =tds[10].text
                        tabla_facturas.loc[ix_output,'Total tax (Header)'] =tds[11].text
                        tabla_facturas.loc[ix_output,'Contract'] =tds[12].text
                        for z in list(insumo_UAT.columns)[:-2]:
                            if tabla_facturas.loc[ix_output,z] != insumo_UAT.loc[ix_output,z]:
                                screenshot_1 = True
                        
                        if screenshot_1:
                            driver.save_screenshot('Screenshots/Invoice_' + tabla_facturas.loc[ix_output,'Invoice #'] +"_1_" + str(now).replace(" ","_").replace(':','-')[0:19] + ".png")
                            screenshot_1 = False

                    url = tds[1].find_element_by_tag_name('a').get_attribute('href')
                    driver.get(url)
                    time.sleep(3)
                    attachments_list = driver.find_element_by_class_name('attachments-list')
                    attachments = attachments_list.find_elements_by_tag_name('div')
                    line = ""
                    for ata in attachments:
                        if ata.text != "":
                            line = line + ata.text + ";"
                    line = line[:-1]
                    tabla_facturas.loc[ix_output,'Attachments'] = line
                    tabla_facturas.loc[ix_output,'Total invoice'] = driver.find_element_by_id('totalWithTaxes').text
                    screenshot_2 = False
                    for z in ['Attachments','Total invoice']:
                            if tabla_facturas.loc[ix_output,z] != insumo_UAT.loc[ix_output,z]:
                                screenshot_2 = True
                        
                    if screenshot_2:
                        driver.save_screenshot('Screenshots/Invoice_' + tabla_facturas.loc[ix_output,'Invoice #'] +"_2_" + str(now).replace(" ","_").replace(':','-')[0:19] + ".png")
                        screenshot_2 = False

                    try:
                        driver.find_element_by_link_text('Líneas de facturas').click()
                    except:
                        driver.find_element_by_link_text('Invoice Lines').click()
                    encontrar = True
                    ix_output = ix_output + 1
                    break
                else:
                    time.sleep(1)
                    prueba = prueba + 1
        if not encontrar:
            pass
    tabla_facturas['Index'] = tabla_facturas['Invoice #']
    tabla_facturas.set_index('Index',inplace=True)
    driver.close()
    estan.to_excel('Facturas subidas.xlsx', index = None, header = True, encoding="utf-8")

class TestSequense(unittest.TestCase):
    pass


def test_generator(a):
    def test(self):
        for x in list(insumo_UAT.columns):
            nombre = str(x)
            with self.subTest(Field = nombre):
                self.assertEqual(str(insumo_UAT.loc[a,x]),str(tabla_facturas.loc[str(insumo_UAT.loc[a,'Invoice #']),x]))
    return test

if __name__ == "__main__":
    os.chdir('G:\Mi unidad\Data\Copa\Validacion facturas')
    now = datetime.datetime.now()

    driver = webdriver.Chrome("C:\Python\Python37\chromedriver")
    tabla_facturas = pd.DataFrame(columns=['Supplier'], index = [0])
    estan = pd.DataFrame(columns=['Invoice'], index = [0])
    comparacion = pd.DataFrame(columns=['Supplier'], index = [0])
    with open("Columnas Copa.txt") as reader:
        for line in reader:
            a =  str(line).replace('\n','')
            tabla_facturas[a] = ""
            comparacion[a] = ""

    insumo_UAT = pd.read_excel('Insumo UAT - copia.xlsx', header = 0)
    testRunner_1=HtmlTestRunner.HTMLTestRunner(output="html_report_dir")
    funcion_uno()
    print(tabla_facturas)
    a,b = insumo_UAT.shape
    for x in range(a):
        test_name = 'test_Invoice # ' + str(insumo_UAT.loc[x,'Invoice #'])
        test_to_run = test_generator(x)
        setattr(TestSequense, test_name, test_to_run)
    unittest.main(testRunner=testRunner_1)


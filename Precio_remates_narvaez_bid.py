from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime as dt
import pandas as pd
import pyodbc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#Cargo la web y el navegador que voy a simular
url ='https://www.narvaezbid.com.ar/categorias/autos-y-motos?searchType=opened&filter=product.subCategory.category.description:autos&pageNumber=1&pageSize=60&orderBy=endDate:asc;price:desc'
driver=webdriver.Chrome()


#Creo control por si falla el primer intento de scrapeo
control = 0


while control == 0 :
    driver.maximize_window()
    driver.get(url)

#Scrapeamos

    desc=[]

    try:
        box = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/a/div/div[1]/div[2]/div[1]/p'))
            )

        # Iterar sobre los elementos encontrados
        for a in box:
            try:
                desc.append(a.text)
                print(a.text)
            except Exception as e:
                print("No se pudo obtener el texto del elemento:", e)

    except Exception as e:
        print("Ocurrió un error:", e)

    fecha=[]
    try:
        box2 = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/a/div/div[1]/div[1]/div[1]/div/span'))
            )

        # Iterar sobre los elementos encontrados
        for a in box2:
            try:
                #prec.append(a.text)
                fecha.append(a.text)

            except Exception as e:
                print("No se pudo obtener el texto del elemento:", e)

    except Exception as e:
        print("Ocurrió un error:", e)

    prec=[]
    #fecha=[]
    try:
        box2 = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div[1]/div/p'))
            )

        # Iterar sobre los elementos encontrados
        for a in box2:
            try:
                prec.append(a.text)
                #fecha.append(dt.datetime.now())

            except Exception as e:
                print("No se pudo obtener el texto del elemento:", e)


    except Exception as e:
        print("Ocurrió un error:", e)




    finally:
        # Cerrar el navegador al finalizar
        driver.quit()
        #print(desc)
    
    if desc[:1] == []:
        
        control = 0
    else:
        control = 1



#Corregimos algunos errores frecuentes en la descarga 
#para dejar los datos listos para la insercion a sql
# (Hay algunos prints en el camino para facilitar la busqueda de errores cuando hacen falta correcciones)

for i, elemento in enumerate(desc):
    if elemento.startswith('Ptas'):
        desc[i] = elemento.replace('.', '', 1)
    elif elemento.startswith('Prov'):
        desc[i] = elemento.replace('.', '', 1)

desc = [cadena.replace('Ptas.', 'Ptas') for cadena in desc]
desc = [cadena.replace('Prov.', 'Provincia') for cadena in desc]
desc = [cadena.replace('Pcia.', 'Provincia') for cadena in desc]
desc = [cadena.replace('1.', '1,') for cadena in desc]
desc = [cadena.replace('2.', '2,') for cadena in desc]
desc = [cadena.replace('Cab.', 'Cab') for cadena in desc]
desc = [cadena.replace('Trans.', 'Trans') for cadena in desc]
desc = [cadena.replace('Provincia De Santa Fe.', 'Provincia De Santa Fe') for cadena in desc]
desc = [cadena.replace('Yacimiento Aguada Pichana,', 'Yacimiento Aguada Pichana') for cadena in desc]
desc = [cadena.replace('Provincia De Buenos Aires.', 'Provincia De Buenos Aires') for cadena in desc]
desc = [cadena.replace('Provincia De Neuquén.', 'Provincia De Neuquén') for cadena in desc]
desc = [cadena.replace('C/Eq.', 'C/Eq') for cadena in desc]
desc = [cadena.replace('p .', 'p ') for cadena in desc]
desc = [cadena.replace('..', '.') for cadena in desc]
desc = [cadena.replace('Auth.', 'Auth') for cadena in desc]
desc = [cadena.replace('La Providencia,', 'La Providencia') for cadena in desc]
print(desc)




desc = [cadena.replace(',', '.') for cadena in desc]
datos_divididos = [item.split('.') for item in desc]



print(datos_divididos)
#mas pruebas para comprobar la estructura de los datos
for a in datos_divididos:
    print (len(a))

#creamos el dataframe que vamos a insertar en sql
df2 = pd.DataFrame(datos_divididos, columns=['Desc1', 'Desc2', 'Año', 'Dom','Ubicacion', 'Provincia'])
coches = list(zip(fecha, prec))

coches2 = pd.DataFrame(coches, columns=['Fecha', 'Precio'])
datos = pd.concat([coches2,df2], axis=1)



datos = datos.fillna('null')

print(datos)



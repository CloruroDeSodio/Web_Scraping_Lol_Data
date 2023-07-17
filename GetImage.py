from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('prueba.db')
cursor = conn.cursor()

# Consulta para obtener los nombres de la tabla "wiki"
cursor.execute("SELECT personaje FROM wiki")
nombres = cursor.fetchall()

# Configuración del servicio de ChromeDriver
service = Service('/home/aguacate/Downloads/googledriver/chromedriver')

# Configuración de las opciones de Chrome
options = Options()
options.add_argument('--headless')  # Ejecución en modo headless (sin abrir el navegador físicamente)

# Inicialización del controlador de Selenium
driver = webdriver.Chrome(service=service, options=options)

# Recorremos los nombres y obtenemos las URLs
for nombre in nombres:
    nombre = nombre[0]  # El nombre está en la primera columna
    url = f"https://universe.leagueoflegends.com/es_MX/story/champion/{nombre}"

    # Navegamos hacia la URL
    driver.get(url)

    # Simulamos desplazarnos hacia abajo para cargar la página completamente
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Esperamos a que la página se cargue completamente
    driver.implicitly_wait(5)  # Puedes ajustar este tiempo si es necesario

    # Buscamos los elementos <div> con la clase "image_3oOd championImage_29ws"
    div_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "image_3oOd") and contains(@class, "championImage_29ws")]')

    if div_elements:
        # Obtenemos el valor del atributo "data-am-url" del primer elemento
        data_am_url = div_elements[0].get_attribute('data-am-url')

        # Actualizamos la columna "imagen" en la base de datos
        cursor.execute("UPDATE wiki SET imagen = ? WHERE personaje = ?", (data_am_url, nombre))

# Guardamos los cambios en la base de datos
conn.commit()

# Cerramos el controlador de Selenium y la conexión a la base de datos
driver.quit()
conn.close()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import re

# Conectar a la base de datos
conn = sqlite3.connect('nombres.db')
cursor = conn.cursor()

# Configurar Selenium WebDriver con Chrome
options = Options()
options.add_argument("--headless")
service = Service('path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

a = 1
while a <= 163:
    query = 'SELECT nombre FROM campeones WHERE id = ?'
    cursor.execute(query, (a,))
    for row in cursor:
        row = ''.join(row)

    # Cargar la página web
    driver.get('https://universe.leagueoflegends.com/es_MX/story/champion/' + row)

    # Esperar a que se cargue el contenido inicial
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p')))
    texto_completo = ''

    # Desplazarse hacia abajo en la página para cargar más contenido
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)

    # Esperar a que se cargue el contenido adicional
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))

    # Extraer la información deseada
    elementos = driver.find_elements(By.CSS_SELECTOR, 'p')
    for elemento in elementos:
        texto = elemento.text
        if texto:
            texto_completo += texto + '<br>'

    # Eliminar etiquetas de párrafo adicionales
    texto_completo = re.sub('<br><br>', '<br>', texto_completo)

    # Insertar datos en la base de datos
    conn2 = sqlite3.connect('prueba.db')
    cursor2 = conn2.cursor()
    query2 = 'INSERT INTO wiki(personaje, informacion) VALUES (?, ?)'
    cursor2.execute(query2, (row, texto_completo))
    conn2.commit()
    cursor2.close()
    conn2.close()

    a += 1
# Cerrar el navegador
driver.quit()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

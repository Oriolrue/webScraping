from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pymysql


options = Options()
options.headless = False  # Set to True for headless mode
driver = webdriver.Chrome(options=options)



# Abrir una página web
driver.get("https://warframe.fandom.com/wiki/The_Murmur")

time.sleep(3)

cookies_button = driver.find_element(By.CLASS_NAME, '_2O--J403t2VqCuF8XJAZLK')
cookies_button.click()

time.sleep(3)

enemies = driver.find_elements(By.CLASS_NAME, 'wds-tabs__tab')

connection = pymysql.connect(
    host="localhost",
    user="usuario",
    password="password",
    database="enemieframe"
)

for names in enemies:
    name = names.find_element(By.TAG_NAME, 'a').text
    with connection.cursor() as cursor:
        sql = "INSERT INTO murmur (name) VALUES (%s)"
        cursor.execute(sql, (name,))
    connection.commit()

print("Datos insertados correctamente")

# Cerrar el navegador
driver.quit()
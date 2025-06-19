import csv # Importa a biblioteca CSV para ler e escrever arquivos CSV
import re # Importa a biblioteca 're' para usar expressões regulares (regex)

from selenium import webdriver # Importa o Selenium para automação do navegador
from selenium.webdriver.chrome.service import Service # Importa a classe Service para configurar o driver do Chrome
from selenium.webdriver.common.by import By # Importa o tipo de seletor de elementos HTML
from selenium.webdriver.support.ui import WebDriverWait # Importa o recurso de espera explícita
from selenium.webdriver.support import expected_conditions as EC # Importa as condições esperadas (como "elemento estar presente")
from webdriver_manager.chrome import ChromeDriverManager # Importa o gerenciador automático do driver do Chrome

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Inicia o navegador Chrome com o driver gerenciado automaticamente
wait = WebDriverWait(driver, 15) # Define um tempo máximo de espera de 15 segundos para os elementos carregarem

try:
    driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")# Abre a página da Mega-Sena no site da Caixa
    span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ng-binding"))) # Espera até que o elemento <span> com a classe 'ng-binding' esteja visível
    match = re.search(r"Concurso\s+(\d+)\s+\(([\d/]+)\)", span.text) # Usa expressão regular para extrair o número do concurso e a data a partir do texto do span
    concurso_num = match.group(1) # Armazena o número do concurso
    concurso_data = match.group(2) # Armazena a data do concurso
    ul = wait.until(EC.presence_of_element_located((By.ID, "ulDezenas"))) # Espera até que o elemento <ul> com ID 'ulDezenas' esteja presente na página
    dezenas = [li.text for li in ul.find_elements(By.TAG_NAME, "li")] # Extrai os textos de cada <li> dentro do <ul>, que são as dezenas sorteadas

    # Abre (ou cria) um arquivo CSV em modo append ('a') com codificação UTF-8
    with open("resultados_megasena.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow([concurso_num, concurso_data, ", ".join(dezenas)]) # Escreve uma nova linha com o número do concurso, a data e as dezenas separadas por vírgula

    
    print(f"Concurso {concurso_num} [{concurso_data}]: {dezenas}") # Imprime no terminal os resultados coletados para conferência

# Caso ocorra algum erro durante a execução, imprime uma mensagem de erro
except Exception as e:
    print("Erro ao extrair o último concurso:", e)

# Fecha o navegador, independentemente de sucesso ou erro
finally:
    driver.quit()
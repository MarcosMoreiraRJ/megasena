# Importa bibliotecas necessárias para manipulação de arquivos, tempo, expressões regulares e tratamento de erros
import csv  # Para manipular arquivos CSV
import time  # Para usar pausas entre requisições
import re  # Para trabalhar com expressões regulares (extração de dados)
import traceback  # Para imprimir rastreamento detalhado de erros

# Importa bibliotecas do Selenium para automação de navegador
from selenium import webdriver  # Controla o navegador
from selenium.webdriver.chrome.service import Service # Garante inicialização do ChromeDriver
from selenium.webdriver.common.by import By  # Para selecionar elementos no HTML
from selenium.webdriver.common.keys import Keys  # Para simular pressionar teclas
from selenium.webdriver.support.ui import WebDriverWait # Espera por elementos de forma explícita
from selenium.webdriver.support import expected_conditions as EC # Condições para esperar elementos
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException # Tratamento de erros do Selenium
from webdriver_manager.chrome import ChromeDriverManager # Baixa e gerencia o ChromeDriver automaticamente

# Define o nome do arquivo CSV onde os resultados serão salvos
csv_filename = "resultados_megasena.csv"

# Inicializa o navegador Chrome automaticamente com o WebDriver gerenciado
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define o tempo máximo de espera explícita para localizar elementos na página (15 segundos)
wait = WebDriverWait(driver, 15)

# Cria (ou sobrescreve) o arquivo CSV com o cabeçalho padrão
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Concurso", "Data", "Dezenas"])  # Cabeçalho das colunas

try:
    # Abre a página da Mega-Sena no site da Caixa
    driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")

    # Espera o carregamento do elemento com o número do concurso mais recente
    span = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.ng-binding")))

    # Usa expressão regular para extrair o número do concurso mais recente da string do elemento
    match = re.search(r"Concurso\s+(\d+)", span.text)
    # Converte para inteiro
    concurso_atual = int(match.group(1)) if match else 0

    # Inicia um loop para buscar todos os concursos do 1 até o mais recente
    for i in range(1, concurso_atual + 1):
        try:
            input_busca = wait.until(EC.presence_of_element_located((By.ID, "buscaConcurso"))) # Aguarda o campo de busca de concurso estar presente na página
            input_busca.clear()  # Limpa o campo de busca
            input_busca.send_keys(str(i))  # Digita o número do concurso desejado
            input_busca.send_keys(Keys.ENTER)  # Pressiona ENTER

            # Aguarda a página atualizar e exibir o número do concurso correto
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.ng-binding"), f"Concurso {i}"))
            
            # Aguarda o carregamento da lista com as dezenas sorteadas
            ul = wait.until(EC.presence_of_element_located((By.ID, "ulDezenas")))
            
            # Coleta as dezenas do sorteio em uma lista de strings
            numeros = [li.text for li in ul.find_elements(By.TAG_NAME, "li")]

            # Novamente busca o span com o número e data do concurso atual
            span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ng-binding")))   
            m = re.search(r"Concurso\s+(\d+)\s+\(([\d/]+)\)", span.text)
            concurso_num = m.group(1)  # Número do concurso
            concurso_data = m.group(2)  # Data do sorteio

            # Abre o arquivo CSV em modo append ("a") para adicionar a nova linha com os dados do concurso
            with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([concurso_num, concurso_data, ", ".join(numeros)])

            # Mostra no terminal o resultado que foi capturado
            print(f"Concurso {concurso_num} [{concurso_data}]: {numeros}")

        # Trata possíveis erros que possam ocorrer em cada iteração
        except (TimeoutException, NoSuchElementException, WebDriverException) as sub_e:
            print(f"Erro ao buscar concurso {i}: {sub_e}")
            traceback.print_exc()
            continue  # Pula para o próximo concurso

        # Aguarda 1 segundos antes de passar para o próximo concurso (evita sobrecarga no site)
        time.sleep(1)

# Caso ocorra algum erro inesperado fora do loop
except Exception as e:
    print("Erro durante o processo principal:", e)
    traceback.print_exc()

# Encerra o navegador ao final do processo (com ou sem erro)
finally:
    driver.quit()
    print("\nProcesso encerrado.")

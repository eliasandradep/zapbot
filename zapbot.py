from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# Caminho para o perfil do Chrome onde a sessão será salva
chrome_profile_path = os.path.expanduser("~") + "/whatsapp_session"

# Opções para iniciar o Chrome com o perfil salvo
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

# Inicializa o WebDriver com o perfil do Chrome
navegador = webdriver.Chrome(options=chrome_options)

# Abre o WhatsApp Web
navegador.get("https://web.whatsapp.com/")

# Aguarda o elemento de QRCode ser carregado
while len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')) > 0:
    print("Aguardando QR Code ser escaneado...")
    time.sleep(5)

# Aguarda o painel de mensagens do WhatsApp carregar
while len(navegador.find_elements(By.ID, 'side')) < 1:
    print("Aguardando o painel de mensagens carregar...")
    time.sleep(5)

print("WhatsApp Web carregado com sucesso!")

def send_message(contact_name, message):
    search_box = navegador.find_element(By.XPATH, '//*[@title="Buscar ou começar uma nova conversa"]')
    search_box.click()
    time.sleep(1)
    search_box.send_keys(contact_name)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    
    message_box = navegador.find_element(By.XPATH, '//*[@data-tab="1"]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)
    time.sleep(1)

def process_message(message):
    if 'bom dia' in message.lower():
        send_message(contact_name, "Bom dia! Seja muito bem-vinda ao Renata Rosa Beauty Concept! Para um atendimento personalizado, informe uma das opções: 1-Agendamento, 2-Dúvidas, 3-Reclamações, 4-Serviços, 5-Valores, 6-Falar com Atendente.")
    elif 'boa tarde' in message.lower():
        send_message(contact_name, "Boa tarde! Seja muito bem-vinda ao Renata Rosa Beauty Concept! Para um atendimento personalizado, informe uma das opções: 1-Agendamento, 2-Dúvidas, 3-Reclamações, 4-Serviços, 5-Valores, 6-Falar com Atendente.")
    elif 'boa noite' in message.lower():
        send_message(contact_name, "Boa noite! Seja muito bem-vinda ao Renata Rosa Beauty Concept! Para um atendimento personalizado, informe uma das opções: 1-Agendamento, 2-Dúvidas, 3-Reclamações, 4-Serviços, 5-Valores, 6-Falar com Atendente.")
    elif '1' in message:
        send_message(contact_name, "É sua primeira visita ao espaço? (Sim/Não)")
        # Esperar resposta do cliente
        time.sleep(10)  # Ajuste o tempo conforme necessário
        response = get_latest_message()
        if 'sim' in response.lower():
            send_message(contact_name, "Por favor, informe seu nome completo, data de nascimento e WhatsApp para cadastro.")
            # Receber dados do cliente e solicitar opções de agendamento
            time.sleep(10)
            send_message(contact_name, "Agora, informe 3 opções de dias e horários para seu agendamento.")
        else:
            send_message(contact_name, "Por favor, informe 3 opções de dias e horários para seu agendamento.")
        # Agradecimento e informações sobre o agendamento
        send_message(contact_name, "Obrigado pelas informações! Aguarde que um atendente fará o cadastramento e confirmará seu agendamento em breve.")
    elif '2' in message:
        send_message(contact_name, "Por favor, descreva sua dúvida detalhadamente e nossa equipe retornará assim que possível.")
    elif '3' in message:
        send_message(contact_name, "Obrigado pelo contato. Por favor, descreva sua reclamação e, se precisar de mais alguma coisa, informe pelo menu de atendimento inicial.")
        # Esperar resposta do cliente
        time.sleep(10)
        response = get_latest_message()
        if 'sim' in response.lower():
            send_message(contact_name, "Informe pelo menu de atendimento inicial sobre o que deseja.")
        else:
            send_message(contact_name, "Obrigado pelo contato. Tenha um bom dia!")
    elif '4' in message:
        services = pd.read_csv('servicos.csv')
        services_cabelo = services[services['Categoria'] == 'Cabelo']
        services_list = '\n'.join(services_cabelo['Nome'].tolist())
        send_message(contact_name, f"Aqui estão nossos serviços:\n{services_list}\nGostaria de agendar um dos serviços?")
        # Esperar resposta do cliente
        time.sleep(10)
        response = get_latest_message()
        if 'sim' in response.lower():
            send_message(contact_name, "É sua primeira visita ao espaço? (Sim/Não)")
            # Receber dados do cliente e solicitar opções de agendamento
            time.sleep(10)
            response = get_latest_message()
            if 'sim' in response.lower():
                send_message(contact_name, "Por favor, informe seu nome completo, data de nascimento e WhatsApp para cadastro.")
                time.sleep(10)
                send_message(contact_name, "Agora, informe 3 opções de dias e horários para seu agendamento.")
            else:
                send_message(contact_name, "Por favor, informe 3 opções de dias e horários para seu agendamento.")
            send_message(contact_name, "Obrigado pelas informações! Aguarde que um atendente fará o cadastramento e confirmará seu agendamento em breve.")
    elif '5' in message:
        prices = pd.read_csv('valores.csv')
        price_list = prices[['Nome', 'Preço']].to_string(index=False)
        send_message(contact_name, f"Aqui estão nossos valores:\n{price_list}\nObrigado pelo contato!")
    elif '6' in message:
        send_message(contact_name, "A conversa será direcionada a um atendente disponível. Por favor, aguarde um momento.")

def get_latest_message():
    # Função para obter a última mensagem recebida (implemente conforme necessário)
    pass

while True:
    # Aqui você pode implementar a lógica para verificar mensagens recebidas
    contact_name = 'Nome do Contato'  # Substitua pelo nome do contato ou obtenha dinamicamente
    message = 'Mensagem do Contato'  # Substitua pela mensagem recebida ou obtenha dinamicamente
    process_message(message)
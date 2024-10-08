from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
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
    sleep(5)

# Aguarda o painel de mensagens do WhatsApp carregar
while len(navegador.find_elements(By.ID, 'side')) < 1:
    print("Aguardando o painel de mensagens carregar...")
    sleep(5)

print("WhatsApp Web carregado com sucesso!")

# Loop para monitorar novas mensagens
while True:
    sleep(3)  # Ajusta o tempo de espera entre as verificações

    try:
        # Localiza os contatos que têm novas notificações
        notificacoes = navegador.find_elements(By.CLASS_NAME, '_ahlk')
        
        if notificacoes:
            print("Notificação detectada.")
            # Clica na notificação (vai abrir a conversa)
            notificacoes[0].click()
            sleep(2)  # Tempo para a conversa carregar

            # Identifica a última mensagem recebida na conversa aberta
            try:
                # Localiza as mensagens na conversa
                mensagens = navegador.find_elements(By.CLASS_NAME, '_akbu')
                
                if mensagens:
                    ultima_mensagem_texto = mensagens[-1].text.lower().strip()  # Ignora maiúsculas/minúsculas e remove espaços em branco
                    print(f"Conteúdo bruto da mensagem: '{mensagens[-1].text}'")  # Conteúdo original da mensagem
                    print(f"Última mensagem processada: '{ultima_mensagem_texto}'")  # Conteúdo após processar

                    # Define a resposta de acordo com o padrão identificado
                    if "bom dia" in ultima_mensagem_texto:
                        resposta = "Bom dia! Seja muito bem-vindo(a) ao Renata Rosa Beauty Concept! Como posso ajudá-lo(a)?"
                    elif "boa tarde" in ultima_mensagem_texto:
                        resposta = "Boa tarde! Seja muito bem-vindo(a) ao Renata Rosa Beauty Concept! Como posso ajudá-lo(a)?"
                    elif "boa noite" in ultima_mensagem_texto:
                        resposta = "Boa noite! Seja muito bem-vindo(a) ao Renata Rosa Beauty Concept! Como posso ajudá-lo(a)?"
                    elif any(palavra in ultima_mensagem_texto for palavra in ["agendar", "agendamento"]):
                        resposta = "É a sua primeira visita ao nosso Espaço?"
                    elif "sim" in ultima_mensagem_texto:
                        resposta = "Favor nos enviar 3 opções de dias e horários, juntamente com seu nome completo, número de telefone que seja WhatsApp e data de nascimento para a efetivação do seu agendamento."
                    elif "não" in ultima_mensagem_texto:
                        resposta = "Favor nos enviar 3 opções de dias e horários em que deseja efetuar o seu agendamento."
                    else:
                        resposta = "Olá! Seja muito Bem-vindo(a) ao Espaço Renata Rosa Beauty Concept. Como posso ajudá-lo(a)?"

                    # Espera explicitamente pelo campo de entrada de texto estar disponível
                    input_box = WebDriverWait(navegador, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
                    )
                    # Foco no campo de entrada para garantir que ele está ativo
                    input_box.click()
                    sleep(1)  # Aguarda um pouco para garantir que o campo está pronto
                    
                    # Envia a resposta
                    input_box.send_keys(resposta)
                    input_box.send_keys(Keys.RETURN)
                    print(f"Mensagem enviada: {resposta}")
                else:
                    print("Nenhuma mensagem encontrada.")
            except Exception as e:
                print(f"Erro ao localizar ou processar mensagens: {e}")
        
        else:
            print("Nenhuma nova mensagem.")
    
    except Exception as e:
        print(f"Erro: {e}")

# Fechar o navegador após a execução (opcional)
# navegador.quit()
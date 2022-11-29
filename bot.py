# importações de bibliotecas para o funcionamento do código

from selenium import webdriver # selenium encontra elementos da página HTML 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time # o time cria um tempo de espera para que o bot entregue as mensagens
from webdriver_manager.chrome import ChromeDriverManager # faz a conexão com o Google Chrome
from tkinter import * # importa o tkinter para ter um interface grafica 
from tkinter import filedialog # é a biblioteca que vai importar as imagens
from tkinter import messagebox

# variáveis utilizadas
contatos = []
mensagens = []
imagens = []

# essa função faz com que seja possivel adicionar imagens via tkinter 
def adicionarImagens():
    # askopenfilename é o método que vai abrir o explorador de arquivos
    imagem = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(
        ("Image files", [".jpg", ".png", ".jpeg"]), ("all files", ".")))
    # .append vai adicionar o item no ultimo lugar do array

    if imagem != "":
        imagens.append(imagem)
        print(imagens)

    print(imagens)

# essa função faz com que seja possivel adicionar os nomes dos contatos via tkinter 
def adicionarContatos():
    if contatosInput.get() != "":
        # .append vai adicionar o item no ultimo lugar do array
        contatos.append(contatosInput.get())

        # .delete (0 = é o inicio, end até o final)
        contatosInput.delete(0, 'end')
    else:
        messagebox.showerror(title="Erro", message="Digite algum contato.")

# essa função faz com que seja possivel adicionar qualquer mensagem via tkinter 
def adicionarMensagens():
    if mensagensInput.get("1.0", "end-1c") != "":
        # .get(1.0 inicio, end-1c até o final) isso é necessario pois o input é um text
        mensagens.append(mensagensInput.get("1.0", "end-1c"))
        mensagensInput.delete("1.0", "end-1c")
        print(mensagens)
    else:
        messagebox.showerror(title="Erro", message="Digite algo no campo de mensagem.")

# reseta os itens salvos
def resetar():
    contatos.clear()
    mensagens.clear()
    imagens.clear()

# a função envia os arquivos para o whatsapp
def enviar():
    if len(contatos) != 0:
        if len(mensagens) != 0 or len(imagens) != 0:
            # ele adiciona as funcionalidades do chrome na variável driver
            driver = webdriver.Chrome(ChromeDriverManager().install())
            # .get abre o whatsapp
            driver.get('https://web.whatsapp.com')

            # time.sleep faz com que o bot espere para mandar a mensagem
            time.sleep(30)

            # essa função faz com que o bot pesquise o nome do contato/grupo selecionado 
            def buscar_contato(contato):

                #.find_element procura um elemento especifico do HTML pelo nome da classe
                pesquisar_contato = driver.find_element(
                    By.XPATH, '//div[contains(@class, "copyable-text selectable-text")]')
                time.sleep(2)

                # .click faz o bot clicar no selecionado através do find_element
                pesquisar_contato.click()

                #.send_keys envia um comando do teclado no elemento que você selecionou
                pesquisar_contato.send_keys(contato)

                #Keys.ENTER envia a tecla enter
                pesquisar_contato.send_keys(Keys.ENTER)
                time.sleep(1)


            # essa função manda as mensagens que o usuario selecionou
            def mandar_mensagem(mensagens):

                # o loop serve para mandar as mensagens independentemente da quantidade de vezes que foi adicionada 
                for mensagem in mensagens:

                    # .split faz separar a string em um array a cada \n
                    mensagemFormat = mensagem.split("\n")
                    enviar_mensagem = driver.find_element(
                        By.XPATH, '//p[contains(@class, "selectable-text copyable-text")]')
                    enviar_mensagem.click()
                    # formata as mensagens para enviar elas com o enter que foi colocado pelo usuario
                    for msg in mensagemFormat:
                        enviar_mensagem.send_keys(msg)
                        enviar_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
                    enviar_mensagem.send_keys(Keys.ENTER)
                    time.sleep(1)

            # essa função enviará as imagens para o whatsapp
            def mandar_imagem(imagens):
                # o loop serve para mandar as imagens independentemente da quantidade de vezes que foi adicionada 
                for imagem in imagens:

                    # estamos utlizando o find_element para encontrar um elemento pelo seu seletor de css
                    driver.find_element(
                        By.CSS_SELECTOR, 'span[data-icon="clip"]').click()
                    attach = driver.find_element(By.CSS_SELECTOR, 'input[type=file]')
                    attach.send_keys(imagem)
                    time.sleep(1)
                    send = driver.find_element(
                        By.XPATH, '//div[contains(@class, "_165_h _2HL9j")]')
                    send.click()
                    time.sleep(1)

            # vai mandar as mensagens para todos os cotatos/grupos que foram inseridos pelo usuarios
            for contato in contatos:
                buscar_contato(contato)

                # uma condição que impede o envio de mensagens caso não tenha nada
                if len(mensagens) > 0:
                    mandar_mensagem(mensagens)
                if len(imagens) > 0:
                    mandar_imagem(imagens)
                time.sleep(1)

            resetar()
        else:
            messagebox.showerror(title="Erro", message="Adicione uma imagem ou mensagem.")
    else:
        messagebox.showerror(title="Erro", message="Digite um contato ou messagem.")

# inicializaçãoc do tkinter em uma variavel
bot = Tk()
#.title é o titulo da janela
bot.title("BOT ZAP ZAP")
# .geometry é o tamanho da tela
bot.geometry("500x380")


# Label vai criar um texto ao lado do input
# anchor são usadas para definir onde o texto é posicionado em relação a um ponto de referência.
# place é usado para definir a posição do elemento
Label(bot, text="BOT ZAP ZAP", anchor=W).place(x=10, y=10)

Label(bot, text="Digite os contatos ou grupos que queira enviar:",
      anchor=W).place(x=10, y=40)

# Entry cria um input
contatosInput = Entry(bot)

# width é a largura
contatosInput.place(x=10, y=70, width=130)

#Button cria um botão que ativa uma função que nesse contexto será adicionarContatos
Button(bot, text="Adicionar", command=adicionarContatos).place(
    x=150, y=65, width=100)

Label(bot, text="Digite as mensagem a serem enviadas:",
      anchor=W).place(x=10, y=100)
mensagensInput = Text(bot, height=10)
mensagensInput.place(x=10, y=130, width=480)

Button(bot, text="Adicionar", command=adicionarMensagens).place(
    x=10, y=300, width=100)

Button(bot, text="Adicionar imagem", command=adicionarImagens).place(
    x=10, y=340, width=120)

Button(bot, text="Enviar mensagem", command=enviar).place(
    x=370, y=340, width=120)


#O método mainloop é usado para "travar" a execução da janela atual usando um event loop do tkinter. Isso permite com que o tkinter possa disparar respostas a eventos na instância atual da janela que chamou o mainloop, como um keypress ou click e não permite a execução de códigos posteriores até que a janela seja fechada.
bot.mainloop()

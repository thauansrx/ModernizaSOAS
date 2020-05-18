"""

    SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
    FLUXO END-TO-END OPERACIONAL.
    ESSE ARQUIVO REFERE-SE À ETAPA DE ATUAÇÃO.

    # Arguments
            object                 - Required : User Interface do Login (UI)
        # Returns
            validador_atuacao       - Required : Validador de execução da Atuação (Boolean)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN) && Rayomi Reis (RAYOMIR)"""
__data_atualizacao__ = "14/05/2020"

import os
import subprocess
import sys
import time
import datetime
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from math import ceil
from queue import Queue

from PIL import ImageTk, Image
import pygubu

from Database_Executa_Query import Executa_Query
from Executa_Versao_Sobre import Orquestrador_Sobre_Versao
import main_menu
import JSON_Executa

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class Frame_Atuacao(object):

    """

        SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
        FLUXO END-TO-END OPERACIONAL.
        ESSE ARQUIVO REFERE-SE À ETAPA DE ATUAÇÃO.

        # Arguments
            object                 - Required : User Interface do Login. (UI)
        # Returns
            validador_login        - Required : Validador de execução da Atuação. (Boolean)

    """


    def __init__(self, queue_thread, funcional_usuario = None, **kw):

        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # INICIALIZANDO O OBJETO TKINTER
        builder.add_from_file(os.path.join(CURRENT_DIR, 'FRAME_ATUACAO.ui'))
        self.root = builder.get_object('Frame_Atuacao')
        self.root.title("MODERNIZA - SOAS")

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file('FRAME_ATUACAO.ui')

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            print("Não há o caminho de imagens")

        # 4 - CRIANDO AS JANELA PRINCIPAIS
        self.mainwindow = builder.get_object('Frame_Atuacao', self.root)
        self.informacoes_gerais = builder.get_object("Label_Informacoes_Gerais", self.root)
        self.campos = builder.get_object('Frame_Campos', self.root)
        self.meio = builder.get_object('Frame_meio', self.root)
        self.campos_adicionais = builder.get_object('Frame_Adicionais', self.root)
        self.sinaleiro = builder.get_object('Frame_Sinaleiro', self.root)
        self.lbl_clock = builder.get_object("Label_Relogio")
        self.relogio_sinal = builder.get_object("Frame_Relogio_Sinal")
        self.classic_theme = builder.get_object("Radiobutton_theme_classic", self.root)
        self.dark_theme = builder.get_object("Radiobutton_theme_dark", self.root)

        self.canvas = tk.Canvas(self.campos)

        # 5 - ASSOCIANDO MENU ÀS JANELAS PRINCIPAIS
        self.mainmenu = menu = self.builder.get_object('Frame_Menu', self.root)
        self.mainwindow.config(menu=self.mainmenu)

        # 6 - DEFININDO BANCO DE DADOS - PRODUÇÃO
        try:
            bd_path = os.getcwd() + "\DB_ModernizaSOAS" + "\\" + "DB_MODERNIZASOAS_PRODUCAO.db"
            self.bd_path = bd_path
            builder.add_resource_path(self.bd_path)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        # 7 - DEFININDO BANCO DE DADOS - LOGS
        try:
            bd_path_logs = os.getcwd() + "\DB_ModernizaSOAS" + "\\" + "DB_MODERNIZASOAS_LOGS.db"
            self.bd_path_logs = bd_path_logs
            builder.add_resource_path(self.bd_path_logs)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        # 8 - DEFININDO TIPOS DE QUERY
        self.tipo_query = ["SELECT", "INSERT", "DELETE", "UPDATE", "TRUNCATE"]

        # 9 - API DE ENVIO DE EMAILS
        # AQUI SERÁ ADICIONADO UMA API DE ENVIO DE EMAILS COM TEMPLATE
        try:
            api_envia_email_path = os.getcwd() + "\API" + "\\" + "Executa_Envia_Email.exe"
            self.api_envia_email = api_envia_email_path
            builder.add_resource_path(self.api_envia_email)
        except Exception as ex:
            print("Não há o caminho da API de Envio de Email")

        # 10 - DEFININDO O GERENCIADOR DE THREAD's
        self.queue = queue_thread

        # 11 - DEFININDO O VALOR DE MÁXIMO COMPONENTES NA TELA
        self.quantidade_maximo_componentes = 3

        # 12 - DEFININDO A LISTA DE BOTÕES DE DECISÃO
        self.lista_botoes_decisao = ["bt_aprovar", "bt_devolver", "bt_followup",
                                     "bt_duplicidade", "bt_buscar_emails"]

        # 13 - VARIÁVEIS GLOBAIS DO TEMA
        self.dark_theme = False
        self.fundo = "#f79c60"
        self.frente = "#ff7200"
        self.letras = "#ffffff"

        # 14 - VARIÁVEL GLOBAIS DE PAUSA
        self.pausa_op = False

        # VARIÁVEL SÓ PARA OS TESTES
        self.quantidade_produto = 0
        self.proxima_operacao = []

        # USUÁRIO LOGADO
        self.funcional_usuario = funcional_usuario

        builder.connect_callbacks(self)


    def registra_erro(self, funcional_usuario, local_erro, acao_erro):

        """

           FUNÇÃO QUE REALIZA O REGISTRO DE ERRO DE ALGUMA AÇÃO NO BANCO DE DADOS DE LOGS.

           # Arguments
               funcional_usuario           - Required : Funcional do usuário. (String)
               local_erro                  - Required : Local do programa onde ocorreu erro. (String)
               acao_erro                   - Required : Ação que gerou o erro. (String)

           # Returns
               validador_orquestrador      - Required : Validador de execução do registro de log. (Boolean)

       """

        try:
            # OBTENDO DATA E HORA ATUAL
            data_hora_atual = Frame_Atuacao.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path_logs

            # DEFININDO SSQL E PARÂMETROS
            ssql = "INSERT INTO TBL_LOGS_ERRO(FUNCIONAL, DT_HR_ERRO, LOCAL_ERRO, ACAO_ERRO) VALUES (?, ?, ?, ?)"
            params = (funcional_usuario, data_hora_atual, local_erro, acao_erro)

            # REALIZANDO A QUERY - INSERT
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[1])
            validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")
        except Exception as ex:
            print(ex)


    def registra_log_saida(self, funcional_usuario):

        """

           FUNÇÃO QUE REALIZA O REGISTRO DE SAÍDA DOS USUÁRIOS NO BANCO DE DADOS DE LOGS.

           # Arguments
               funcional_usuario           - Required : Funcional do usuário. (String)

           # Returns
               validador_orquestrador      - Required : Validador de execução do registro de log. (Boolean)

       """

        try:
            # OBTENDO DATA E HORA ATUAL
            data_hora_atual = Frame_Atuacao.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path_logs

            # DEFININDO SSQL E PARÂMETROS
            ssql = "UPDATE TBL_ACESSO SET DT_HR_SAIDA = ? " \
                                   "WHERE ID_ACESSO = (SELECT ID_ACESSO FROM (SELECT ID_ACESSO FROM TBL_ACESSO WHERE FUNCIONAL = ? " \
                                   "ORDER BY ID_ACESSO DESC LIMIT 1) as temp);"
            params = (data_hora_atual, funcional_usuario)

            # REALIZANDO A QUERY - UPDATE
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[3])

            validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.registra_log_saida", str(ex))


    def theme_colors(self):

        """

        PALETAS DARK:
            self.fundo = "#28334A"
            self.frente = "#101820"
            self.letras = "#FEE715"

        PALETAS DARK BLUE:
            self.fundo = "#140083"
            self.frente = "#28334A"
            self.letras = "#FEE715"

        PALETAS ITAU CLASSICO:
            self.fundo = "#f79c60"
            self.frente = "#ff7200"
            self.letras = "#ffffff"

        @return:

        """

        try:
            if self.dark_theme == True:
                self.fundo = "#140083"
                self.frente = "#28334A"
                self.letras = "#FEE715"
            else:
                self.fundo = "#f79c60"
                self.frente = "#ff7200"
                self.letras = "#ffffff"

            # DESTRUINDO OS CAMPOS DO SINALEIRO
            Frame_Atuacao.percorre_campos_por_tipo(self, self.sinaleiro, "Label", "nomes_labels_paletas")
            # REFATORANDO OS CAMPOS DO SINALEIRO
            etapas_processo = Frame_Atuacao.obtem_etapas_proxima_operacao(self, self.quantidade_produto)
            Frame_Atuacao.cria_label_sinaleiros(self, self.proxima_operacao[0], etapas_processo, self.frente)

            # DEFINE AS ENTRY QUE SERÃO MUDADOS
            objetos_entry = ["Label_Produto_Informacoes_Gerais", "Label_Agencia_Informacoes_Gerais", "Label_Conta_Informacoes_Gerais", "Label_PN_Informacoes_Gerais", "Label_CNPJ_Informacoes_Gerais"]
            for o in objetos_entry:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, foreground=self.letras, selectforeground=self.frente, readonlybackground=self.frente)

            # DEFINE LISTA DE BOTÕES QUE SERÃO MUDADOS
            objetos_botoes = ["bt_pausar_op", "bt_aprovar", "bt_devolver", "bt_followup", "bt_duplicidade", "bt_buscar_emails"]
            for o in objetos_botoes:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(activebackground=self.frente, activeforeground=self.frente, background=self.frente, foreground=self.frente, disabledforeground=self.frente)


            # DEFINE LISTA DE Labels QUE SERÃO MUDADOS
            objetos_label = ["Label_Produto_Informacoes_Gerais", "Label_Agencia_Informacoes_Gerais", "Label_Conta_Informacoes_Gerais", "Label_PN_Informacoes_Gerais",
                             "Label_CNPJ_Informacoes_Gerais", "Label_Usuario_Informacoes_Gerais", "Label_Calendar_Informacoes_Gerais", "Label_Relogio"]

            # Edita os Objetos
            for o in objetos_label:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, foreground=self.letras)

            # DEFINE LISTA DE OBJETOS DO TIPO RADIOBUTTON
            objetos_radiobutton = ["Radiobutton_theme_dark", "Radiobutton_theme_classic"]
            for o in objetos_radiobutton:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, foreground=self.letras, highlightbackground=self.fundo, activebackground=self.frente)

            # DEFINE LISTA DE OBJETOS DO TIPO LabelFRAME
            objetos_labelframe = ["Frame_Ta", "Frame_Sinaleiro", "Label_Informacoes_Gerais", 'Frame_Email']
            for o in objetos_labelframe:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, foreground=self.letras, highlightbackground=self.fundo)

            # DEFINE LISTA DE OBJETOS DO TIPO FRAME
            objetos_frame =["Frame_Central", "Frame_Adicionais", "Frame_Anotacoes", "Frame_Decisao"]
            for o in objetos_frame:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, highlightbackground=self.fundo)
            self.Frame_Relogio_Sinal = self.builder.get_object("Frame_Relogio_Sinal", self.root)
            self.Frame_Relogio_Sinal.configure(background=self.fundo, highlightbackground=self.fundo)

            # DEFINE LISTA DE OBJETOS DO TIPO CANVAS
            objetos_canvas = ["Canvas_Calendario_Informacoes_Gerais", "Canvas_Logo_Informacoes_Gerais"]
            for o in objetos_canvas:
                self.o = self.builder.get_object(str(o), self.root)
                self.o.configure(background=self.frente, highlightbackground=self.frente, )
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.theme_colors", str(ex))


    def radio_dark_theme(self):

        try:
            # HABILITA NOVAMENTE O BOTÃO DE Classic_theme
            Frame_Atuacao.define_estado_botao(self, "Radiobutton_theme_classic", "active")
            Frame_Atuacao.define_estado_botao(self, "Radiobutton_theme_dark", "disabled")
            # self.classic_theme.configure(value=None)

            # HABILITA O TEMA DARK
            self.dark_theme = True

            # DEFINE A NOVA COR DA JANELA
            Frame_Atuacao.theme_colors(self)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.radio_dark_theme", str(ex))


    def radio_classic_theme(self):

        try:
            # HABILITA NOVAMENTE O BOTÃO DE CLASSIC_THEME
            Frame_Atuacao.define_estado_botao(self, "Radiobutton_theme_dark", "active")
            Frame_Atuacao.define_estado_botao(self, "Radiobutton_theme_classic", "disable")
            # self.dark_theme.configure(value=None)

            # HABILITA O TEMA CLASSIC
            self.dark_theme = False

            # DEFINE A NOVA COR DA JANELA
            Frame_Atuacao.theme_colors(self)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.radio_classic_theme", str(ex))


    def centraliza_janela(self, tamanho_largura=None, tamanho_altura=None):

        """

            CENTRALIZA E DEFINE O TAMANHO DO FRAME PRINCIPAL SENDO RESPONSIVO EM RELAÇÃO AO TAMANHO DA TELA DO USUÁRIO.

            # Arguments

            # Returns

        """

        try:
            # FUNÇÃO DEFINIDA PARA CENTRALIZAR O FRAME

            janela_root = self.root

            janela_root.update_idletasks()

            # CASO A LARGURA E ALTURA SEJAM None, O SISTEMA RECONFIGURA COM BASE NAS DEFINIÇÕES DE LARGURA E ALTURA DO SISTEMA.

            # DEFININDO LARGURA
            if tamanho_largura == None:
                width = janela_root.winfo_width()
            else:
                width = tamanho_largura

            # DEFININDO ALTURA
            if tamanho_largura == None:
                height = janela_root.winfo_height()
            else:
                height = tamanho_altura

            x = (janela_root.winfo_screenwidth() // 2) - (width // 2)
            y = (janela_root.winfo_screenheight() // 2) - (height // 2)
            janela_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        except Exception as ex:
            print(ex)


    def resizable_window(self):

        self.var_size_height = True

        try:
            while self.var_size_height == True:
                self.current_sizeo_height = self.root.winfo_height()
                self.current_size_width = self.root.winfo_width()

                while self.root.winfo_height() == self.current_sizeo_height and self.root.winfo_width() == self.current_size_width:
                    time.sleep(1)

                if self.root.winfo_height() != self.current_sizeo_height:

                    # CONFIGURA ALTURA DO LABEL QUE CONTEM O RELOGIO E OS SINAIS
                    self.relogio_sinal.configure(height=self.root.winfo_height()-100)
                    self.sinaleiro.configure(height=self.root.winfo_height() - 157)

                    # CONFIGURA ALTURA ONDE OS CAMPOS BOTÕES DE DECISÕES E A CAIXA DE TEXTO ESTÃO LOCALIZADOS
                    self.campos_adicionais.configure(height=self.root.winfo_height()-100)

                    # CONFIGURA ALTURA DO LABEL CENTRAL ONDE A OPERAÇÃO ATUA
                    self.campos.configure(height=self.root.winfo_height()-100)

                if self.root.winfo_width() != self.current_size_width:

                    # CONFIGURA LARGURA DO CABEÇALHO
                    self.informacoes_gerais.configure(width=self.root.winfo_width())

                    # CONFIGURA A LARGURA DO LABEL CENTRAL ONDE A OPERAÇÃO ATUA
                    campos_width = self.root.winfo_width() - 391
                    self.campos.configure(width=campos_width)

                    # CONFIGURA A LARGURA DAS COLUNAS DO LABEL CENTRAL ONDE A OPERAÇÃO ATUA
                    self.campos.columnconfigure(0, minsize=(campos_width / 3))
                    self.campos.columnconfigure(1, minsize=(campos_width / 3))
                    self.campos.columnconfigure(2, minsize=(campos_width / 3))
        except Exception as ex:
            pass


    def orquestrador_reponsivo(self):

        try:
            t = Thread(target=Frame_Atuacao.resizable_window, daemon=False, args=(self,))
            t.start()
        except Exception as ex:
            pass


    def get_current_size_width(self):

        self.var_size_width = True

        while self.var_size_width == True:
            self.current_size_width = self.root.winfo_width()

            while self.root.winfo_width() == self.current_size_width:
                pass

            print(f"Valor novo: {self.root.winfo_width()}, valor antigo: {self.current_size_width}")


    def resizable(self, resizablelargura, resizablealtura):

        """

            DEFINE A POSSIBILIDADE DE REDIMENSIONAMENTO DA TELA.

            # Arguments
                resizablelargura        - Required : Redimensionamento horizontal. (Boolean)
                resizablealtura         - Required : Redimensionamento vertical. (Boolean)

            # Returns

        """

        try:
            # FUNÇÃO DEFINIDA PARA CONTROLAR O REDIMENSIONAMENTO
            self.root.resizable(resizablelargura, resizablealtura)
        except Exception as ex:
            print(ex)


    @staticmethod
    def define_backgrounds(janela, cor):

        """

            DEFINE UMA COR À JANELA INSTANCIADO A PARTIR DOS SELF.ROOT's (# 4 - CRIANDO AS JANELA PRINCIPAIS)

            # Arguments
                janela           - Required : Janela que receberá a alteração de bg. (String)
                cor              - Required : Cor aplicado ao bg. (String)

            # Returns

        """

        try:
            # DEFININDO UMA INSTÂNCIA DE ESTILO
            style = tk.ttk.Style()
            # DEFININDO A CONFIGURAÇÃO DE BG
            style.configure("TFrame", background=cor)
            # APLICANDO A CONFIGUAÇÃO DE BG
            janela.config(style='TFrame')
        except Exception as ex:
            print(ex)


    def call_definicoes_background(self):

        """

            CHAMA A FUNÇÃO QUE DEFINE UMA COR À JANELA INSTANCIADO A PARTIR DOS SELF.ROOT's
            (# 4 - CRIANDO AS JANELA PRINCIPAIS)

            # Arguments

            # Returns

        """

        try:
            Frame_Atuacao.define_backgrounds(self.mainwindow, "white")
        except Exception as ex:
            print(ex)
        try:
            Frame_Atuacao.define_backgrounds(self.informacoes_gerais, "white")
        except Exception as ex:
            print(ex)
        try:
            Frame_Atuacao.define_backgrounds(self.campos, "white")
        except Exception as ex:
            print(ex)
        try:
            Frame_Atuacao.define_backgrounds(self.campos_adicionais, "white")
        except Exception as ex:
            print(ex)


    def fecha_frame(self):

        """

            DEFINE A POSSIBILIDADE DE REDIMENSIONAMENTO DA TELA.

            # Arguments

            # Returns

        """

        try:
            self.root.quit()
        except Exception as ex:
            print(ex)


    def insere_img_canvas(self, objeto_para_imagem, imagem, altura, largura):

        """

            INSERE IMAGEM NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto_para_imagem        - Required : Objeto Canvas. (UI)
                imagem                    - Required : Imagem a ser inserida no Canvas. (.jpg | .png)

            # Returns
                validador_query           - Required : Validador de execução da função. (Boolean)

        """

        try:
            # FUNÇÃO DEFINIDA PARA INSERIR IMAGEM NO CANVAS

            objeto_para_imagem.image = ImageTk.PhotoImage(imagem)
            objeto_para_imagem.create_image(altura,
                                            largura,
                                            image=objeto_para_imagem.image,
                                            anchor="nw")

            return True

        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.insere_img_canvas", str(ex))
            return False


    def seleciona_img_canvas(self, objeto, imagem, altura_imagem, largura_imagem):

        """

            SELECIONA IMAGEM A SER INSERIDO NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto                    - Required : Objeto Canvas. (UI)
                imagem                    - Required : Imagem a ser inserida no Canvas. (String)

            # Returns
                validador_query           - Required : Validador de execução da função. (Boolean)

        """

        validador = False

        while validador is False:

            try:
                img = Image.open(self.img_path + "\\" + imagem)

                # INSERINDO A IMAGEM
                validador = Frame_Atuacao.insere_img_canvas(self, objeto, img, altura_imagem, largura_imagem)

                return validador
            except Exception as ex:
                Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.seleciona_img_canvas", str(ex))
                return False


    def carrega_img_canvas(self, objeto, imagem, altura_imagem, largura_imagem):

        """

            CARREGA IMAGEM A SER INSERIDO NO CANVAS CRIADO NO USER INTERFACE.

            # Arguments
                objeto                    - Required : Objeto Canvas. (UI)

            # Returns

        """

        try:
            # CANVAS_LOGO
            canvas_logo = self.builder.get_object(objeto)

            # SELECIONANDO A IMAGEM E CARREGANDO A IMAGEM - PESSOA
            Frame_Atuacao.seleciona_img_canvas(self, canvas_logo, imagem, altura_imagem, largura_imagem)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.carrega_img_canvas", str(ex))
            print(ex)


    def aplica_imagem_objeto(self, objeto_recebe_imagem, imagem):

        """

            APLICA UMA IMAGEM A UM OBJETO UI.

            # Arguments


            # Returns

        """

        try:
            # OBTENDO O OBJETO
            img_label = self.builder.get_object(objeto_recebe_imagem, self.root)

            # ABRINDO A IMAGEM USANDO PILs
            image = Image.open(self.img_path + "\\" + imagem)
            photo = ImageTk.PhotoImage(image, master=self.root)

            # APLICANDO A IMAGEM
            img_label.new_image = photo
            img_label.config(image = img_label.new_image)
        except Exception as ex:
            print(ex)


    @staticmethod
    def replace_variaveis(valor, valor_antigo, valor_novo):

        """

            FUNÇÃO QUE PERMITE A SUBSTITUIR ALGUMA PARTE DA VARIÁVEL POR UM NOVO VALOR.
            USO DA FUNÇÃO REPLACE.

            # Arguments
                caminho_api                 - Required : Caminho da API - MAR2. (String)

            # Returns
                validador                   - Required : Validador de execução da função. (Boolean)
                retorno_api                 - Required : Retorno do valor obtido via API. (List)

        """

        try:
            novo_valor_substituido = valor.replace(valor_antigo, valor_novo)
            return novo_valor_substituido
        except Exception as ex:
            return valor


    def executa_envio_email(self, queue_thread, args):

        """

            FUNÇÃO QUE PERMITE O ENVIO DE EMAIL.
            O ENVIO DE EMAIL É REALIZADO UTILIZANDO UM TEMPLATE OFT.
            EXECUTA A API ENVIA EMAIL.

            # Arguments
                Email_Envio                   - Optional : Caixa de Email de saída do email (String)
                Assunto                       - Optional : Assunto para envio no email (String)
                destinatarios_input           - Optional : Lista de emails para envio do email (List)
                Data_Operacao                 - Optional : Data para envio no email (String)
                Agencia                       - Optional : Agencia para envio no email (String)
                Conta                         - Optional : Conta para envio no email (String)
                PN                            - Optional : PN para envio no email (String)
                Produto                       - Optional : Produto para envio no email (String)
                Status                        - Optional : Status da operação para envio no email (String)
                texto_email                   - Optional : Texto de corpo para envio no email (String)
                texto_devolucao               - Optional : Texto de Devolução para envio no email (String)
                caminho_template_input        - Required : Caminho do template para envio do email (String)

            # Returns
                validador                   - Required : Validador de execução da função. (Boolean)
                retorno_api                 - Required : Retorno do valor obtido via API. (List)

        """

        validador = False

        caminho_api = args[0]
        email_envio = args[1]
        destinatarios = args[2]
        assunto = args[3]
        data_operacao = args[4]
        produto = args[5]
        agencia = args[6]
        conta = args[7]
        pn = args[8]
        status = args[9]
        texto_email = args[10]
        texto_devolucao = args[11]
        caminho_template = args[12]

        try:
            proc = subprocess.Popen([caminho_api, email_envio, destinatarios,
                                     assunto, data_operacao, produto,
                                     agencia, conta, pn, status,
                                     texto_email, texto_devolucao, caminho_template], stdout=subprocess.PIPE)
            retorno_api = proc.stdout.readline()
            validador = True

            print("EMAIL ENVIADO COM SUCESSO")

            try:
                retorno_api = Frame_Atuacao.replace_variaveis(retorno_api, "\n", "")
            except Exception as ex:
                print(ex)

            return retorno_api
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.executa_envio_email", str(ex))
            return validador


    def bt_menu_paineis_historico_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - HISTÓRICO DE OPERAÇÕES.
            ABRE UM PAINEL NO QUAL É POSSÍVEL BUSCAR O HISTÓRICO DE UMA OPERAÇÃO.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_paineis_skills_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - SKILLS.
            ABRE UM PAINEL CONTENDO SKILLS DE USUÁRIOS E PERMITINDO ALTERAÇÃO.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_paineis_meurelatorio_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - MEU RELATÓRIO.
            ABRE UM PAINEL CONTENDO O RELATÓRIO DE OPERAÇÕES DO USUÁRIO NO DIA.
            ESSA FUNÇÃO ESTÁ HABILITADA PARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_paineis_menu_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - MENU PRINCIPAL.
            ABRE O MENU PRINCIPAL.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS USUÁRIOS COM NÍVEL DE ACESSO AO MENU.

            # Arguments

            # Returns

        """

        if self.operacao_ativa == False:
            # O COLABORADOR NÃO ESTÁ COM OPERAÇÃO
            # ABRINDO MENU
            self.mainmenu = True
            # FECHANDO JANELA ATUAL
            Frame_Atuacao.fecha_frame(self)
        else:
            # O COLABORADOR ESTÁ COM OPERAÇÃO
            messagebox.showinfo("MODERNIZA SOAS", "A OPERAÇÃO DEVE SER FINALIZADA")


    def bt_menu_cadastro_produtos_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - CADASTRO - PRODUTOS.
            ABRE UM PAINEL NO QUAL É POSSÍVEL CADASTRAR NOVOS PRODUTOS E SUAS REGRAS DE NEGÓCIO.
            ESSA FUNÇÃO ESTÁ HABILITADA PARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_cadastro_colaboradores_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - COLABORADOES.
            ABRE UM PAINEL NO QUAL É POSSÍVEL CADASTRAR NOVOS COLABORADORES.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_relatorios_produtividade_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - RELATÓRIOS - PRODUTIVIDADE.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER O RELATÓRIO DE PRODUTIVIDADE DOS COLABORADORES.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_relatorios_produtos_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - RELATÓRIOS - PRODUTIVIDADE.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER O RELATÓRIO DE TMA E SLA DOS PRODUTOS.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_relatorios_meurelatorio_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - RELATÓRIOS - PRODUTIVIDADE.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER O RELATÓRIO DE PRODUTIVIDADE DO COLABORADOR.
            ESSA FUNÇÃO ESTÁ HABILITADA PARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_suporte_desenvolvedores_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - SOBRE - DESENVOLVEDORES.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER OS DESENVOLVEDORES DO MODERNIZA SOAS.
            ESSA FUNÇÃO ESTÁ HABILITADA APARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_menu_suporte_versao_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - PAINÉIS - COLABORADOES.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER A ATUAL VERSÃO DO MODERNIZA SOAS.
            ESSA FUNÇÃO ESTÁ HABILITADA PARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        try:
            # CHAMANDO O ORQUESTRADOR DO SOBRE VERSÃO
            Orquestrador_Sobre_Versao()
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_menu_suporte_versao_click", str(ex))


    def bt_menu_suporte_ajuda_click(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O MENU - SOBRE - AJUDA.
            ABRE UM PAINEL NO QUAL É POSSÍVEL OBTER AJUDA SOBRE O SISTEMA.
            ESSA FUNÇÃO ESTÁ HABILITADA PARA TODOS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def obtem_date_time(self, tipo_retorno):

        """

            OBTÉM TODOS OS POSSÍVEIS RETORNOS DE DATA E TEMPO.

            # Arguments
                tipo_retorno                    - Required : Formato de retorno. (String)

            # Returns

        """

        """%Y/%m/%d %H:%M:%S | %Y-%m-%d %H:%M:%S
        Dia: %d
        Mês: %
        Ano: %Y
        Data: %Y/%m/%d

        Hora: %H
        Minuto: %M
        Segundo: %S"""

        try:
            ts = time.time()
            stfim = datetime.datetime.fromtimestamp(ts).strftime(tipo_retorno)

            return stfim
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.obtem_date_time", str(ex))


    def verifica_pos_lost_focus(self, objeto_event, texto_original):

        """

            VERIFICA SE OS CAMPOS APÓS PERDEREM O FOCUS, TIVERAM ALGO PREENCHIDO, CASO NÃO, RETORNA AO TEXTO ORIGINAL.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)

            # Returns

        """

        # VERIFICANDO SE HÁ ALGO DIGITADO
        if objeto_event.get() == "":
            # CASO NÃO TENHA NADA DIGITADO, SUBSTITUI PELO TEXTO ORIGINAL
            try:
                # INSERINDO O TEXTO INICIAL DO OBJETO.
                objeto_event.insert(0, texto_original)
            except Exception as ex:
                print(ex)


    def clear_search(event, objeto_event):

        """

            LIMPA CAMPOS QUE JÁ POSSUEM TEXTO PRÉ DEFINIDO.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)

            # Returns

        """

        try:
            # DELETANDO O TEXTO INICIAL DO OBJETO.
            objeto_event.delete("1.0", tk.END)
        except Exception as ex:
            print(ex)


    def altera_componente_texto(self, componente_alteracao, config_alteracao, config_nova):

        """

            FUNÇÃO GEMÉRICA PARA ALTERAÇÃO DO TEXTO DE UM OBJETO.
            RECEBE O OBJETO, A CONFIGURAÇÃO A SER ALTERADA E O NOVO RESULTADO.

            # Arguments
                componente_alteracao           - Required : Objeto para alteração. (UI)
                config_alteracao               - Required : Configuração do Objeto que será alterada. (String)
                config_nova                    - Required : Novo resultado. (String)

            # Returns

        """

        try:
            # OBTENDO COMPONENTE
            componente = self.builder.get_object(componente_alteracao)

            componente[config_alteracao] = config_nova
        except Exception as ex:
            print(ex)


    def define_estado_botao(self, objeto, status_botao):

        """

            FUNÇÃO QUE DEFINE O ESTADO DE UM BOTÃO COMO HABILITADO/DESABILITADO.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)
                status_botao               - Required : Estado do botão (active/disabled). (String)

            # Returns

        """

        try:
            frame_1 = self.builder.get_object(objeto)
            frame_1["state"] = status_botao
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.define_estado_botao", str(ex))


    def define_estado_botoes_decisao(self, lista_frames_decisao, status_botao):

        """

            FUNÇÃO QUE DEFINE O ESTADO DOS BOTÕES DE DECISÃO COMO HABILITADO/DESABILITADO.

            # Arguments
                lista_frames_decisao            - Required : Objetos para ocorrer a ação. (UI)
                status_botao                    - Required : Estado do botão (enabled/disabled). (String)

            # Returns

        """

        for objeto in lista_frames_decisao:
            try:
                frame_1 = self.builder.get_object(objeto)
                frame_1["state"] = status_botao
            except Exception as ex:
                print(ex)
                Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.define_estado_botoes_decisao", str(ex))


    def percorre_campos_por_tipo(self, janela, tipo_campo, acao):

        """

            PERCORRE TODOS OS CAMPOS DADO O FRAME, ATRAVÉS DO TIPO DE CAMPO.
            HÁ UMA SÉRIE DE AÇÕES DISPONÍVEIS, SÃO ELAS:
            event_entrys: Nessa ação, ao percorrer os campos define-se eventos como get_focus ou lost_focus.


            # Arguments
                janela                   - Required : Janela que será percorrida. (String)
                tipo_campo               - Required : Tipo de campo a ser procurado. (String)
                acao                     - Required : Ação a ser realizada. (String)


            # Returns

        """

        try:
            children_widgets = janela.winfo_children()
            for children_widget in children_widgets:
                if children_widget.winfo_class().find(tipo_campo) != -1:
                    if acao == "event_entrys":
                        print(children_widget.get())
                        children_widget.destroy()
                    elif acao == "nomes_labels_paletas":
                        children_widget.destroy()
                    else:
                        print(children_widget.get())
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.percorre_campos_por_tipo", str(ex))


    def destroi_todos_campos(self, janela):

        """

            DESTRÓI TODOS OS CAMPOS DADO O FRAME, NÃO FILTRANDO ATRAVÉS DO TIPO DE CAMPO.

            # Arguments
                janela                   - Required : Janela que será percorrida. (String)
                tipo_campo               - Required : Tipo de campo a ser procurado. (String)
                acao                     - Required : Ação a ser realizada. (String)


            # Returns

        """

        try:
            children_widgets = janela.winfo_children()
            for children_widget in children_widgets:
                children_widget.destroy()
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.destroi_todos_campos", str(ex))


    def define_valor_variavel(self, campo_a_definir, valor_variavel):

        """

            REALIZA A DEFINIÇÃO DE UM VALOR DE VARIÁVEL JÁ INSTANCIADA NO UI.

            # Arguments
                campo_a_definir              - Required : Variável que será definida. (String)
                valor_variavel               - Required : Valor da variável a definir. (String)

            # Returns

        """

        try:
            self.builder.get_variable(campo_a_definir).set(valor_variavel)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.define_valor_variavel", str(ex))


    def clear_search(event, objeto_event):

        """

            LIMPA CAMPOS QUE JÁ POSSUEM TEXTO PRÉ DEFINIDO.

            # Arguments
                objeto_event               - Required : Objeto para ocorrer a ação. (UI)

            # Returns

        """

        try:
            # DELETANDO O TEXTO INICIAL DO OBJETO.
            objeto_event.delete(0, tk.END)
        except Exception as ex:
            print(ex)


    def events_entrys(self, objeto_entry):

        """

            DEFINE OS EVENTOS DE LIMPEZA DOS CAMPOS DE DADOS APÓS GET FOCUS.
            A LIMPEZA RETIRA OS RÓTULOS PRÉ DEFINIDOS.

            # Arguments
                objeto_entry            - Required : Objeto para entrada de dados. (UI)

            # Returns

        """

        try:
            # EVENTO APÓS GET FOCUS
            entry = self.builder.get_object(objeto_entry)
        except Exception as ex:
            pass
        try:
            entry.bind("<FocusIn>", lambda event, arg=entry: Frame_Atuacao.clear_search(event, arg))
        except Exception as ex:
            pass


    def preenche_label_informacoes_gerais(self, lista_proximaop, lista_usuario_data):

        """

            REALIZA O PREENCHIMENTO DAS INFORMAÇÕES DA OPERAÇÃO NA JANELA DE INFORMAÇÕES GERAIS (self.informacoes_gerais)
            HÁ OPERAÇÕES QUE SERÁ PREENCHIDO OS VALORES DE AG/CONTA.
            OUTRAS OPERAÇÕES PODEM PREENCHER APENAS PN E CNPJ.
            ESSE FLUXO É ADAPTADO PARA QUALQUER FLUXO DE PREENCHIMENTO DE INFORMAÇÕES GERAIS.
            (PRODUTO, AGÊNCIA, CONTA, PN, CNPJ, USUÁRIO E DATA ATUAL)


            # Arguments
                lista_proximaop            - Required : Lista contendo produto, agência, conta, pn, cnpj, usuário e data atual (List)
                lista_usuario_data         - Required : Lista contendo usuário e data atual (List)

            # Returns

        """

        try:
            # CARREGA PRODUTO
            Frame_Atuacao.define_valor_variavel(self, "value_label_produto", lista_proximaop[0])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.produto",
                                        str(ex))


        try:
            # CARREGA AGÊNCIA
            Frame_Atuacao.define_valor_variavel(self, "value_label_agencia", lista_proximaop[1])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.agencia",
                                        str(ex))

        try:
            # CARREGA CONTA
            Frame_Atuacao.define_valor_variavel(self, "value_label_conta", lista_proximaop[2])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.conta",
                                        str(ex))

        try:
            # CARREGA PN
            Frame_Atuacao.define_valor_variavel(self, "value_label_pn", lista_proximaop[3])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.pn",
                                        str(ex))

        try:
            # CARREGA CNPJ
            Frame_Atuacao.define_valor_variavel(self, "value_label_cnpj", lista_proximaop[4])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.cnpj",
                                        str(ex))

        try:
            # CARREGA USUÁRIO
            Frame_Atuacao.define_valor_variavel(self, "value_label_usuario", lista_usuario_data[0])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.usuario",
                                        str(ex))

        try:
            # CARREGA DATA ATUAL
            Frame_Atuacao.define_valor_variavel(self, "value_label_calendar", lista_usuario_data[1])
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(),
                                        "Frame_Atuacao.preenche_label_informacoes_gerais.data",
                                        str(ex))


    @staticmethod
    def define_qtde_linhas_colunas(quantidade_componentes, quantidade_maxima_componentes):

        """

            REALIZA O CÁLCULO MATEMÁTICO PARA CÁLCULO DE QUANTOS COMPONENTES SERÃO INSERIDOS EM TELA.
            BASEIA-SE NA QUANTIDADE DE DADOS COMPLEMENTARES QUE O PRODUTO NECESSITA.


            # Arguments
                quantidade_componentes            - Required : Quantidade de componentes para o produto (Integer)
                quantidade_maxima_componentes     - Required : Quantidade máxima de componentes por linha (Integer)

            # Returns

        """

        try:
            quantidade = quantidade_componentes
            quantidade_maxima_colunas = quantidade_maxima_componentes

            quantidade_linhas = ceil(quantidade/quantidade_maxima_colunas)
            quantidade_resto = quantidade % quantidade_maxima_colunas

            if quantidade_resto == 0:
                return quantidade_linhas, quantidade_maxima_componentes
            else:
                return quantidade_linhas, quantidade_resto
        except Exception as ex:
            print(ex)


    def cria_label_informacoes_complementares(self, proxima_operacao, quantidade_maxima_componentes):

        """

            ORQUESTRADOR PRINCIPAL QUE REALIZA A CRIAÇÃO DOS COMPONENTES REQUISITADOS PELO PRODUTO.
            A FUNÇÃO TAMBÉM ORQUESTRA A ETAPA DE INSERT DOS VALORES JÁ CARREGADOR A PARTIR DAS INFORMAÇÕES COMPLEMENTARES.


            # Arguments
                quantidade_componentes            - Required : Quantidade de componentes para o produto (Integer)
                quantidade_maxima_componentes     - Required : Quantidade máxima de componentes por linha (Integer)

            # Returns

        """

        try:
            # OBTENDO O PRODUTO
            produto = proxima_operacao[0]
            quantidade_entrys = proxima_operacao[5]
            quantidade_combobox = proxima_operacao[6]

            lista_campos = JSON_Executa.get_keys_json(proxima_operacao[7])

            # OBTENDO A QUANTIDADE TOTAL DE COMPONENTES REQUISITADOS
            quantidade_componentes = quantidade_entrys + quantidade_combobox

            # OBTENDO A QUANTIDADE TOTAL DE LINHAS E COLUNAS
            qtde_linhas, qtde_colunas = Frame_Atuacao.define_qtde_linhas_colunas(quantidade_componentes,
                                                                                 quantidade_maxima_componentes)

            # INICIANDO O CONTADOR DE LINHAS (permite controlar em qual linha está sendo gridado os componentes)
            contador_linhas = 1
            # INICIANDO O CONTADOR DE CAMPOS (permite controlar quantos componentes já foram gridados)
            contador_campos = 1

            pady_acumulativo = 20

            qtde_linhas_percorrer = (2 + (qtde_linhas - 1) * 2)

            for linha in range(0, qtde_linhas_percorrer, 2):

                if contador_linhas == qtde_linhas:
                    qtde_colunas_atual = qtde_colunas
                else:
                    qtde_colunas_atual = quantidade_maxima_componentes

                for coluna in range(0, qtde_colunas_atual, 1):

                    if coluna == 2:
                        valor_padx = 30
                    else:
                        valor_padx = 40

                    # OBTENDO O TIPO DE CADA COMPONENTE A SER COLOCADO NA TELA
                    tipo_dado_atual = JSON_Executa.get_value_json(proxima_operacao[8], lista_campos[contador_campos-1])

                    # INSERINDO O LABEL
                    self.nomelabel = "lbl" + str(linha) + str(coluna)
                    self.nomelabel = tk.Label(self.campos, text=lista_campos[contador_campos-1], background="#dddddd")
                    self.nomelabel.grid(row=0, column=coluna, pady=pady_acumulativo, sticky='n')

                    # TOMADA DE DECISÃO DE QUAL TIPO DE COMPONENTE A SER INSERIDO NA TELA
                    if tipo_dado_atual == "ENTRY":

                        nomecomponente = "ed" + str(linha + 1) + str(coluna)

                        nomecomponente = tk.Entry(self.campos)
                        nomecomponente.grid(row=0, column=coluna, pady=pady_acumulativo+30, sticky='n')
                        nomecomponente.configure(justify="center")

                    if tipo_dado_atual == "COMBOBOX":

                        nomecomponente = "combo" + str(linha + 1) + str(coluna)

                        nomecomponente = tk.ttk.Combobox(self.campos)
                        nomecomponente.grid(row=0, column=coluna, pady=pady_acumulativo+30, sticky='n')
                        nomecomponente.configure(justify="center")

                    # REALIZA O INSERT DE VALORES
                    nomecomponente.insert(0, JSON_Executa.get_value_json(proxima_operacao[7], lista_campos[contador_campos-1]))

                    # CONTABILIZANDO MAIS UM CAMPO JÁ DEFINIDO EM TELA
                    contador_campos +=1

                # CONTABILIZANDO MAIS UMA LINHA PREENCHIDA
                contador_linhas +=1
                pady_acumulativo +=60
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.cria_label_informacoes_complementares", str(ex))


    def abrindo_imagem_usando_pil(self, nome_imagem):

        """

            FUNÇÃO GENÉRICA QUE PERMITE ABRIR A INSTÂNCIA DE UMA IMAGEM UTILIZANDO O PILLOW.

            # Arguments
                nome_imagem            - Required : Nome da imagem que será instanciada (String)

            # Returns
                photo                  - Required : Instância aberta (PIL)

        """

        try:
            # ABRINDO A IMAGEM USANDO PILs
            image = Image.open(self.img_path + "\\" + nome_imagem)
            photo = ImageTk.PhotoImage(image, master=self.root)

            return photo
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.abrindo_imagem_usando_pil",
                                        str(ex))
            return None


    def aplica_imagem_usando_pil(self, objeto_para_imagem, photo):

        """

            FUNÇÃO GENÉRICA QUE PERMITE APLICAR A IMAGEM A UM OBJETO QUE POSSUI RECURSO IMAGE.

            # Arguments
                objeto_para_imagem            - Required : Nome do objeto que receberá a imagem (UI)
                nome_imagem                   - Required : Nome da imagem instanciada (PIL)

            # Returns

        """

        try:
            # APLICANDO A IMAGEM
            objeto_para_imagem.new_image = photo
            objeto_para_imagem.config(image=objeto_para_imagem.new_image)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.aplica_imagem_usando_pil",
                                        str(ex))


    @staticmethod
    def obtem_nome_separado(produto):

        """

            FUNÇÃO GENÉRICA QUE PERMITE OBTER O NOME SEPARADO PARA APLICAR DE FORMA QUEBRADA.

            # Arguments
                produto                       - Required : Nome que receberá a quebra (String)

            # Returns
                nome_produto_total            - Required : Nome após separação (String)

        """

        try:
            nome_produto_total = ""
            for nome_produto_separado in produto.split():
                nome_produto_total = nome_produto_total + nome_produto_separado + "\n"
            return nome_produto_total
        except Exception as ex:
            print(ex)
            return produto


    def cria_label_sinaleiros(self, proxima_operacao, etapas_processo, cor_bg):

        """

            ORQUESTRADOR PRINCIPAL QUE REALIZA A CRIAÇÃO DOS COMPONENTES DE SINALEIRO PARA O PROCESSO.
            A FUNÇÃO TAMBÉM ORQUESTRA A ETAPA DE INSERT DAS DATAS DE ENCERRAMENTO DAS ETAPAS JÁ ENCERRADAS.


            # Arguments
                quantidade_componentes            - Required : Quantidade de componentes para o produto (Integer)
                quantidade_maxima_componentes     - Required : Quantidade máxima de componentes por linha (Integer)

            # Returns

        """

        try:
            # OBTENDO A QUANTIDADE DE ETAPAS DO PROCESSO
            quantidade_etapas_processo = len(etapas_processo)
        except Exception as ex:
            print(ex)
            quantidade_etapas_processo = 2

        # INICIANDO O CONTADOR DE CAMPOS (permite controlar quantos componentes já foram gridados)
        contador_campos = 0

        # PARA CADA UMA DAS ETAPAS - INCLUSÃO DO LABEL (COM SINAL) E DATA ENCERRAMENTO
        self.dict_label = {}
        self.dict_nomesinal = {}
        for etapa_atual in range(quantidade_etapas_processo):

            self.key = 0

            # INCLUSÃO DO SINAL (IMAGEM)
            self.nomesinal = "sinal_sinaleiro" + str(etapa_atual)
            self.nomesinal = tk.Label(self.sinaleiro, text=etapas_processo[etapa_atual][0],
                                      background=cor_bg, name=self.nomesinal)
            self.nomesinal.grid(row=contador_campos, column=0)

            self.dict_nomesinal[self.nomesinal] = self.nomesinal

            # DISTRIBUIÇÃO  CIRCULO VERDE
            # ETAPA ATUAL (PROXIMA OPERAÇÃO) - SINAL AMARELO
            # ETAPAS JÁ FEITAS - SINAL VERDE
            # ETAPAS AINDA NÃO REALIZADAS, SENDO POSTERIORES À ETAPA ATUAL - SINAL CINZA

            if etapa_atual == 0:
                imagem = "circulo_verde.png"
            elif etapas_processo[etapa_atual][0] == proxima_operacao:
                imagem = "sinal_amarelo.png"
            elif etapas_processo[etapa_atual][1]!= "":
                imagem = "sinal_verde.png"
            else:
                imagem = "sinal_cinza.png"

            # ABRINDO A IMAGEM USANDO PIL's (SINALEIRO A SER APLICADO)
            imagem_objeto = Frame_Atuacao.abrindo_imagem_usando_pil(self, imagem)

            # APLICANDO A IMAGEM (SINALEIRO A SER APLICADO)
            imagem_objeto = Frame_Atuacao.aplica_imagem_usando_pil(self, self.nomesinal, imagem_objeto)

            nome_produto_total = Frame_Atuacao.obtem_nome_separado(etapas_processo[etapa_atual][0])

            # INCLUSÃO DO LABEL
            self.nomelabel = "lbl_sinaleiro" + str(etapa_atual)
            self.nomelabel = tk.Label(self.sinaleiro,
                                      text=nome_produto_total + etapas_processo[etapa_atual][1],
                                      background=cor_bg, foreground="#ffffff", name=self.nomelabel)
            self.nomelabel.grid(row=contador_campos + 1, column=0)

            self.dict_label[self.nomelabel] = self.nomelabel

            contador_campos +=2


    def obtem_etapas_proxima_operacao(self, id_produto):

        """

            FUNÇÃO UTILIZADA PARA REALIZAR A QUERY QUE RETORNA AS ETAPAS DO PRODUTO DA PRÓXIMA OPERAÇÃO.

            # Arguments
                id_produto                     - Required: Id do produto da próxima operação (Integer)

            # Returns
                etapas_proxima_operacao        - Required: Etapas da próxima operação (List)

        """

        if id_produto == 1:
            etapas_processo_atual = [["DISTRIBUIÇÃO", "08/05/2020 10:00"], ["ANTECIPAÇÃO CADASTRO", "08/05/2020 12:10"],
                                     ["ANTECIPAÇÃO LIBERAÇÃO", "08/05/2020 12:30"], ["TEF CONTA VINCULADA", ""]]
        elif id_produto == 2:
            etapas_processo_atual = [["DISTRIBUIÇÃO", "06/05/2020 11:00"], ["GIROCOMP PN", ""],
                                     ["GIROCOMP DUPLO CHECK", ""]]
        else:
            etapas_processo_atual = [["DISTRIBUIÇÃO", "05/05/2020 11:00"], ["GIROCOMP PN", "06/05/2020 18:65"],
                                     ["GIROCOMP DUPLO CHECK", ""]]

        return etapas_processo_atual


    def proxima_operacao(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE PRÓXIMA OPERAÇÃO.
            REALIZA O CARREGAMENTO DA PRÓXIMA OPERAÇÃO UTILIZANO-SE DO RETORNO DO FLUXO DE OBTENÇÃO DA PRÓXIMA OPERAÇÃO.

            # Arguments

            # Returns

        """

        try:
            # OBTENDO RACF
            racf_usuario = os.getlogin().upper()

            # OBTENDO DATA ATUAL
            data_atual = Frame_Atuacao.obtem_date_time(self, "%d")

            # OBTENDO DATA E HORA DE INICIO DA OPERAÇÃO
            self.data_inicio = Frame_Atuacao.obtem_date_time(self, "%d/%m/%Y")
            self.hora_inicio = Frame_Atuacao.obtem_date_time(self, "%H:%M:%S")

            print("A OPERAÇÃO ESTÁ INICIANDO EM {} - {}".format(self.data_inicio, self.hora_inicio))

            # OBTENDO AS INFORMAÇÕES GERAIS DA PRÓXIMA OPERAÇÃO

            # ISSO AQUI É SÓ PARA IR ATUALIZANDO AS OPERAÇÕES NOS TESTES
            self.quantidade_produto +=1
            produto = self.quantidade_produto

            if produto == 1:

                # OBTENDO OPERAÇÃO A SER PROCESSADA (SKILL/ FIFO / PRIORIDADES)
                self.proxima_operacao = ["TEF CONTA VINCULADA", "8325", "17711-5", "", "774.628.404-30"]

                # OBTENDO AS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_dados = {"SUBPRODUTO": "DUPLO CHECK", "GARANTIA": "RENEGOCIAÇÃO",
                              "VALOR": 1000000, "NºCONTRATO": 85215697, "DATA VENCIMENTO": "", "DATA CONTRATAÇÃO": "",
                              "DATA CONTATO TELEFÔNICO": "06/05/2020", "PLATAFORMA": "6325"}

                # OBTENDO OS TIPOS DE COMPONENTES DAS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_tipos_dados = {"SUBPRODUTO": "COMBOBOX", "GARANTIA": "ENTRY",
                                    "VALOR": "ENTRY", "NºCONTRATO": "ENTRY", "DATA VENCIMENTO": "ENTRY",
                                    "DATA CONTRATAÇÃO": "ENTRY",
                                    "DATA CONTATO TELEFÔNICO": "ENTRY", "PLATAFORMA": "COMBOBOX"}

                etapas_processo_atual = Frame_Atuacao.obtem_etapas_proxima_operacao(self, 1)

            elif produto == 2:
                # OBTENDO OPERAÇÃO A SER PROCESSADA (SKILL/ FIFO / PRIORIDADES)
                self.proxima_operacao = ["GIROCOMP PN", "", "", "15975385", "774.628.404-30"]

                # OBTENDO AS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_dados = {"SUBPRODUTO": "DUPLO CHECK", "GARANTIA": "RENEGOCIAÇÃO",
                              "VALOR": 1000000, "NºCONTRATO": 85215697, "SITO": "", "Nº BOLETO": ""}

                # OBTENDO OS TIPOS DE COMPONENTES DAS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_tipos_dados = {"SUBPRODUTO": "COMBOBOX", "GARANTIA": "ENTRY",
                                    "VALOR": "ENTRY", "NºCONTRATO": "ENTRY", "SITO": "ENTRY", "Nº BOLETO": "ENTRY"}

                etapas_processo_atual = Frame_Atuacao.obtem_etapas_proxima_operacao(self, 2)
            else:
                # OBTENDO OPERAÇÃO A SER PROCESSADA (SKILL/ FIFO / PRIORIDADES)
                self.proxima_operacao = ["GIROCOMP DUPLO CHECK", "", "", "85214796", "432.622.738-62"]

                # OBTENDO AS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_dados = {"SUBPRODUTO": "DUPLO CHECK", "GARANTIA": "RENEGOCIAÇÃO",
                              "VALOR": 150000, "NºCONTRATO": 85214796, "SITO": "REGULARIZADO"}

                # OBTENDO OS TIPOS DE COMPONENTES DAS INFORMAÇÕES COMPLEMENTARES DA PRÓXIMA OPERAÇÃO
                json_tipos_dados = {"SUBPRODUTO": "COMBOBOX", "GARANTIA": "ENTRY",
                                    "VALOR": "ENTRY", "NºCONTRATO": "ENTRY", "SITO": "ENTRY"}

                etapas_processo_atual = Frame_Atuacao.obtem_etapas_proxima_operacao(self, 3)


            # OBTENDO A QUANTIDADE DE CADA TIPO DE COMPONENTE
            quantidade_entrys = JSON_Executa.get_values_tipos_json(json_tipos_dados, "ENTRY")
            quantidade_combobox = JSON_Executa.get_values_tipos_json(json_tipos_dados, "COMBOBOX")

            # OBTENDO A QUANTIDADE DE CADA TIPO DE COMPONENTE
            self.proxima_operacao.extend([quantidade_entrys, quantidade_combobox, json_dados, json_tipos_dados])

            # OBTENDO INFORMACOES DE DATA E USUÁRIO
            usario_data = [racf_usuario, data_atual]

            # PREENCHE LABEL DE INFORMAÇÕES GERAIS
            Frame_Atuacao.preenche_label_informacoes_gerais(self, self.proxima_operacao, usario_data)

            # CRIA CAMPOS E PREENCHE COM OS DADOS JÁ EXISTENTES
            Frame_Atuacao.cria_label_informacoes_complementares(self, self.proxima_operacao,
                                                                self.quantidade_maximo_componentes)

            # CRIA OS SINALEIROS E PREENCHE COM DATAS DE ENCERRAMENTOS
            Frame_Atuacao.cria_label_sinaleiros(self, self.proxima_operacao[0], etapas_processo_atual, self.frente)

            # DESABILITA O BOTÃO DE PRÓXIMA OPERAÇÃO
            Frame_Atuacao.define_estado_botao(self, "bt_pausar_op", "active")

            # HABILITANDO TODOS OS BOTÕES DE DECISÃO
            Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "active")

            # VARIÁVEL GLOBAL PARA IDENTIFICAÇÃO DE OPERAÇÃO ATIVA
            self.operacao_ativa = True

            # INICIO DO RELÓGIO DA OPERAÇÃO
            Frame_Atuacao.thread_open(self, Frame_Atuacao.timer, "start_relogio", self.queue)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.proxima_operacao",
                                        str(ex))


    def busca_proxima_operacao(self):

        """

            FUNÇÃO UTILIZADA PARA INICIAR A PROXIMA OPERAÇÃO E MOSTRAR NA TELA PARA O USUÁRIO.

            # Arguments

            # Returns

        """

        if self.pausa_op is False:
            # OBTENDO A PRÓXIMA OPERAÇÃO E MOSTRANDO AO USUÁRIO
            Frame_Atuacao.proxima_operacao(self)

        else:
            # PAUSA ATIVADA
            Frame_Atuacao.pausa_ativa(self)


    @staticmethod
    def confirmar_acao():

        """

            FUNÇÃO UTILIZADA PARA CONFIRMAR AÇÕES.

            # Arguments

            # Returns
            validador_acao                - Required: Boolean contendo o resultado do MsgBox (Boolean)

        """

        try:
            MsgBox = messagebox.askquestion("MODERNIZA SOAS", "DESEJA REALMENTE REALIZAR ESSA AÇÃO?",
                                            icon='warning')
            if MsgBox == 'yes':
                return MsgBox
            else:
                return "no"
        except Exception as ex:
            # CASO OCORRA ALGUM ERRO, CONFIRMAMOS A AÇÃO
            print(ex)
            return "yes"


    def altera_status_botao_pausar(self, status_atual_pausa):

        """

            FUNÇÃO UTILIZADA PARA ALTERAR A IMAGEM DO BOTÃO DE PAUSAR OPERAÇÕES.
            PAUSA ATIVA - CANCELAR PAUSA
            PAUSA NÃO ATIVA - PAUSAR OPERAÇÕES

            # Arguments

            # Returns
            validador_acao                - Required: Boolean contendo o resultado do MsgBox (Boolean)

        """

        if status_atual_pausa == True:
            if self.operacao_ativa == True:
                # O OPERADOR DESEJA PAUSAR, MAS ATUALMENTE ESTÁ COM OPERAÇÃO ATIVA
                imagem = "cancelar_pausa_dark.png"
            else:
                # O OPERADOR DESEJA PAUSAR E ATUALMENTE NÃO ESTÁ COM OPERAÇÃO ATIVA
                imagem = "retomar_pausa_dark.png"
        else:
            if self.operacao_ativa == True:
                # O OPERADOR DESEJA CANCELAR PAUSA, MAS ATUALMENTE ESTÁ COM OPERAÇÃO ATIVA
                imagem = "pausa_light.png"
            else:
                # O OPERADOR DESEJA CANCELAR PAUSA, MAS ATUALMENTE ESTÁ COM RELÓGIO DE PAUSA ATIVO
                # ALTERA IMAGEM DO BOTÃO
                imagem = "pausa_light.png"
                # LOG DE DESPAUSE
                Frame_Atuacao.registra_log_fim_pausa(self)
                # INICIA NOVA OPERAÇÃO
                Frame_Atuacao.busca_proxima_operacao(self)

        try:
            # ALTERANDO A IMAGEM DO BOTÃO
            # ABRINDO A IMAGEM USANDO PIL's (SINALEIRO A SER APLICADO)
            imagem_objeto = Frame_Atuacao.abrindo_imagem_usando_pil(self, imagem)

            botao = self.builder.get_object("bt_pausar_op")

            # APLICANDO A IMAGEM (SINALEIRO A SER APLICADO)
            imagem_objeto = Frame_Atuacao.aplica_imagem_usando_pil(self, botao, imagem_objeto)

            if status_atual_pausa == True:
                if self.operacao_ativa == True:
                    messagebox.showinfo("MODERNIZA SOAS", "PAUSA AGENDADA")
                else:
                    messagebox.showinfo("MODERNIZA SOAS", "PAUSA INICIADA")
            else:
                messagebox.showinfo("MODERNIZA SOAS", "PAUSA CANCELADA")

        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.altera_status_botao_pausar",
                                        str(ex))


    def bt_pausar_op_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE PAUSAR.
            REALIZA a CRIAÇÃO DO LOG DE PAUSA DO USUÁRIO, IMPEDINDO A DISTRIBUIÇÃO DE UMA NOVA OPERAÇÃO PARA O USUÁRIO.

            # Arguments

            # Returns

        """

        # OBTENDO A CONFIRMAÇÃO DE AÇÃO
        validador_acao = Frame_Atuacao.confirmar_acao()

        if validador_acao == "yes":

            # DEFININDO A PAUSA COMO ATIVA/NÃO ATIVA GLOBALMENTE NA CLASSE
            if self.pausa_op is False:
                self.pausa_op = True
            else:
                self.pausa_op = False

            Frame_Atuacao.altera_status_botao_pausar(self, self.pausa_op)


    def registra_log_pausa(self):

        """

           FUNÇÃO QUE REALIZA O REGISTRO DE PAUSA NO BANCO DE DADOS DE LOGS.

           # Arguments

           # Returns
               validador_orquestrador      - Required : Validador de execução do registro de pausa. (Boolean)

       """

        try:
            # OBTENDO DATA E HORA ATUAL
            data_hora_atual = Frame_Atuacao.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path_logs

            # DEFININDO SSQL E PARÂMETROS
            ssql = "INSERT INTO TBL_PAUSA(FUNCIONAL, DT_HR_INICIO, PAUSA_EM_OPERACAO) VALUES (?, ?, ?)"
            params = (self.funcional_usuario, data_hora_atual, self.operacao_ativa)

            # REALIZANDO A QUERY - INSERT
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[1])
            validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.registra_log_pausa", str(ex))


    def registra_log_fim_pausa(self):

        """

           FUNÇÃO QUE REALIZA O REGISTRO DO FIM DA PAUSA NO BANCO DE DADOS DE LOGS.

           # Arguments

           # Returns
               validador_orquestrador      - Required : Validador de execução do registro de fim da pausa. (Boolean)

       """

        try:
            # OBTENDO DATA E HORA ATUAL
            data_hora_atual = Frame_Atuacao.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path_logs

            # DEFININDO SSQL E PARÂMETROS
            ssql = "UPDATE TBL_PAUSA SET DT_HR_FINAL = ? " \
                   "WHERE ID_PAUSA = (SELECT ID_PAUSA FROM TBL_PAUSA WHERE FUNCIONAL = ? " \
                   "ORDER BY ID_PAUSA DESC LIMIT 1)"
            params = (data_hora_atual, self.funcional_usuario)

            # REALIZANDO A QUERY - UPDATE
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[3])
            validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.registra_log_fim_pausa", str(ex))


    def pausa_ativa(self):

        """

            AÇÃO REALIZADA APÓS A FINALIZAÇÃO DE UMA OPERAÇÃO COM A PAUSA ATIVADA.
            REALIZA O INICIO DA PAUSA ATÉ QUE O COLABORADOR CLIQUE EM RETOMAR OPERAÇÕES.

            # Arguments

            # Returns

        """

        # HABILITANDO RELÓGIO DE PAUSA
        print("RELÓGIO DE PAUSA ATIVADO")

        # INSERINDO LOG DE PAUSA INICIADA
        Frame_Atuacao.registra_log_pausa(self)

        # BOTÃO DE PAUSAR COM IMAGEM DE RETOMAR OPERAÇÕES
        Frame_Atuacao.altera_status_botao_pausar(self, self.pausa_op)


    def bt_aprovar_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE APROVAR.
            REALIZA A ATUALIZAÇÃO DA OPERAÇÃO UTILIZANDO O FLUXO DE APROVAÇÃO.

            # Arguments

            # Returns

        """

        try:
            # OBTENDO A CONFIRMAÇÃO DE AÇÃO
            validador_acao = Frame_Atuacao.confirmar_acao()

            if validador_acao == "yes":

                email_envio_input = ""
                destinatarios_input = ""
                assunto_input = "[OPERAÇÃO APROVADA] AGÊNCIA {} - CONTA {}".format(self.proxima_operacao[1], self.proxima_operacao[2])
                data_operacao_input = self.data_inicio
                produto_input = self.proxima_operacao[0]
                agencia_input = self.proxima_operacao[1]
                conta_input = self.proxima_operacao[2]
                pn_input = self.proxima_operacao[3]
                status_input = "APROVADA"
                texto_input = ""
                texto_devolucao_input = ""
                caminho_template_input = os.getcwd() + "\Templates_Emails" + "\\" + "Template_Agencia_Conta_Aprovada.oft"

                try:
                    # ENVIA EMAIL
                    validador_email = Frame_Atuacao.thread_open(self, Frame_Atuacao.executa_envio_email,
                                                                "envia_email", self.queue,
                                                                self.api_envia_email, email_envio_input,
                                                                destinatarios_input, assunto_input,
                                                                data_operacao_input, produto_input,
                                                                agencia_input, conta_input,
                                                                pn_input, status_input,
                                                                texto_input, texto_devolucao_input,
                                                                caminho_template_input)

                    # MESSAGE BOX AO USUÁRIO
                    messagebox.showinfo("MODERNIZA SOAS", "OPERAÇÃO APROVADA COM SUCESSO")

                    # DESTRÓI TODOS OS COMPONENTES EM TELA
                    Frame_Atuacao.destroi_todos_campos(self, self.campos)
                    Frame_Atuacao.destroi_todos_campos(self, self.sinaleiro)

                    # HABILITA NOVAMENTE O BOTÃO DE PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.define_estado_botao(self, "bt_pausar_op", "active")

                    # DESABILITANDO TODOS OS BOTÕES DE DECISÃO
                    Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "disabled")

                    # VARIÁVEL GLOBAL PARA IDENTIFICAÇÃO DE OPERAÇÃO ATIVA
                    self.operacao_ativa = False

                    # BUSCANDO PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.busca_proxima_operacao(self)
                except Exception as ex:
                    Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_aprovar_click",
                                                str(ex))
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_aprovar_click",
                                        str(ex))

        # FECHA THREAD DE TIMER
        try:
            if validador_acao == "yes":
                Frame_Atuacao.kill_threads(self, self.queue)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_aprovar_click",
                                        str(ex))


    def bt_devolver_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE DEVOLVER.
            REALIZA A ATUALIZAÇÃO DA OPERAÇÃO UTILIZANDO O FLUXO DE DEVOLUÇÃO.

            # Arguments

            # Returns

        """

        try:
            # OBTENDO A CONFIRMAÇÃO DE AÇÃO
            validador_acao = Frame_Atuacao.confirmar_acao()

            if validador_acao == "yes":

                email_envio_input = ""
                destinatarios_input = ""
                assunto_input = "[OPERAÇÃO DEVOLVIDA] AGÊNCIA {} - CONTA {}".format(self.proxima_operacao[1], self.proxima_operacao[2])
                data_operacao_input = self.data_inicio
                produto_input = self.proxima_operacao[0]
                agencia_input = self.proxima_operacao[1]
                conta_input = self.proxima_operacao[2]
                pn_input = self.proxima_operacao[3]
                status_input = "DEVOLVIDA"
                texto_input = ""
                texto_devolucao_input = "ERRO NA FORMALIZAÇÃO DO DOCUMENTO"
                caminho_template_input = os.getcwd() + "\Templates_Emails" + "\\" + "Template_Agencia_Conta_Devolvida.oft"

                try:
                    # ENVIA EMAIL
                    validador_email = Frame_Atuacao.thread_open(self, Frame_Atuacao.executa_envio_email,
                                                                "envia_email", self.queue,
                                                                self.api_envia_email, email_envio_input,
                                                                destinatarios_input, assunto_input,
                                                                data_operacao_input, produto_input,
                                                                agencia_input, conta_input,
                                                                pn_input, status_input,
                                                                texto_input, texto_devolucao_input,
                                                                caminho_template_input)

                    # MESSAGE BOX AO USUÁRIO
                    messagebox.showinfo("MODERNIZA SOAS", "OPERAÇÃO DEVOLVIDA COM SUCESSO")

                    # DESTRÓI TODOS OS COMPONENTES EM TELA
                    Frame_Atuacao.destroi_todos_campos(self, self.campos)
                    Frame_Atuacao.destroi_todos_campos(self, self.sinaleiro)

                    # HABILITA NOVAMENTE O BOTÃO DE PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.define_estado_botao(self, "bt_pausar_op", "active")

                    # DESABILITANDO TODOS OS BOTÕES DE DECISÃO
                    Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "disabled")

                    # VARIÁVEL GLOBAL PARA IDENTIFICAÇÃO DE OPERAÇÃO ATIVA
                    self.operacao_ativa = False

                    # BUSCANDO PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.busca_proxima_operacao(self)
                except Exception as ex:
                    Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_devolver_click",
                                                str(ex))
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_devolver_click",
                                        str(ex))

        # FECHA THREAD DE TIMER
        try:
            if validador_acao == "yes":
                Frame_Atuacao.kill_threads(self, self.queue)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_devolver_click",
                                        str(ex))


    def bt_followup_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE FOLLOW UP.
            REALIZA A ATUALIZAÇÃO DA OPERAÇÃO UTILIZANDO O FLUXO DE FOLLOW UP.

            # Arguments

            # Returns

        """

        try:
            # OBTENDO A CONFIRMAÇÃO DE AÇÃO
            validador_acao = Frame_Atuacao.confirmar_acao()

            if validador_acao == "yes":

                try:
                    # MESSAGE BOX AO USUÁRIO
                    messagebox.showinfo("MODERNIZA SOAS", "OPERAÇÃO COLOCADA EM FOLLOW UP COM SUCESSO")

                    # DESTRÓI TODOS OS COMPONENTES EM TELA
                    Frame_Atuacao.destroi_todos_campos(self, self.campos)
                    Frame_Atuacao.destroi_todos_campos(self, self.sinaleiro)

                    # HABILITA NOVAMENTE O BOTÃO DE PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.define_estado_botao(self, "bt_pausar_op", "active")

                    # DESABILITANDO TODOS OS BOTÕES DE DECISÃO
                    Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "disabled")

                    # VARIÁVEL GLOBAL PARA IDENTIFICAÇÃO DE OPERAÇÃO ATIVA
                    self.operacao_ativa = False

                    # BUSCANDO PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.busca_proxima_operacao(self)
                except Exception as ex:
                    Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_followup_click",
                                                str(ex))
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_followup_click",
                                        str(ex))

        # FECHA THREAD DE TIMER
        try:
            if validador_acao == "yes":
                Frame_Atuacao.kill_threads(self, self.queue)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_followup_click",
                                        str(ex))


    def bt_duplicidade_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE DUPLICIDADE.
            REALIZA A ATUALIZAÇÃO DA OPERAÇÃO UTILIZANDO O FLUXO DE DUPLICIDADE.

            # Arguments

            # Returns

        """

        try:
            # OBTENDO A CONFIRMAÇÃO DE AÇÃO
            validador_acao = Frame_Atuacao.confirmar_acao()

            if validador_acao == "yes":

                try:
                    # MESSAGE BOX AO USUÁRIO
                    messagebox.showinfo("MODERNIZA SOAS", "OPERAÇÃO COLOCADA EM DUPLICIDADE COM SUCESSO")

                    # DESTRÓI TODOS OS COMPONENTES EM TELA
                    Frame_Atuacao.destroi_todos_campos(self, self.campos)
                    Frame_Atuacao.destroi_todos_campos(self, self.sinaleiro)

                    # HABILITA NOVAMENTE O BOTÃO DE PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.define_estado_botao(self, "bt_pausar_op", "active")

                    # DESABILITANDO TODOS OS BOTÕES DE DECISÃO
                    Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "disabled")

                    # VARIÁVEL GLOBAL PARA IDENTIFICAÇÃO DE OPERAÇÃO ATIVA
                    self.operacao_ativa = False

                    # BUSCANDO PRÓXIMA OPERAÇÃO
                    Frame_Atuacao.busca_proxima_operacao(self)
                except Exception as ex:
                    Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_duplicidade_click",
                                                str(ex))
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_duplicidade_click",
                                        str(ex))

        # FECHA THREAD DE TIMER
        try:
            if validador_acao == "yes":
                Frame_Atuacao.kill_threads(self, self.queue)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.bt_duplicidade_click",
                                        str(ex))


    def configura_barra_rolagem(self, frame_barra_rolagem, objeto_barra_rolagem,
                                frame_objeto_vinculado, objeto_vinculado):

        """

            FUNÇÃO UTILIZADA PARA REALIZAR O VÍNCULO DE COMPONENTES TIPO SCROLL COM OUTROS COMPONENTES.

            # Arguments
            frame_barra_rolagem             - Required : Frame que contém o componente scroll (UI)
            objeto_barra_rolagem            - Required : Scroll que será manipulado (String)
            frame_objeto_vinculado          - Required : Frame que contém o componente que receberá o vínculo (UI)
            objeto_vinculado                - Required : Componente que receberá o vínculo (String)

            # Returns

        """

        try:
            # OBTENDO A BARRA DE ROLAGEM
            scroll = self.builder.get_object(objeto_barra_rolagem, frame_barra_rolagem)
        except Exception as ex:
            pass

        try:
            # OBTENDO O OBJETO VINCULADO
            objeto_vinculado_scroll = self.builder.get_object(objeto_vinculado, frame_objeto_vinculado)
        except Exception as ex:
            pass

        try:
            # DEFININDO O VINCULO
            objeto_vinculado_scroll["yscrollcommand"] = scroll.set
            scroll.config(command=objeto_vinculado_scroll.yview)
        except Exception as ex:
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.configura_barra_rolagem",
                                        str(ex))


    def configura_inicial_botoes_text_scroll(self):

        """

            FUNÇÃO UTILIZADA PARA A CONFIGURAÇÃO DE COMPONENTES (BOTÕES, TEXT E SCROLLBAR).

            # Arguments

            # Returns

        """

        try:
            # DESABILITANDO OS BOTÕES DE DECISÃO
            Frame_Atuacao.define_estado_botoes_decisao(self, self.lista_botoes_decisao, "disabled")

            # VINCULANDO ANOTAÇÕES E SCROLL
            Frame_Atuacao.configura_barra_rolagem(self, self.campos_adicionais, "Scrollbar_anotacoes1",
                                                  self.campos_adicionais, "txt_anotacoes_1")
        except Exception as ex:
            print(ex)


    def thread_open(self, funcao, nome, queue_thread, *kw):

        """

            FUNÇÃO GENÉRICA PARA REALIZAR O CARREGAMENTO DE THREAD's.
            CHAMA A THREAD USANDO APENAS O QUEUE COMO ARGUMENTO OU COM A QUEUE E OUTROS ARGUMENTOS (KW).

            # Arguments
                nome             - Required : Nome dado à thread.
                queue_ativa      - Required : Fila de Thread's ativas. (Queue)
                *kw              - Optional : Lista de Argumentos que podem ser utilizados na def chamada pela thread.

            # Returns

        """

        try:
            if len(kw) == 0:
                thread = Thread(target=funcao, name=nome, daemon=False, args=(self, queue_thread))
                thread.start()
            else:
                thread = Thread(target=funcao, name=nome, daemon=False, args=(self, queue_thread, kw))
                thread.start()
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.thread_open",
                                        str(ex))


    def kill_threads(self, queue_ativa):

        """

            MARCA A FILA DE THREAD'S COMO NÃO VAZIAS, OU SEJA, NENHUMA THREAD PODE CONTINUAR.

            # Arguments
                queue_ativa      - Required : Fila de Thread's ativas. (Queue)

            # Returns

        """

        # INTERROMPER TODAS AS THREADS ATIVAS (IS_ALIVE = TRUE)

        try:
            queue_ativa.put(1)
        except Exception as ex:
            print(ex)
            Frame_Atuacao.registra_erro(self, os.getlogin(), "Frame_Atuacao.kill_threads",
                                        str(ex))


    def strfdelta(tdelta, fmt):

        try:
            d = {"D": tdelta.days}
            hours, rem = divmod(tdelta.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            d["H"] = '{:02d}'.format(hours)
            d["M"] = '{:02d}'.format(minutes)
            d["S"] = '{:02d}'.format(seconds)
            return fmt.format(**d)
        except Exception as ex:
            return None


    def timer(self, queue_ativa):

        agora = datetime.datetime.now()

        try:
            while queue_ativa.empty():
                string = datetime.datetime.now() - agora
                self.h = Frame_Atuacao.strfdelta(string, '{H}:{M}:{S}')
                self.lbl_clock.config(text=self.h)
                time.sleep(1)
            self.queue.get()
        except Exception as ex:
            pass


    def execute(self):

        """

            EXECUTA A APLICAÇÃO.

            # Arguments


            # Returns

        """

        # O MAINLOOP MANTÉM O FRAME SENDO UTILIZADO EM LOOP
        self.root.mainloop()

        self.var_size_height = False

        try:
            # O MAINLOOP É FINALIZADO
            self.root.destroy()
        except Exception as ex:
            pass

        # REGISTRANDO O LOG DE SAÍDA
        Frame_Atuacao.registra_log_saida(self, str(self.funcional_usuario))

        try:
            if self.mainmenu == True:
                main_menu.Orquestrador_Main_Menu()
        except Exception as ex:
            pass


def Orquestrador_Atuacao(funcional_usuario = None):

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O GERENCIADOR DE THREAD's
    queue_thread = Queue()

    # INICIANDO O APP
    app_proc = Frame_Atuacao(queue_thread, funcional_usuario)

    # CONFIGURANDO
    app_proc.centraliza_janela()
    app_proc.resizable(True, True)

    # TORNA A TELA RESPONSIVA
    # app_proc.orquestrador_reponsivo()

    # APLICANDO CONFIGURAÇÕES DE BACKGROUND
    # app_proc.call_definicoes_background()

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("Canvas_Logo_Informacoes_Gerais", "Logo_Itau.png", 10, 0)

    # INSERINDO CALENDAR
    app_proc.carrega_img_canvas("Canvas_Calendario_Informacoes_Gerais", "Calendar_Branco.png", 13, 1)

    # INSERINDO IMAGEM NO BOTÃO DE EMAIL
    app_proc.aplica_imagem_objeto("bt_buscar_emails", "buscar_emails.png")

    # INSERINDO IMAGEM NO BOTÃO DE PAUSAR OPERAÇÕES
    app_proc.aplica_imagem_objeto("bt_pausar_op", "pausa_light.png")

    # INSERINDO IMAGEM NOS BOTÕES DE DECISÃO
    app_proc.aplica_imagem_objeto("bt_aprovar", "aprovar-green.png")
    app_proc.aplica_imagem_objeto("bt_devolver", "devolver-red.png")
    app_proc.aplica_imagem_objeto("bt_followup", "followup-yellow.png")
    app_proc.aplica_imagem_objeto("bt_duplicidade", "duplicidade-blue.png")

    # DEFININDO CONFIGURAÇÕES INICIAS DOS COMPONENTES (BOTÕES, TEXT E SCROLLBAR)
    app_proc.configura_inicial_botoes_text_scroll()

    # INICIANDO O SISTEMA DE ATUAÇÃO COM UMA PRÓXIMA OPERAÇÃO
    app_proc.busca_proxima_operacao()

    # EXECUTANDO
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(Orquestrador_Atuacao())

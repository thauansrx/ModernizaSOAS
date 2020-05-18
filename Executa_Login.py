"""

    SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
    FLUXO END-TO-END OPERACIONAL.

    # Arguments
            object                 - Required : User Interface do Login (UI)
        # Returns
            validador_login        - Required : Validador de execução do Login (Boolean)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN) && Rayomi Reis (RAYOMIR)"""
__data_atualizacao__ = "13/05/2020"


import os
import subprocess
import sys
import time
import datetime
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from queue import Queue

from PIL import ImageTk, Image
import pygubu

from Database_Executa_Query import Executa_Query
from Executa_Atuacao import Orquestrador_Atuacao
from main_menu import Orquestrador_Main_Menu

class Frame_Login(object):

    """

        SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
        FLUXO END-TO-END OPERACIONAL.

        # Arguments
            object                 - Required : User Interface do Login. (UI)
        # Returns
            validador_login        - Required : Validador de execução do Login. (Boolean)

    """

    def __init__(self, queue_thread, **kw):

        # INICIALIZANDO O OBJETO TKINTER
        self.root = tk.Tk()
        self.root.title("MODERNIZA - SOAS")

        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file('FRAME_LOGIN.ui')

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            print("Não há o caminho de imagens")

        # 4 - CRIANDO A JANELA PRINCIPAL
        self.mainwindow = builder.get_object('frame_login', self.root)

        # 5 - DEFININDO BANCO DE DADOS - PRODUÇÃO
        try:
            bd_path = os.getcwd() + "\DB_ModernizaSOAS" + "\\" + "DB_MODERNIZASOAS_PRODUCAO.db"
            self.bd_path = bd_path
            builder.add_resource_path(self.bd_path)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        # 6 - DEFININDO BANCO DE DADOS - LOGS
        try:
            bd_path_logs = os.getcwd() + "\DB_ModernizaSOAS" + "\\" + "DB_MODERNIZASOAS_LOGS.db"
            self.bd_path_logs = bd_path_logs
            builder.add_resource_path(self.bd_path_logs)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        # 7 - DEFININDO TIPOS DE QUERY
        self.tipo_query = ["SELECT", "INSERT", "DELETE", "UPDATE", "TRUNCATE"]

        # 8 - API DO WEBDRIVER
        try:
            api_valida_webdriver_path = os.getcwd() + "\API" + "\\" + "Executa_Webdriver.exe"
            self.valida_webdriver = api_valida_webdriver_path
            builder.add_resource_path(self.valida_webdriver)
        except Exception as ex:
            print("Não há o caminho da API de Webdriver")

        # 9 - API DE LOGIN NO MAR2
        try:
            api_mar2_path = os.getcwd() + "\API" + "\\" + "Executa_Mar2.exe"
            self.api_mar2 = api_mar2_path
            builder.add_resource_path(self.api_mar2)
        except Exception as ex:
            print("Não há o caminho da API de login no Mar2")

        # 10 - DEFININDO O GERENCIADOR DE THREAD's
        self.queue = queue_thread

        # 11 - DEFININDO A VARIÁVEL DE VALIDAÇÃO DE LOGIN
        self.validador_login = False

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
            data_hora_atual = Frame_Login.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

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


    def registra_log_acesso(self, funcional_usuario):

        """

           FUNÇÃO QUE REALIZA O REGISTRO DE ACESSO DOS USUÁRIOS NO BANCO DE DADOS DE LOGS.

           # Arguments
               funcional_usuario           - Required : Funcional do usuário. (String)

           # Returns
               validador_orquestrador      - Required : Validador de execução do registro de log. (Boolean)

       """

        try:
            # OBTENDO DATA E HORA ATUAL
            data_hora_atual = Frame_Login.obtem_date_time(self, "%d/%m/%Y %H:%M:%S")

            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path_logs

            # DEFININDO SSQL E PARÂMETROS
            ssql = "INSERT INTO TBL_ACESSO(FUNCIONAL, DT_HR_ENTRADA) VALUES (?, ?)"
            params = (funcional_usuario, data_hora_atual)

            # REALIZANDO A QUERY - INSERT
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[1])
            validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.registra_log_acesso", str(ex))


    def obtem_nivel_acesso(self, funcional_usuario):

        """

           FUNÇÃO QUE REALIZA A OBTENÇÃO DO NIVEL DE ACESSO DO USUÁRIO NO BANCO DE DADOS DE PRODUÇÃO.

           # Arguments
               funcional_usuario           - Required : Funcional do usuário. (String)

           # Returns
               validador_orquestrador      - Required : Validador de execução do select do nivel de acesso. (Boolean)

       """

        try:
            # OBTENDO O CAMINHO DO BD
            caminho_bd = self.bd_path

            # DEFININDO SSQL E PARÂMETROS
            ssql = "SELECT TELAS_ACESSO FROM TBL_NIVEL_ACESSO " \
                   "WHERE ID_NIVEL_ACESSO = (SELECT ID_NIVEL_ACESSO FROM TBL_COLABORADOR " \
                   "WHERE FUNCIONAL = ?)"
            params = (funcional_usuario, )

            # REALIZANDO A QUERY - SELECT
            orquestrador = Executa_Query(caminho_bd, ssql, params, self.tipo_query[0])
            validador_orquestrador, nivel_acesso = orquestrador.Orquestrador_Executa_Query()

            if validador_orquestrador is True:
                print("QUERY EXECUTADA COM SUCESSO")

                if len(nivel_acesso) > 0:
                    return nivel_acesso[0][0]
                else:
                    return None

        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.registra_log_acesso", str(ex))

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
            Frame_Login.registra_erro(os.getlogin(), "Frame_Login.obtem_date_time", str(ex))


    def centraliza_janela(self, tamanho_largura = None, tamanho_altura = None):

        """

            CENTRALIZA E DEFINE O TAMANHO DO FRAME PRINCIPAL SENDO RESPONSIVO EM RELAÇÃO AO TAMANHO DA TELA DO USUÁRIO.

            # Arguments

            # Returns

        """

        try:
            # FUNÇÃO DEFINIDA PARA CENTRALIZAR O FRAME

            janela_root = self.root

            janela_root.update_idletasks()

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
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.insere_img_canvas", str(ex))
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
                validador = Frame_Login.insere_img_canvas(self, objeto, img, altura_imagem, largura_imagem)

                return validador
            except Exception as ex:
                Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.seleciona_img_canvas", str(ex))
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
            Frame_Login.seleciona_img_canvas(self, canvas_logo, imagem, altura_imagem, largura_imagem)
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.carrega_img_canvas", str(ex))


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
            objeto_event.delete(0, tk.END)
        except Exception as ex:
            print(ex)


    def events_entrys(self, objeto_usuario, objeto_senha):

        """

            DEFINE OS EVENTOS DE LIMPEZA DOS CAMPOS USUÁRIO E SENHA APÓS GET FOCUS..
            A LIMPEZA RETIRA OS RÓTULOS PRÉ DEFINIDOS.

            # Arguments
                objeto_usuario             - Required : Objeto para entrada do usuário. (UI)
                objeto_senha               - Required : Objeto para entrada da senha. (UI)

            # Returns

        """

        try:
            # ENTRY USUÁRIO

            # EVENTO APÓS GET FOCUS
            entry_usuario = self.builder.get_object(objeto_usuario)
            entry_usuario.bind("<Button-1>", lambda event, arg=entry_usuario: Frame_Login.clear_search(event, arg))

            # EVENTO APÓS LOST FOCUS
            entry_usuario = self.builder.get_object(objeto_usuario)
            entry_usuario.bind("<FocusOut>", lambda event, arg=entry_usuario: Frame_Login.verifica_pos_lost_focus(event,
                                                                                                                  arg,
                                                                                                                  "Funcional do Usuário"))

            # ENTRY SENHA

            # EVENTO APÓS GET FOCUS
            entry_senha = self.builder.get_object(objeto_senha)
            entry_senha.bind("<Button-1>", lambda event, arg=entry_senha: Frame_Login.clear_search(event, arg))

            # EVENTO APÓS LOST FOCUS
            entry_senha = self.builder.get_object(objeto_senha)
            entry_senha.bind("<FocusOut>",
                             lambda event, arg=entry_senha: Frame_Login.verifica_pos_lost_focus(event,
                                                                                                arg,
                                                                                                "Senha"))
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
                status_botao               - Required : Estado do botão (enabled/disabled). (String)

            # Returns

        """

        try:
            frame_1 = self.builder.get_object(objeto)
            frame_1["state"] = status_botao
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.define_estado_botao", str(ex))


    def altera_componente_configure(self, componente_alteracao, config_alteracao, config_nova):

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

            componente.configure(config_alteracao = config_nova)
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.altera_componente_configure", str(ex))


    def retorna_value_funcao_objeto(self, componente_funcao, config_funcao):

        """

            FUNÇÃO GENÉRICA PARA RETORNAR O VALOR DE UMA CONFIGURAÇÃO DO OBJETO.
            Exemplo: Obter o texto contigo em um objeto (object["text"]).

            # Arguments
                componente_funcao           - Required : Objeto para obter config. (UI)
                config_funcao               - Required : Configuração do Objeto que será obtido. (String)

            # Returns
                componente[config_funcao]   - Required : Valor da configuração. (String)

        """

        try:
            # OBTENDO COMPONENTE
            componente = self.builder.get_object(componente_funcao)

            return componente[config_funcao]
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.retorna_value_funcao_objeto", str(ex))


    def realiza_cadastro(self, caminho_bd, cadastro_usuario, cadastro_senha):

        """

            FUNÇÃO QUE PERMITE O CADASTRO DE LOGINS PARA USUÁRIOS.

            # Arguments
                caminho_bd                  - Required : Caminho do banco de dados. (String)
                cadastro_usuario            - Required : Funcional do Usuário. (String)
                cadastro_usuario            - Required : Senha do Usuário. (String)

            # Returns
                validador_orquestrador      - Required : Validador de execução da função. (Boolean)

        """

        ssql = "INSERT INTO TBL_LOGIN (USUARIO, SENHA) VALUES (?, ?)"
        parametros = (cadastro_usuario, cadastro_senha)

        # INICIANDO A CLASSE
        orquestrador = Executa_Query(caminho_bd, ssql, parametros, self.tipo_query[1])

        # REALIZANDO O ORQUESTRADOR
        validador_orquestrador = orquestrador.Orquestrador_Executa_Query()

        if validador_orquestrador is True:
            print("QUERY EXECUTADA COM SUCESSO")


    def executa_consulta_login_bd(self, caminho_bd, usuario, senha):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO A TBL_LOGIN NO BANCO DE DADOS.

            # Arguments
                caminho_bd                  - Required : Caminho do banco de dados. (String)
                cadastro_usuario            - Required : Funcional do Usuário. (String)
                cadastro_usuario            - Required : Senha do Usuário. (String)

            # Returns
                validador_orquestrador      - Required : Validador de execução da função. (Boolean)
                resultado_consulta          - Required : Resultado do select no banco de dados (List)

        """

        validador = False

        try:

            # EXECUTANDO AÇÃO DO CURSOS
            ssql = "SELECT * FROM TBL_LOGIN WHERE USUARIO = ? AND SENHA = ?"
            parametros = (usuario, senha)

            # INICIANDO A CLASSE
            orquestrador = Executa_Query(caminho_bd, ssql, parametros, self.tipo_query[0])

            # REALIZANDO O ORQUESTRADOR
            validador_orquestrador, resultado_consulta = orquestrador.Orquestrador_Executa_Query()

            return validador_orquestrador, resultado_consulta
        except Exception as ex:
            return None, validador


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


    def executa_consulta_validacao_webdriver(self, caminho_api):

        """

            FUNÇÃO QUE PERMITE A INSTALAÇÃO DO WEBDRIVER MAIS ATUALIZADO NA PASTA PUBLIC.
            O WEBDRIVER É UTILIZADO NA API DE VALIDAÇÃO DO MAR2
            EXECUTA A API VALIDAÇÃO WEBDRIVER.

            # Arguments
                caminho_api                 - Required : Caminho da API - WEBDRIVER. (String)

            # Returns
                validador                   - Required : Validador de execução da função. (Boolean)
                retorno_api                 - Required : Retorno do valor obtido via API. (List)

        """

        validador = False

        try:
            proc = subprocess.Popen([caminho_api], stdout=subprocess.PIPE, encoding='utf8')
            retorno_api = proc.stdout.readline()
            validador = True

            try:
                retorno_api = Frame_Login.replace_variaveis(retorno_api, "\n", "")
            except Exception as ex:
                print(ex)

            return validador, retorno_api
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.executa_consulta_validacao_webdriver", str(ex))
            return None, validador


    def executa_consulta_login_mar2(self, caminho_api, caminho_chrome, usuario, senha):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO A API - MAR2.
            EXECUTA A API MAR2.

            # Arguments
                caminho_api                 - Required : Caminho da API - MAR2. (String)
                cadastro_usuario            - Required : Funcional do Usuário. (String)
                cadastro_usuario            - Required : Senha do Usuário. (String)

            # Returns
                validador                   - Required : Validador de execução da função. (Boolean)
                retorno_api                 - Required : Retorno do valor obtido via API. (List)

        """

        validador = False

        try:
            proc = subprocess.Popen([caminho_api, caminho_chrome, usuario, senha], stdout=subprocess.PIPE, encoding='utf8')
            retorno_api = proc.stdout.readline()
            validador = True

            return validador, retorno_api
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.executa_consulta_login_mar2", str(ex))
            return None, validador


    def valida_consulta_login_bd(self, resultado_consulta):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO AO BD.
            UTILIZA O RESULTADO DA EXECUÇÃO DO BD.

            # Arguments
                resultado_consulta          - Required : Retorno do valor obtido via Banco de Dados. (List)

            # Returns
                validador_retorno_bd        - Required : Validador se o usuário já estava cadastrado. (Boolean)

        """

        validador_retorno_bd = False

        try:
            if len(resultado_consulta) > 0:
                validador_retorno_bd = True
            else:
                validador_retorno_bd = False
            return validador_retorno_bd
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.valida_consulta_login_bd", str(ex))
            return validador_retorno_bd


    def valida_consulta_login_mar2(self, resultado_consulta_mar2):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO A API - MAR2.
            UTILIZA O RESULTADO DA EXECUÇÃO DA API.

            # Arguments
                resultado_consulta_mar2      - Required : Retorno do valor obtido via API. (List)

            # Returns
                validador_retorno_api        - Required : Validador se o usuário e senha procedem com o sistema. (Boolean)

        """

        validador_retorno_api = False

        resultado_consulta = str(resultado_consulta_mar2)

        try:
            if resultado_consulta.find("True")!=-1:
                validador_retorno_api = True
            else:
                validador_retorno_api = False
            return validador_retorno_api
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.valida_consulta_login_mar2", str(ex))
            return validador_retorno_api


    def valida_login(self, usuario, senha):

        # INICIANDO A VARIÁVEL DE VALIDADOR DA EXECUÇÃO DO ORQUESTRADOR (VALIDA_LOGIN).
        validador = False

        if usuario != "" and usuario != "FUNCIONAL DO USUÁRIO":
            if senha != "" and senha != "SENHA":

                # VERIFICANDO SE O BOTÃO ESTÁ COM LABEL - ENTRAR OU NOVO
                if Frame_Login.retorna_value_funcao_objeto(self, "bt_entrar", "text") == "ENTRAR":

                    # REALIZA A CONSULTA NO BANCO DE DADOS
                    # validador, resultado_consulta_login = Frame_Login.executa_consulta_login_bd(self, self.bd_path, usuario, senha)

                    # CHAMANDO A THREAD DA BARRA DE PROGRESSO

                    Frame_Login.thread_open(self, Frame_Login.carrega_bar, "ProgressBar", self.queue)

                    # REALIZA A VALIDAÇÃO DO WEBDRIVER
                    validador, path_chromedriver = Frame_Login.executa_consulta_validacao_webdriver(self, self.valida_webdriver)

                    # REALIZA A CONSULTA NA API - MAR2
                    validador, resultado_consulta_login = Frame_Login.executa_consulta_login_mar2(self, self.api_mar2,
                                                                                                  path_chromedriver, usuario, senha)
                    if validador is True:
                        validador = False

                        # ELIMINANDO A THREAD ATIVA
                        Frame_Login.kill_threads(self, self.queue)

                        # VALIDA O RESULTADO
                        # validador = Frame_Login.valida_consulta_login_bd(self, resultado_consulta_login)

                        # VALIDA O RESULTADO DA API - MAR2
                        validador = Frame_Login.valida_consulta_login_mar2(self, resultado_consulta_login)

                        if validador is True:
                            messagebox.showinfo("MODERNIZA SOAS", "LOGIN REALIZADO COM SUCESSO")

                            # DEFININDO O USUARIO COMO VARIÁVEL GLOBAL DA CLASSE
                            self.usuario = usuario

                            # OBTENDO O NÍVEL DE ACESSO
                            self.nivel_acesso = Frame_Login.obtem_nivel_acesso(self, self.usuario)

                            # CASO RETORNE NONE, O USUÁRIO NAÕ ESTÁ CADASTRADO NO SISTEMA
                            if self.nivel_acesso == None:
                                messagebox.showinfo("MODERNIZA SOAS", "VOCÊ NÃO POSSUI CADASTRO NO SISTEMA \n"
                                                                      "CONTATE A SUA SUPERVISÃO")
                            else:
                                # REALIZANDO O LOG DE ACESSO
                                Frame_Login.registra_log_acesso(self, self.usuario)

                            # FECHANDO O FRAME
                            Frame_Login.fecha_frame(self)

                            self.validador_login = True

                        else:
                            messagebox.showinfo("MODERNIZA SOAS", "USUÁRIO OU SENHA INVÁLIDO")

                            """MsgBox = messagebox.askquestion("MODERNIZA SOAS", "NOVO USUÁRIO\nDESEJA SE CADASTRAR?",
                                                            icon='warning')
                            if MsgBox == 'yes':
                                # BOTÃO DE ENTRAR ALTERA PARA NOVO
                                Frame_Login.altera_componente_texto(self, "bt_entrar", "text", "NOVO")
                            else:
                                messagebox.showinfo("MODERNIZA SOAS", "TENTE LOGAR NOVAMENTE")
                                # BOTÃO DE NOVO ALTERA PARA ENTRAR
                                Frame_Login.altera_componente_texto(self, "bt_entrar", "text", "ENTRAR")"""

                else:
                    Frame_Login.realiza_cadastro(self, self.bd_path, usuario, senha)
                    Frame_Login.fecha_frame(self)
            else:
                messagebox.showinfo("MODERNIZA SOAS", "DIGITE UMA SENHA")
        else:
            messagebox.showinfo("MODERNIZA SOAS", "DIGITE O USUÁRIO")
        # HABILITANDO BOTÃO DE ENTRAR
        Frame_Login.define_estado_botao(self, "bt_entrar", "normal")

        try:
            self.t.join()
        except Exception as ex:
            pass


    def carrega_bar(self, queue_ativa):

        """

            REALIZA O CARREGAMENTO DA BARRA DE PROGRESSO, INDICANDO AO USUÁRIO QUE O PROCESSO DE LOGIN ESTÁ SENDO EXECUTADO.
            A QUEUE CONTROLA A FILA DE THREADS.

            # Arguments
                queue_ativa      - Required : Fila de Thread's ativas. (Queue)

            # Returns

        """

        try:
            self.barVar = self.builder.get_variable("barVar")

            while queue_ativa.empty():
                for t in range(0, 230, 1):
                    self.barVar.set(t)
                    self.root.update_idletasks()
                    time.sleep(0.01)
                self.barVar.set(0)
                self.root.update_idletasks()
            # LIMPANDO A QUEUE, ISSO PERMITE QUE A BARRA DE PROGRESSO SEJA RECARREGADA CASO O LOGIN SEJA INVÁLIDO.
            self.queue.get()
        except Exception as ex:
            pass


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
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.thread_open", str(ex))


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
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.kill_threads", str(ex))


    def bt_entrar_click(self):

        """

            AÇÃO REALIZADA APÓS O CLICK NO BOTÃO DE ENTRAR.
            OBTÉM-SE OS VALORES DIGITADOS NOS CAMPOS DE ENTRY USUÁRIO E ENTRY SENHA.
            CHAMA A VALIDAÇÃO DOS PREENCHIMENTOS E DO LOGIN NO MAR2.

            # Arguments

            # Returns

        """

        try:
            # DESABILITANDO BOTÃO DE ENTRAR
            Frame_Login.define_estado_botao(self, "bt_entrar", "disabled")
        except Exception as ex:
            print(ex)

        try:
            # OBTENDO USUÁRIO
            entry_usuario = self.builder.get_object("entry_usuario")
            value_usuario = entry_usuario.get().upper()
        except Exception as ex:
            print(ex)
            value_usuario = ""

        try:
            # OBTENDO SENHA
            entry_senha = self.builder.get_object("entry_senha")
            value_senha = entry_senha.get().upper()
        except Exception as ex:
            print(ex)
            value_senha = ""

        try:
            # VALIDANDO O LOGIN
            self.t = Thread(target=Frame_Login.valida_login, name="nome", daemon=True, args=(self, value_usuario, value_senha,))
            self.t.start()
        except Exception as ex:
            print(ex)
            Frame_Login.registra_erro(self, os.getlogin(), "Frame_Login.bt_entrar_click", str(ex))


    def execute(self):

        # O MAINLOOP MANTÉM O FRAME SENDO UTILIZADO EM LOOP
        self.root.mainloop()

        try:
            # O MAINLOOP É FINALIZADO
            self.root.destroy()
        except Exception as ex:
            pass

        # VALIDAÇÃO DO LOG DO USUÁRIO
        if self.validador_login == True:

            # VALIDAÇÃO DO NÍVEL DE ACESSO
            if self.nivel_acesso == "ATUACAO":
                Orquestrador_Atuacao(self.usuario)
            elif self.nivel_acesso == "MENU":
                Orquestrador_Main_Menu(self.usuario)
            else:
                Frame_Login.registra_erro(self, self.usuario, "Frame_Login.obtem_nivel_acesso", "sem acesso")


def Orquestrador_Login():

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O GERENCIADOR DE THREAD's
    queue_thread = Queue()

    # INICIANDO O APP
    app_proc = Frame_Login(queue_thread)

    # CONFIGURANDO
    app_proc.centraliza_janela(765, 400)
    app_proc.resizable(False, False)

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("canvas_logo", "moderniza_logo_with_back.png", -35, -150)

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("canvas_bemvindo", "Logo_Login_BemVindo_3.png", 30, 40)

    # DEFININDO EVENTS
    app_proc.events_entrys("entry_usuario", "entry_senha")

    # EXECUTANDO
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(Orquestrador_Login())


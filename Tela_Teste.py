"""

    SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
    FLUXO END-TO-END OPERACIONAL.

    # Arguments
            object                 - Required : User Interface do Login (UI)
        # Returns
            validador_login        - Required : Validador de execução do Login (Boolean)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "30/04/2020"


import os
import subprocess
import sqlite3
import sys
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image
import pygubu

from Database_Executa_Query import Executa_Query

class Frame_Login(object):

    """

        SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
        FLUXO END-TO-END OPERACIONAL.

        # Arguments
            object                 - Required : User Interface do Login. (UI)
        # Returns
            validador_login        - Required : Validador de execução do Login. (Boolean)

    """

    def __init__(self, **kw):

        # INICIALIZANDO O OBJETO TKINTER
        self.root = tk.Tk()
        self.root.title("MODERNIZA - SOAS")

        self.root["bg"] = "blue"

        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file('FRAME_LOGIN - Cópia.ui')

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

        # 5 - DEFININDO BANCO DE DADOS
        try:
            bd_path = os.getcwd() + "\\" + "Database_ModernizaSOAS"
            self.bd_path = bd_path
            builder.add_resource_path(self.bd_path)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        # 6 - DEFININDO TIPOS DE QUERY
        self.tipo_query = ["SELECT", "INSERT", "DELETE", "UPDATE", "TRUNCATE"]

        # 7 - API DE LOGIN NO MAR2
        try:
            api_mar2_path = os.getcwd() + "\API" + "\\" + "Executa_Mar2.exe"
            self.api_mar2 = api_mar2_path
            builder.add_resource_path(self.api_mar2)
        except Exception as ex:
            print("Não há o caminho da API de login no Mar2")

        builder.connect_callbacks(self)


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
            self.root.destroy()
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

            DEFINE OS EVENTOS DE LIMPEZA DOS CAMPOS USUÁRIO E SENHA APÓS CLIQUE DO USUÁRIO.
            A LIMPEZA RETIRA OS RÓTULOS PRÉ DEFINIDOS.

            # Arguments
                objeto_usuario             - Required : Objeto para entrada do usuário. (UI)
                objeto_senha               - Required : Objeto para entrada da senha. (UI)

            # Returns

        """

        try:
            # ENTRY USUÁRIO
            entry_usuario = self.builder.get_object(objeto_usuario)
            entry_usuario.bind("<Button-1>", lambda event, arg=entry_usuario: Frame_Login.clear_search(event, arg))

            # ENTRY SENHA
            entry_senha = self.builder.get_object(objeto_senha)
            entry_senha.bind("<Button-1>", lambda event, arg=entry_senha: Frame_Login.clear_search(event, arg))
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


    def retorna_value_funcao_objeto(self, componente_funcao, config_funcao):

        """

            FUNÇÃO GEMÉRICA PARA RETORNAR O VALOR DE UMA CONFIGURAÇÃO DO OBJETO.
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


    def executa_consulta_login_mar2(self, caminho_api, usuario, senha):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO A API - MAR2.
            EXECUTA A API.

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
            proc = subprocess.Popen([caminho_api, usuario, senha], stdout=subprocess.PIPE)
            retorno_api = proc.stdout.readline()
            validador = True

            return validador, retorno_api
        except Exception as ex:
            print(ex)
            return None, validador


    def valida_consulta_login_bd(self, resultado_consulta):

        """

            FUNÇÃO QUE PERMITE A VALIDAÇÃO DO USUÁRIO EM RELAÇÃO A API - MAR2.
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
            return validador_retorno_api


    def valida_login(self, usuario, senha):

        validador = False

        if usuario != "" and usuario != "FUNCIONAL DO USUÁRIO":
            if senha != "" and senha != "SENHA":

                # VERIFICANDO SE O BOTÃO ESTÁ COM LABEL - ENTRAR OU NOVO
                if Frame_Login.retorna_value_funcao_objeto(self, "bt_entrar", "text") == "ENTRAR":

                    # REALIZA A CONSULTA NO BANCO DE DADOS
                    # validador, resultado_consulta_login = Frame_Login.executa_consulta_login_bd(self, self.bd_path, usuario, senha)

                    # REALIZA A CONSULTA NA API - MAR2
                    validador, resultado_consulta_login = Frame_Login.executa_consulta_login_mar2(self, self.api_mar2, usuario, senha)
                    if validador is True:
                        validador = False

                        # VALIDA O RESULTADO
                        # validador = Frame_Login.valida_consulta_login_bd(self, resultado_consulta_login)

                        # VALIDA O RESULTADO DA API - MAR2
                        validador = Frame_Login.valida_consulta_login_mar2(self, resultado_consulta_login)

                        if validador is True:
                            messagebox.showinfo("MODERNIZA SOAS", "LOGIN REALIZADO COM SUCESSO")
                            Frame_Login.fecha_frame(self)
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
                    Frame_Login.realiza_cadastro(self.bd_path, usuario, senha)
                    Frame_Login.fecha_frame(self)
            else:
                messagebox.showinfo("MODERNIZA SOAS", "DIGITE UMA SENHA")
        else:
            messagebox.showinfo("MODERNIZA SOAS", "DIGITE O USUÁRIO")

    def carega_bar(self):

        for t in range(0, 100, 20):
            self.barVar.set(t)
            print(t)
            self.root.update_idletasks()
            time.sleep(2)
            self.barVar.set(100)
        print('Fim...')


    def bt_entrar_click(self):

        """global progress_bar, barVar
        self.progress_bar = self.builder.get_object("Progressbar_Entrar")
        self.barVar = tk.DoubleVar()

        self.barVar.set(0)

        Frame_Login.carega_bar(self)"""

        # OBTENDO USUÁRIO
        entry_usuario = self.builder.get_object("entry_usuario")
        value_usuario = entry_usuario.get().upper()

        # OBTENDO SENHA
        entry_senha = self.builder.get_object("entry_senha")
        value_senha = entry_senha.get().upper()

        # VALIDANDO
        Frame_Login.valida_login(self, value_usuario, value_senha)


    def execute(self):

        self.root.mainloop()


def main(args):

    # INICIANDO O APP
    app_proc = Frame_Login()

    # CONFIGURANDO
    app_proc.centraliza_janela(765, 400)
    app_proc.resizable(False, False)

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("canvas_logo", "Logo_Login_Estrela.png", 90, 70)

    # INSERINDO LOGO
    app_proc.carrega_img_canvas("canvas_bemvindo", "Logo_Login_BemVindo.png", 30, 40)

    # DEFININDO EVENTS
    app_proc.events_entrys("entry_usuario", "entry_senha")

    # EXECUTANDO
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))


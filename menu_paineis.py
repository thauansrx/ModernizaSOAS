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

import main_menu
import Executa_Atuacao

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class Frame_menu_paineis(object):

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
        builder.add_from_file(os.path.join(CURRENT_DIR, 'menu_paineis.ui'))
        self.root = builder.get_object('main')
        self.root.title("Menu Paineis")
        self.root.state('zoomed')

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            pass

        # 4 - DEFININDO AS VARIAVEIS DE AMBIENTE PARA TRANSIÇÃO DE TELA
        self.mainmenu = False

        # 9 - DEFININDO O GERENCIADOR DE THREAD's
        self.queue = queue_thread

        # USUÁRIO LOGADO
        self.funcional_usuario = funcional_usuario

        builder.connect_callbacks(self)

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
                validador = Frame_menu_paineis.insere_img_canvas(self, objeto, img, altura_imagem, largura_imagem)

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
            Frame_menu_paineis.seleciona_img_canvas(self, canvas_logo, imagem, altura_imagem, largura_imagem)
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

    def bt_voltar_main_menu(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O BOTÃO
            RETORNA PARA O MENU PRINCIPAL.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        self.mainmenu = True
        Frame_menu_paineis.fecha_frame(self)

    def bt_acessa_painel_operações(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O BOTÃO
            ABRE UM PAINEL DE OPERAÇÕES PARA A ATUAÇÃO DOS OPERADORES.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        self.painel_operações = True
        Frame_menu_paineis.fecha_frame(self)

    def bt_painel_histórico(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O BOTÃO
            ABRE UMA PAINEL PARA INFORMAR O HISTORICO DE OPERAÇÕES.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


    def bt_painel_skills(self):

        """

            FUNÇÃO APÓS O CLICK SOBRE O BOTÃO
            ABRE UMA PAINEL DE SKILLS DE CADA OPERADOR.
            ESSA FUNÇÃO ESTÁ HABILITADA APENAS PARA ALGUNS USUÁRIOS.

            # Arguments

            # Returns

        """

        messagebox.showinfo("MODERNIZA SOAS", "FUNÇÃO EM CONSTRUÇÃO")


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

    def imagem(self, label_recebe_imagem, imagem):

        """

            APLICA UMA IMAGEM A UM LABEL.

            # Arguments


            # Returns

        """

        try:
            # OBTENDO O LABEL
            img_label = self.builder.get_object(label_recebe_imagem, self.root)

            # ABRINDO A IMAGEM USANDO PILs
            image = Image.open(self.img_path + "\\" + imagem)
            photo = ImageTk.PhotoImage(image, master=self.root)

            # APLICANDO A IMAGEM
            img_label.new_image = photo
            img_label.config(image = img_label.new_image)
        except Exception as ex:
            print(ex)


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

        try:
            if self.mainmenu == True:
                main_menu.Orquestrador_Main_Menu()
            elif self.painel_operações == True:
                Executa_Atuacao.Orquestrador_Atuacao(self.funcional_usuario)

        except Exception as ex:
            pass


def Orquestrador_Menu_Paineis(funcional_usuario = None):

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O GERENCIADOR DE THREAD's
    queue_thread = Queue()

    # INICIANDO O APP
    app_proc = Frame_menu_paineis(queue_thread, funcional_usuario)

    # CONFIGURANDO
    app_proc.centraliza_janela()

    # INSERINDO FUNDO
    app_proc.carrega_img_canvas("fundo", "fundo_paineis.jpg", 0, 0)

    # APLICANDO A IMAGEM NOS BOTÕES
    app_proc.imagem("Bt_historico", "menu_historico.png")
    app_proc.imagem("Bt_operações", "menu_operações.png")
    app_proc.imagem("Bt_skill", "menu_skill.png")
    app_proc.imagem("Bt_voltar", "voltar_bt.png")


    # EXECUTANDO
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(Orquestrador_Menu_Paineis())

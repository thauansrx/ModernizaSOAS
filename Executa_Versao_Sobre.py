"""

    SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
    FLUXO END-TO-END OPERACIONAL.
    ESSE ARQUIVO REFERE-SE À ETAPA DO SOBRE VERSÃO.

    # Arguments
            object                       - Required : User Interface do Login (UI)
        # Returns

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN) && Rayomi Reis"""
__data_atualizacao__ = "10/05/2020"

import os
import sys
import tkinter as tk

from PIL import ImageTk, Image
import pygubu

from Database_Executa_Query import Executa_Query

class Frame_Sobre_Versao(object):

    """

        SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
        FLUXO END-TO-END OPERACIONAL.
        ESSE ARQUIVO REFERE-SE À ETAPA DO SOBRE VERSÃO.

        # Arguments
            object                 - Required : User Interface do Login. (UI)
        # Returns

    """


    def __init__(self, **kw):

        # INICIALIZANDO O OBJETO TKINTER
        self.root = tk.Tk()
        self.root.title("MODERNIZA - SOAS")

        # 1 - CRIANDO O BUILDER
        self.builder = builder = pygubu.Builder()

        # 2 - LENDO O ARQUIVO UI
        builder.add_from_file('FRAME_SOBRE_VERSAO.ui')

        # 3 - CARREGANDO O CAMINHO DE IMAGENS
        try:
            img_path = os.getcwd() + r"\Imagens"
            img_path = os.path.abspath(img_path)
            self.img_path = img_path
            builder.add_resource_path(self.img_path)
        except Exception as ex:
            print("Não há o caminho de imagens")

        # 4 - CRIANDO AS JANELA PRINCIPAIS
        self.mainwindow = builder.get_object('Frame_Sobre_Versao', self.root)

        # 5 - DEFININDO BANCO DE DADOS
        try:
            bd_path = os.getcwd() + "\DB_ModernizaSOAS" + "\\" + "DB_MODERNIZASOAS.db"
            self.bd_path = bd_path
            builder.add_resource_path(self.bd_path)
        except Exception as ex:
            print("Não há o caminho do banco de dados")

        builder.connect_callbacks(self)


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


    def obtem_versao_atual(self):

        """

            REALIZA A QUERY NO BANCO DE DADOS, OBTENDO A VERSÃO ATUAL DO SISTEMA

            # Arguments


            # Returns
            versao_atual                  - Required : Versão atual do sistema. (String)

        """


        versao_atual = "1.0"

        try:
            versao_atual_sistema = "VERSÃO: " + versao_atual
        except Exception as ex:
            print(ex)
            versao_atual_sistema = versao_atual

        return versao_atual_sistema


    def visualiza_versao_atual(self, label_versao_atual):

        """

            MOSTRA AO USUÁRIO A VERSÃO ATUAL DO SISTEMA

            # Arguments


            # Returns

        """

        try:
            # OBTENDO A VERSÃO ATUAL NO BANCO DE DADOS
            versao_atual = Frame_Sobre_Versao.obtem_versao_atual(self.mainwindow)

            # OBTENDO O LABEL
            label_text = self.builder.get_object(label_versao_atual)

            # APLICANDO A VERSÃO ATUAL NO LABEL
            label_text["text"] = versao_atual
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

        try:
            # O MAINLOOP É FINALIZADO
            self.root.destroy()
        except Exception as ex:
            pass


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


def Orquestrador_Sobre_Versao():

    """

        ORQUESTRADOR DE EXECUÇÃO DO CÓDIGO.

        # Arguments

        # Returns

    """

    # INICIANDO O APP
    app_proc = Frame_Sobre_Versao()

    # CONFIGURANDO
    app_proc.centraliza_janela(400, 350)
    app_proc.resizable(True, True)

    # OBTENDO A VERSÃO ATUAL
    app_proc.visualiza_versao_atual("Label_Sobre_Versao_Versao")

    # APLICANDO A IMAGEM AO LABEL
    app_proc.aplica_imagem_objeto("Label_Sobre_Versao_Logo", "Logo_Moderniza_SOAS.png")

    # EXECUTANDO
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(Orquestrador_Sobre_Versao())

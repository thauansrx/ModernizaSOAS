"""

    SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
    FLUXO END-TO-END OPERACIONAL.
    ESSE ARQUIVO REFERE-SE À API DE ENVIO DE EMAIL.

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

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "14/05/2020"

import os
import sys
import win32com.client as win32


class Executa_Envia_Email_Teplate():

    """

        SISTEMA PARA ATUAÇÃO EM OPERAÇÕES - SOAS.
        FLUXO END-TO-END OPERACIONAL.
        ESSE ARQUIVO REFERE-SE À API DE ENVIO DE EMAIL.

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

    """


    def __init__(self, email_envio, destinatarios_input,
                 assunto_input, data_operacao_input, produto_input,
                 agencia_input, conta_input, pn_input, status_input,
                 texto_email, texto_devolucao_input, caminho_template_input):

        self.email_envio = email_envio
        self.assunto = assunto_input
        self.destinatarios = destinatarios_input
        self.data_operacao = data_operacao_input
        self.produto = produto_input
        self.agencia = agencia_input
        self.conta = conta_input
        self.pn = pn_input
        self.status = status_input
        self.texto = texto_email
        self.texto_devolucao = texto_devolucao_input
        self.caminho_template = caminho_template_input


    @staticmethod
    def instancia_outlok():

        """

            OBTÉM UMA INSTÂNCIA DO OUTLOOK APPLICATION.
            RETORNA O OBJETO OUTLOOK.

            # Arguments

            # Returns
                outlook                 - Required : Instância do outlook application. (Outlook Application)

        """

        validador_execucao = False

        try:
            outlook = win32.Dispatch('outlook.application')
            validador_execucao = True
        except Exception as ex:
            outlook = None

        return validador_execucao, outlook


    def instancia_template(self, outlook, caminho_template):

        """

            OBTÉM UMA INSTÂNCIA DO TEMPLATE (OFT).
            RETORNA O EMAIL JÁ COM TEMPLATE INSTANCIADO.

            # Arguments
                outlook                 - Required : Instância do outlook application. (Outlook Application)
                caminho_template        - Required : Caminho do template. (String)

            # Returns
                mail                    - Required : Email com template instanciado. (Outlook Mail)

        """

        validador_execucao = False

        try:
            mail = outlook.CreateItemFromTemplate(caminho_template)
            validador_execucao = True
        except Exception as ex:
            mail = None

        return validador_execucao, mail


    @staticmethod
    def envia_email(self, email, caixa_envio, lista_para_email,
                    assunto_email, data_operacao_email, produto_email,
                    status_email, agencia_email, conta_email, pn_email,
                    texto_email, texto_devolucao_email):

        """

            REALIZA O DISPLAY DO EMAIL PARA O USUÁRIO, REALIZANDO AS SUBSTITUIÇÕES NO TEMPLATE.
            INSERE OS DESTINÁRIOS E O ASSUNTO DE ENVIO.

            # Arguments
                email                        - Required : Instância do outlook application. (Outlook Application)
                caixa_envio                  - Optional : Cakixa de envio do email. (String)
                lista_para_email             - Optional : Lista de emails destinatários. (String)
                assunto_email                - Optional : Assunto para envio no email (String)
                data_operacao_email          - Optional : Data para envio no email (String)
                produto_email                - Optional : Produto para envio no email (String)
                status_email                 - Optional : Status da operação para envio no email (String)
                agencia_email                - Optional : Agencia para envio no email (String)
                conta_email                  - Optional : Conta para envio no email (String)
                pn_email                     - Optional : PN para envio no email (String)
                texto_email                  - Optional : Texto de corpo para envio no email (String)
                texto_devolucao              - Optional : Texto de devolução no email (String)

            # Returns
                validador_execucao           - Required : Email com template instanciado. (Outlook Mail)

        """

        validador_execucao = False

        try:
            # INSERINDO A CAIXA DE ENVIO DO EMAIL
            email.SendOnBehalfName = caixa_envio
        except Exception as ex:
            pass

        try:
            # INSERINDO OS DESTINATÁRIOS
            email.To = lista_para_email
        except Exception as ex:
            pass

        try:
            # INSERINDO O ASSUNTO
            email.Subject = assunto_email
        except Exception as ex:
            pass

        try:
            # REALIZANDO OS REPLACES
            email.HTMLBody = email.HTMLBody.replace("DATA_INPUT", str(data_operacao_email))
            email.HTMLBody = email.HTMLBody.replace("PRODUTO_INPUT", str(produto_email))
            email.HTMLBody = email.HTMLBody.replace("STATUS_INPUT", str(status_email))
            email.HTMLBody = email.HTMLBody.replace("AGENCIA_INPUT", str(agencia_email))
            email.HTMLBody = email.HTMLBody.replace("CONTA_INPUT", str(conta_email))
            email.HTMLBody = email.HTMLBody.replace("PN_INPUT", str(pn_email))
            email.HTMLBody = email.HTMLBody.replace("DEV_INPUT", str(texto_devolucao_email))
        except Exception as ex:
            pass

        try:
            email.Display()
            validador_execucao = True
        except Exception as ex:
            print(ex)

        return validador_execucao


    def orquestrador_envia_email(self):

        # INICIANDO O VALIDADOR DE EXECUÇÃO DO ORQUESTRADOR
        validacao_execucao = False

        # INSTANCIANDO O OUTLOOK
        validacao_execucao, outlook = Executa_Envia_Email_Teplate.instancia_outlok()

        if validacao_execucao is True:
            validacao_execucao = False

            # INSTANCIANDO O TEMPLATE
            validacao_execucao, mail = Executa_Envia_Email_Teplate.instancia_template(self, outlook, self.caminho_template)

            if validacao_execucao is True:
                validacao_execucao = False
                validacao_execucao = Executa_Envia_Email_Teplate.envia_email(self, mail, self.email_envio,
                                                                             self.destinatarios, self.assunto,
                                                                             self.data_operacao, self.produto,
                                                                             self.status, self.agencia,
                                                                             self.conta, self.pn, self.texto,
                                                                             self.texto_devolucao)

                return validacao_execucao

if __name__ == "__main__":

    try:
        email_envio = sys.argv[1]
        destinatarios = sys.argv[2]
        assunto = sys.argv[3]
        data_operacao = sys.argv[4]
        produto = sys.argv[5]
        agencia = sys.argv[6]
        conta = sys.argv[7]
        pn = sys.argv[8]
        status = sys.argv[9]
        texto_email = sys.argv[10]
        texto_devolucao = sys.argv[11]
        caminho_template = sys.argv[12]

        orquestrador_email = Executa_Envia_Email_Teplate(email_envio, destinatarios,
                                                         assunto, data_operacao,
                                                         produto, agencia,
                                                         conta, pn, status, texto_email,
                                                         texto_devolucao, caminho_template)
        validador_email = orquestrador_email.orquestrador_envia_email()
        print(validador_email)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <string_to_reverse>")






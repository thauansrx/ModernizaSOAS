"""

    MICROSERVIÇO RESPONSÁVEL POR TODAS AS INTERAÇÕES COM O BANCO DE DADOS.
    SELECT | INSERT | DELETE | UPDATE | TRUNCATE

    # Arguments
        caminho_banco_dados            - Required : Caminho do Banco de Dados. (String)
        ssql                           - Required : Query a ser executada. (String)
        parametros                     - Required : Parâmetros da query. (Tuple)
        tipo_query                     - Required : Tipo da query a ser executada. (String)
    # Returns
        validador_query                - Required : Validador de execução da Query. (Boolean)

"""


__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "01/05/2020"


import os
import sqlite3

class Executa_Query():

    """

        MICROSERVIÇO RESPONSÁVEL POR TODAS AS INTERAÇÕES COM O BANCO DE DADOS.
        SELECT | INSERT | DELETE | UPDATE | TRUNCATE

        # Arguments
            caminho_banco_dados            - Required : Caminho do Banco de Dados. (String)
            ssql                           - Required : Query a ser executada. (String)
            parametros                     - Required : Parâmetros da query. (Tuple)
            tipo_query                     - Required : Tipo da query a ser executada. (String)
        # Returns
            validador_query                - Required : Validador de execução da Query. (Boolean)

    """

    def __init__(self, caminho_banco_dados, ssql, parametros, tipo_query, **kw):

        self.bd = caminho_banco_dados
        self.query = ssql
        self.parametros = parametros
        self.tipo_acao_query = tipo_query


    @staticmethod
    def abre_conexao(caminho_bd):

        """

            ABRE A CONEXÃO COM O BANCO DE DADOS.
            REALIZA A TENTATIVA DE CONEXÃO COM MÁXIMO DE 10 TENTATIVAS (TIMEOUT).

            # Arguments
                caminho_bd            - Required : Caminho do Banco de Dados. (String)

            # Returns
                conn                  - Required : Conexão aberta. (conn)
                validador_query       - Required : Validador de execução da Query. (Boolean)

        """

        validador = False
        tentativas = 0

        # INICIA A CONEXÃO COM O BANCO DE DADOS
        while validador is False or tentativas <= 10:
            try:
                conn = sqlite3.connect(caminho_bd)
                validador = True
                return conn, validador
            except Exception as ex:
                print(ex)
                tentativas += 1
                return None, validador


    @staticmethod
    def fecha_conexao(conn):

        """

            FECHA A CONEXÃO COM O BANCO DE DADOS.

            # Arguments
                conn                  - Required : Conexão aberta. (conn)

            # Returns

        """

        try:
            conn.close()
        except Exception as ex:
            print(ex)


    @staticmethod
    def inicia_cursor(conn):

        """

            INICIA UM CURSOR PARA ITERAÇÃO COM O BANCO DE DADOS.

            # Arguments
                conn                  - Required : Conexão aberta. (conn)

            # Returns
                cursor                - Required : Cursos iniciado. (cursor)

        """

        try:
            # DEFININDO UM CURSOR
            cursor = conn.cursor()
            return cursor
        except Exception as ex:
            print(ex)
            return None


    @staticmethod
    def executa_query_insert_delete_update_truncate(conn, ssql, parametros):

        """

            EXECUTA AS QUERYS DE TIPO: INSERT | DELETE | UPDATE | TRUNCATE

            # Arguments
                conn                  - Required : Conexão aberta. (conn)
                ssql                  - Required : Query a ser executada. (String)
                parametros            - Required : Parâmetros da query. (Tuple)

            # Returns
                validador_query       - Required : Validador de execução da Query. (Boolean)

        """

        cursor = Executa_Query.inicia_cursor(conn)

        validador = False

        try:
            # REALIZANDO A QUERY
            cursor.execute(ssql, parametros)
            conn.commit()
            validador = True
            return validador
        except Exception as ex:
            print(ex)
            return validador


    @staticmethod
    def executa_query_select(conn, ssql, parametros):

        """

            EXECUTA AS QUERYS DE TIPO: SELECT

            # Arguments
                conn                  - Required : Conexão aberta. (conn)
                ssql                  - Required : Query a ser executada. (String)
                parametros            - Required : Parâmetros da query. (Tuple)

            # Returns
                validador_query       - Required : Validador de execução da Query. (Boolean)

        """

        cursor = Executa_Query.inicia_cursor(conn)

        validador = False

        try:
            # REALIZANDO A QUERY
            cursor.execute(ssql, parametros)
            conn.commit()
            validador = True
            return validador, cursor.fetchall()
        except Exception as ex:
            print(ex)
            return validador


    def Orquestrador_Executa_Query(self):

        validador = False

        # INICIANDO A CONEXÃO COM O BANCO DE DADOS
        conn, validador = Executa_Query.abre_conexao(self.bd)

        if validador is True:
            # VALIDANDO O TIPO DE QUERY A SER EXECUTADA
            if self.tipo_acao_query == "INSERT" or self.tipo_acao_query == "UPDATE" or self.tipo_acao_query == "DELETE" or self.tipo_acao_query == "TRUNCATE":
                # EXECUTANDO QUERY INSERT / UPDATE / DELETE
                validador = Executa_Query.executa_query_insert_delete_update_truncate(conn, self.query, self.parametros)
                Executa_Query.fecha_conexao(conn)
                return validador
            elif self.tipo_acao_query == "SELECT":
                # EXECUTANDO QUERY SELECT
                validador, resultado_query = Executa_Query.executa_query_select(conn, self.query, self.parametros)
                Executa_Query.fecha_conexao(conn)
                return validador, resultado_query
            else:
                Executa_Query.fecha_conexao(conn)
                return validador

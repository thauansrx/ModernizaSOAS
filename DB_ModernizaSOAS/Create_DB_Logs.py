import sqlite3
import os

# OBTENDO O USUÁRIO
user = os.getlogin()

# OBTENDO O CAMINHO DO BD
caminho_db = os.getcwd()
nome_db = 'DB_MODERNIZASOAS_LOGS'

caminho_completo_bd = caminho_db + '\\' + nome_db + '.db'

conn = sqlite3.connect(caminho_completo_bd)

cursor = conn.cursor()

# CRIANDO A TBL_ACESSO
sql_create_tbl_acesso = """
CREATE TABLE IF NOT EXISTS TBL_ACESSO (ID_ACESSO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        FUNCIONAL TEXT,
                                        DT_HR_ENTRADA TEXT,
                                        DT_HR_SAIDA TEXT);
"""
cursor.execute(sql_create_tbl_acesso)

# CRIANDO A TBL_PAUSA
sql_create_tbl_pausa = """
CREATE TABLE IF NOT EXISTS TBL_PAUSA (ID_PAUSA INTEGER PRIMARY KEY AUTOINCREMENT,
                                        FUNCIONAL TEXT,
                                        DT_HR_INICIO TEXT,
                                        DT_HR_FINAL TEXT, 
                                        PAUSA_EM_OPERACAO INTEGER);
"""
cursor.execute(sql_create_tbl_pausa)

# CRIANDO A TBL_LOGS_ACAO
sql_create_tbl_logs_acao = """
CREATE TABLE IF NOT EXISTS TBL_LOGS_ACAO (ID_ACAO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        FUNCIONAL TEXT,
                                        DT_HR_ACAO TEXT,
                                        LOCAL_ACAO TEXT, 
                                        ACAO_REALIZADA TEXT);
"""
cursor.execute(sql_create_tbl_logs_acao)

# CRIANDO A TBL_LOGS_ERRO
sql_create_tbl_logs_erro = """
CREATE TABLE IF NOT EXISTS TBL_LOGS_ERRO (ID_ERRO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        FUNCIONAL TEXT,
                                        DT_HR_ERRO TEXT,
                                        LOCAL_ERRO TEXT, 
                                        ACAO_ERRO TEXT);
"""
cursor.execute(sql_create_tbl_logs_erro)
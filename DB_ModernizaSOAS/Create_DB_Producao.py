import sqlite3
import os

# OBTENDO O USUÁRIO
user = os.getlogin()

# OBTENDO O CAMINHO DO BD
caminho_db = os.getcwd()
nome_db = 'DB_MODERNIZASOAS_PRODUCAO'

caminho_completo_bd = caminho_db + '\\' + nome_db + '.db'

conn = sqlite3.connect(caminho_completo_bd)

cursor = conn.cursor()
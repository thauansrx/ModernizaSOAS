---**************************************
---
---         SQL CREATE
---
---**************************************

--- ESTRUTURA DE ACESSO 
CREATE TABLE IF NOT EXISTS TBL_ACESSO (ID_ACESSO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        RACF TEXT,
                                        FUNCIONAL TEXT,
                                        DT_HR_ENTRADA TEXT,
                                        TIPO_ENTRADA TEXT,
                                        DT_HR_SAIDA TEXT);    

--- ESTRUTURA DA OPERACAO 

CREATE TABLE IF NOT EXISTS TBL_CARGO (ID_CARGO INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        CARGO TEXT NOT NULL);
                                        
CREATE TABLE IF NOT EXISTS TBL_PRIORIDADE (ID_PRIORIDADE INTEGER PRIMARY KEY AUTOINCREMENT,
                                        NIVEL_PRIORIDADE INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS TBL_PROCESSO (ID_PROCESSO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        NOME_PROCESSO TEXT NOT NULL,
                                        ESTEIRA_PROCESSO NOT NULL);

CREATE TABLE IF NOT EXISTS TBL_SLA (ID_SLA INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        SLA TEXT NOT NULL);
 
CREATE TABLE IF NOT EXISTS TBL_PONDERADOR (ID_PONDERADOR INTEGER PRIMARY KEY AUTOINCREMENT,
                                        PONDERADOR REAL NOT NULL);
        
CREATE TABLE IF NOT EXISTS TBL_PRODUTO (ID_PRODUTO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PROCESSO INTEGER NOT NULL,
                                        ID_PONDERADOR INTEGER NOT NULL,
                                        ID_SLA INTEGER NOT NULL,
                                        NOME_PRODUTO TEXT NOT NULL,
                                        INFOS_NECESSARIAS TEXT,
                                        FOREIGN KEY(ID_PROCESSO) REFERENCES TBL_PROCESSO(ID_PROCESSO),
                                        FOREIGN KEY(ID_PONDERADOR) REFERENCES TBL_PONDERADOR(ID_PONDERADOR),
                                        FOREIGN KEY(ID_SLA) REFERENCES TBL_SLA(ID_SLA));

CREATE TABLE IF NOT EXISTS TBL_PRODUTO_PONDERADOR (ID_PRODUTO_PONDERADOR INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PRODUTO INTEGER NOT NULL,
                                        ID_PONDERADOR INTEGER NOT NULL,
                                        DT_VIGENCIA TEXT,
                                        FOREIGN KEY(ID_PRODUTO) REFERENCES TBL_PRODUTO(ID_PRODUTO),
                                        FOREIGN KEY(ID_PONDERADOR) REFERENCES TBL_PONDERADOR(ID_PONDERADOR));

CREATE TABLE IF NOT EXISTS TBL_PRODUTO_SLA (ID_PRODUTO_SLA INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PRODUTO INTEGER NOT NULL,
                                        ID_SLA INTEGER NOT NULL,
                                        DT_VIGENCIA TEXT,
                                        FOREIGN KEY(ID_PRODUTO) REFERENCES TBL_PRODUTO(ID_PRODUTO),
                                        FOREIGN KEY(ID_SLA) REFERENCES TBL_SLA(ID_SLA));

CREATE TABLE IF NOT EXISTS TBL_SKILL (ID_SKILL INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PROCESSO INTEGER NOT NULL, 
                                        ID_PRODUTO INTEGER NOT NULL,
                                        ID_COLABORADOR INTEGER NOT NULL, 
                                        SKILL TEXT NOT NULL, 
                                        FOREIGN KEY(ID_PROCESSO) REFERENCES TBL_PROCESSO(ID_PROCESSO)
                                        FOREIGN KEY(ID_PRODUTO) REFERENCES TBL_PRODUTO(ID_PRODUTO)
                                        FOREIGN KEY(ID_COLABORADOR) REFERENCES TBL_COLABORADOR(ID_COLABORADOR));

CREATE TABLE IF NOT EXISTS TBL_NIVEL_ACESSO (ID_NIVEL_ACESSO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PROCESSO INTEGER NOT NULL, 
                                        ID_PRODUTO INTEGER NOT NULL,
                                        NIVEL_ACESSO TEXT NOT NULL, 
                                        FOREIGN KEY(ID_PROCESSO) REFERENCES TBL_PROCESSO(ID_PROCESSO)
                                        FOREIGN KEY(ID_PRODUTO) REFERENCES TBL_PRODUTO(ID_PRODUTO));


CREATE TABLE IF NOT EXISTS TBL_COLABORADOR (ID_COLABORADOR INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_CARGO INTEGER NOT NULL,
                                        ID_NIVEL_ACESSO INTEGER NOT NULL,
                                        RACF TEXT NOT NULL,
                                        FUNCIONAL TEXT,
                                        NOME TEXT,
                                        ATIVO INTEGER,
                                        HIERARQUIA TEXT,
                                        FOREIGN KEY(ID_CARGO) REFERENCES TBL_CARGO(ID_CARGO),
                                        FOREIGN KEY(ID_NIVEL_ACESSO) REFERENCES TBL_NIVEL_ACESSO(ID_NIVEL_ACESSO));                    

CREATE TABLE IF NOT EXISTS TBL_ANALISE (ID_ANALISE INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_PRODUTO INTEGER NOT NULL,
                                        ID_PROCESSO INTEGER NOT NULL,
                                        ID_COLABORADOR INTEGER NOT NULL,
                                        ID_PRIORIDADE INTEGER,
                                        DT_RECEBIMENTO TEXT NOT NULL,
                                        HR_RECEBIMENTO TEXT,
                                        DT_INCLUSAO TEXT NOT NULL,
                                        HR_INCLUSAO TEXT,
                                        SEQUENCIA_ATUAL INTEGER,
                                        FIM_ATUACAO INTEGER,
                                        INFOS_COMPLEMENTARES TEXT,
                                        FOREIGN KEY(ID_PRODUTO) REFERENCES TBL_PRODUTO(ID_PRODUTO),
                                        FOREIGN KEY(ID_PROCESSO) REFERENCES TBL_PROCESSO(ID_PROCESSO),
                                        FOREIGN KEY(ID_COLABORADOR) REFERENCES TBL_COLABORADOR(ID_COLABORADOR),
                                        FOREIGN KEY(ID_PRIORIDADE) REFERENCES TBL_PRIORIDADE(ID_PRIORIDADE));
                        
CREATE TABLE IF NOT EXISTS TBL_ATUACAO (ID_ATUACAO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_ANALISE INTEGER NOT NULL,
                                        DT_INICIO TEXT NOT NULL,
                                        HR_INICIO TEXT,
                                        DT_ENCERRAMENTO TEXT NOT NULL,
                                        HR_ENCERRAMENTO TEXT,
                                        FOREIGN KEY(ID_ANALISE) REFERENCES TBL_ANALISE(ID_ANALISE));

--- ESTRUTURA DOS DADOS DA VIEW 
CREATE TABLE IF NOT EXISTS TBL_TIPO_DADO_VIEW (ID_DADO INTEGER PRIMARY KEY AUTOINCREMENT,
                                        TIPO_DADO TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS TBL_DADO_VIEW (ID_DADO_VIEW INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ID_DADO INTEGER NOT NULL,
                                        QTD_DADO_VIEW INTEGER NOT NULL,
                                        FOREIGN KEY(ID_DADO) REFERENCES TBL_TIPO_DADO_VIEW(ID_DADO));
            
                   

---**************************************
---
---         SQL INPUT
---
---**************************************


---INSERINDO NA TABELA SLA
INSERT INTO TBL_SLA(SLA) VALUES ("D1"), ("8H"), ("6H"),("4H"), ("2H"), ("D0");

---SELECT * FROM TBL_SLA;

---INSERINDO NA TABELA PONDERADOR
INSERT INTO TBL_PONDERADOR(PONDERADOR)
VALUES ("0,4"), ("0,6"), ("0,8"),("0,2"), ("1,5"), ("2,4");

---SELECT * FROM TBL_PONDERADOR;

---INSERINDO NA TABELA PRODUTO
INSERT INTO TBL_PRODUTO(ID_PONDERADOR, ID_SLA, NOME_PRODUTO, INFOS)
VALUES (1,2,"CARTAO DE GRÉDITO", "{VALOR}{CNPJ}{GARANTIA}"),(3, 2, "ABERTURA", "{TIPO_NAT_JUR}{MODULO}");

---SELECT DISTINCT * FROM TBL_PRODUTO AS PRODUTO INNER JOIN TBL_SLA AS SLA ON PRODUTO.ID_SLA = SLA.ID_SLA;

---INSERINDO NA TABELA CARGO
INSERT INTO TBL_CARGO(CARGO)
VALUES ("ANALISTA"), ("OPERADOR 6H"), ("OPERADOR 8H");

---SELECT * FROM TBL_CARGO;

---INSERINDO NA TABELA PROCESSO
INSERT INTO TBL_PROCESSO(NOME_PROCESSO, ESTEIRA_PROCESSO)
VALUES ("ABERTURA", "GOM"), ("ABERTURA", "GOE"),("CREDITO", "GOM"),("SERVICO", "GOM"), ("GARANTIAS", "GOE"), ("LEASING", "GOE"), ("CAIXA", "GOM");

---SELECT * FROM TBL_PROCESSO;

---INSERINDO NA TABELA SKILL
INSERT INTO TBL_SKILL(ID_PROCESSO, SKILL)
VALUES (1,"2"),(2,"4"),(3,"1"),(4,"2");

---SELECT * FROM TBL_SKILL;

---SELECT DISTINCT * FROM TBL_PROCESSO AS PROCESSO JOIN TBL_SKILL AS SKILL ON PROCESSO.ID_PROCESSO = SKILL.ID_PROCESSO;

---INSERINDO NA TABELA COLABORADOR
INSERT INTO TBL_COLABORADOR(ID_CARGO, ID_SKILL, RACF, FUNCIONAL, NOME, ATIVO, HIERARQUIA)
VALUES ("1","1","EMERVIN","789546213","EMERSON VINICIUS RAFAEL","1","SPV: LEANPET, COORD: LEANPET"),
        ("2","2","VIFANTI","987456325","VINICIUS CAMPOS FANTI","1", "SPV: LEANPET, COORD: LEANPET"),
        ("3","2","THAUTRI","965874321","THAUAN TRINDADE MORENO","1", "SPV: LEANPET, COORD: LEANPET");

---SELECT* FROM TBL_COLABORADOR;

---INSERINDO NA TABELA PRIORIDADE
INSERT INTO TBL_PRIORIDADE(NIVEL_PRIORIDADE)
VALUES ("1"),("2"),("3"),("4");

---SELECT * FROM TBL_PRIORIDADE;

---INSERINDO NA TABELA ANALISE
INSERT INTO TBL_ANALISE(ID_PRODUTO, ID_PROCESSO, ID_COLABORADOR, ID_PRIORIDADE, DT_RECEBIMENTO, HR_RECEBIMENTO, DT_INCLUSAO, HR_INCLUSAO, SEQUENCIA_ATUAL, FIM_ATUACAO, INFOS_COMPLEMENTARES)
VALUES ("1", "1", "3", "4", "06-05-2020", "18:00:00", "06-05-2020", "18:00:00", "1", "0", ""),
        ("2", "1", "2", "3", "06-05-2020", "18:00:00", "06-05-2020", "18:00:00", "1", "0", ""),
        ("3", "3", "1", "2", "06-05-2020", "18:00:00", "06-05-2020", "18:00:00", "1", "0", "");

---SELECT* FROM TBL_ANALISE;

---INSERINDO NA TABELA ATUACAO
INSERT INTO TBL_ATUACAO(ID_ANALISE, DT_INICIO, HR_INICIO, DT_ENCERRAMENTO, HR_ENCERRAMENTO)
VALUES ("1", "06-05-2020", "", "06-05-2020", ""),
        ("1", "06-05-2020", "", "06-05-2020", ""),
        ("2", "06-05-2020", "", "06-05-2020", "");
        
---INSERINDO NA TABELA TIPO DE DADOS_VIEW
INSERT INTO TBL_TIPO_DADO_VIEW (TIPO_DADO) VALUES ("ENTRY"),("COMBOBOX");

---SELECT * FROM TBL_TIPO_DADO_VIEW;

INSERT INTO TBL_ACESSO(RACF, DT_HR_ENTRADA, TIPO_ENTRADA) VALUES ("THAUTRI", "2020-05-07 20:00:00","MAR2"), ("EMERVIN", "2020-05-07 20:00:00","MAR2");

---RETORNA O ID_ACESSO PARA ATUALIZAR A SAIDA
--SELECT MAX(ID_ACESSO) AS MAX_ID_ACESSO FROM TBL_ACESSO WHERE RACF = "THAUTRI";

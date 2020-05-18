

---**************************************
---
---         LOG ACESSO
---
---**************************************

---insere na tabela a entrada
INSERT INTO TBL_ACESSO(FUNCIONAL, DT_HR_ENTRADA) VALUES ("444444", "12-05-2020");

---obtem o id_acesso e insere na tabela a saida
UPDATE TBL_ACESSO SET dt_hr_saida = '13-12-2020' WHERE ID_ACESSO = (SELECT ID_ACESSO FROM (SELECT ID_ACESSO FROM TBL_ACESSO where funcional = '444444' ORDER BY ID_ACESSO DESC LIMIT 1) as temp);

---vizualiza a tabela 
SELECT * FROM TBL_ACESSO;

---(truncate) limpa os dados da tabela
DELETE FROM TBL_ACESSO;




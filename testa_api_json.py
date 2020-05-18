import JSON_Executa

json_string = {"SUBPRODUTO": "DUPLO CHECK", "GARANTIA": "RENEGOCIAÇÃO", "VALOR": 1000000, "NºCONTRATO": 85215697}
json_tipos_dados = {"SUBPRODUTO": "ENTRY", "GARANTIA": "ENTRY",
                    "VALOR": "ENTRY", "NºCONTRATO": "ENTRY", "DATA VENCIMENTO": "ENTRY"}


print(JSON_Executa.get_keys_json(json_string))
print(JSON_Executa.get_value_json(json_string, "SUBPRODUTO"))
print(JSON_Executa.tamanho_json(json_string))


def tamanho_json(json):

    """

        OBTÉM O TAMANHO DO JSON.

        # Arguments
            json:                     - Required: Json o qual será obtido o tamanho (Dict)

        # Returns

    """

    try:
        return len(json.keys())
    except Exception as ex:
        print(ex)
        return None

def get_value_json(json, key):

    """

        OBTÉM O VALOR DE UMA CHAVE NO JSON.

        # Arguments
            json:                     - Required: Json o qual será obtida o valor da chave (Dict)
            key:                      - Required: Chave a qual será obtida o valor (String)

        # Returns

    """

    try:
        return json[key]
    except Exception as ex:
        print(ex)
        return None

def get_keys_json(json):

    """

        OBTÉM AS CHAVES DO JSON.

        # Arguments
            json:                     - Required: Json o qual será obtida os nomes das chaves (Dict)

        # Returns

    """

    try:
        return list(json.keys())
    except Exception as ex:
        print(ex)
        return None

def get_values_tipos_json(json, tipo_dado):

    """

        OBTÉM A QUANTIDADE DE TIPOS DO JSON.
        EXEMPLO: QUANTIDADE DE TIPOS DE ENTRY'S do JSON.

        # Arguments
            json:                     - Required: Json o qual será obtida os nomes das chaves (Dict)
            tipo_dado:                - Required: Tipo de dado para obter-se a quantidade do tipo de dado (Dict)

        # Returns

    """

    quantidade_componentes_tipo = 0

    try:
        for value in json.values():
            if value == tipo_dado:
                quantidade_componentes_tipo +=1
        return quantidade_componentes_tipo
    except Exception as ex:
        print(ex)
        return None


json_string = {"SUBPRODUTO": "DUPLO CHECK", "GARANTIA": "RENEGOCIAÇÃO", "VALOR": 1000000, "NºCONTRATO": 85215697}
json_tipos_dados = {"SUBPRODUTO": "ENTRY", "GARANTIA": "ENTRY",
                    "VALOR": "ENTRY", "NºCONTRATO": "ENTRY", "DATA VENCIMENTO": "ENTRY"}

print(get_keys_json(json_string))
print(get_value_json(json_string, "SUBPRODUTO"))
print(tamanho_json(json_string))

for value in get_keys_json(json_string):
    print(get_value_json(json_string, value))

print(get_values_tipos_json(json_tipos_dados, "ENTRY"))

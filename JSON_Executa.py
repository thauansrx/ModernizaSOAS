"""

    MICROSERVIÇO RESPONSÁVEL POR TODAS AS INTERAÇÕES COM O TIPO JSON.
    GET KEYS | GET VALUES | GET LEN

    # Arguments
        json:                           - Required: Json o qual será obtido a função (Dict)

    # Returns
        validador_json                 - Required : Validador de execução da ação dessa classe. (Boolean)

"""


__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "06/05/2020"


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
                quantidade_componentes_tipo += 1
        return quantidade_componentes_tipo
    except Exception as ex:
        print(ex)
        return None


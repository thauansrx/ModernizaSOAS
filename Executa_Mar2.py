import sys
import time

def retorna_valor(path_chrome_driver, funcional_input, senha_input):

    time.sleep(10)
    return True

if __name__ == "__main__":

    try:
        path_chrome_driver = sys.argv[1]
        funcional_input = sys.argv[2]
        senha = sys.argv[3]
        validador_login = retorna_valor(path_chrome_driver, funcional_input, senha)
        print(validador_login)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <string_to_reverse>")
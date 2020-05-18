import sys
import time

def retorna_valor():

    time.sleep(2)
    caminho_chrome_driver = r'C:\Users\Public\chromedriver.exe'
    return caminho_chrome_driver

if __name__ == "__main__":

    try:
        validador_login = retorna_valor()
        print(validador_login)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <string_to_reverse>")
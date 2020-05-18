import subprocess
import os

path_api = os.getcwd() + "\API" + "\\" + "Executa_Mar2.exe"

proc = subprocess.Popen([path_api, "987297361", "852147"], stdout=subprocess.PIPE)
lines = proc.stdout.readline()


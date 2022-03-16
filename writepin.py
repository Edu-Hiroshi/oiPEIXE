import requests
import random
import time

while (True):
    
    temp = 25 + random.randint(1,6) - random.randint(1,6)

    #simula valores de temperatura, ao adicionar o valor de temperatura ao PIN V1
    url = "http://blynk-cloud.com/q5nnotGVGKpzhdvCpwyFx7pU3u0PF0an/update/V1?value="+str(temp)

    #ativa a URL acima, enviando assim os valores de temperatura aleatorios
    r = requests.get(url)

    print(r.text)

    time.sleep(4)

from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import csv
from datetime import date
import time
import requests
import datetime as dt

# em "/temp" sempre digitar: Datahora, Temperatura

# em "/" sempre digitar:
#       [wget --post-data "data=123"]
#                   ou
#       [curl -H \Content-Type:application/json\ -X POST --data "{\"data\":\"123\"}" http://localhost:5000/]


app = Flask(__name__)

@app.route('/')
def webhook():

    while (True):

        data = request.args.get("data")

        url = "http://blynk-cloud.com/q5nnotGVGKpzhdvCpwyFx7pU3u0PF0an/get/V1"

        r = requests.get(url)

        f = open('data{}.csv'.format(date.today()), 'a+')

        temp = float(r.text.replace('"', '').replace('[', '').replace(']', ''))

        if temp > 28:
            url = 'http://blynk-cloud.com/q5nnotGVGKpzhdvCpwyFx7pU3u0PF0an/notify'
            myobj = {'body': 'ALERTA! \n A temperatura está acima do normal'}

            x = requests.post(url, json=myobj)

        with f:
            writer = csv.writer(f)

            writer.writerow([time.time(), r.text.replace('"', '').replace('[', '').replace(']', '')])

        # depois aumentar o timer
        time.sleep(30)


@app.route("/grafico")
def home():
    return render_template('TEMP.html',url='/static/images/TEMP.png')


@app.route('/temp')
def temp():

    x=[]
    y=[]

    dataset = open('data{}.csv'.format(date.today()), 'r')
    tabela = pd.read_csv('data{}.csv'.format(date.today()))
    tabela

    x = tabela['Datahora']
    y = tabela[' Temperatura']

    #n=20
    #duration=1000
    #now=time.mktime(time.localtime())
    #timestamps=np.linspace(now,now+duration,n)
    dates=[dt.datetime.fromtimestamp(ts) for ts in x]
    datenums=md.date2num(dates)


    plt.ylabel('TEMPERATURA (Cº)')
    plt.subplots_adjust(bottom=0.2)
    plt.xticks( rotation=25 )
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    datenumsl = datenums[0:30]
    yl = y[0:30]
    plt.plot(datenumsl,yl)
    plt.savefig('static/images/TEMP.png')

    # plt.show()

    resp = jsonify(success=True)  # Colocar no final da função temp
    return resp


@app.route('/timer')
def alimentar():

    while (True):
        if dt.datetime.now().hour == 14:
            url = 'http://blynk-cloud.com/q5nnotGVGKpzhdvCpwyFx7pU3u0PF0an/notify'
            myobj = {'body': 'É aconselhavel alimentar os peixes'}

            k = requests.post(url, json=myobj)

        time.sleep(3600)


if __name__ == "__main__":
    app.run(debug=True)
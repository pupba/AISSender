from flask import Flask, render_template, request, jsonify
import requests
from TCPA import *
import pandas as pd
import json
sender = Flask(__name__)
tcpamod = None
tcpa = Tcpa()


@sender.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        btname = request.form.get('btn')
        global tcpamod
        if btname == "시작":
            tcpamod = Tcpa()
            ipAddress = request.form['ip-address']
            # AIS 데이터 요청
            # IP 주소에 요청 보내기
            response = requests.get(f"http://{ipAddress}/ais_data")

            # 응답 대기
            ais = response.json()
            ais = {col: data for data, col in zip(
                json.loads(ais["ais_records"]), ais["columns"])}
            # 계산
            data = pd.DataFrame(ais, index=[0])
            print(tcpa.get())
            tcpamod = WorkerThread(tcpa, (data, ipAddress, tcpa.get()))
            tcpamod.start()
        else:
            tcpamod.stop()

    return render_template('index.html')


@sender.route('/ais_data', methods=['GET', "POST"])
def get_ais_record():
    if request.method == "GET":
        ais_data = pd.read_csv("./ais20171001_top5/ais_top4_mmsi440311690.csv")
        if not ais_data.empty:
            record = ais_data.loc[0, [
                'MMSI', 'Latitude', 'Longitude', 'SOG', 'COG']]
            return jsonify({"ais_records": record.to_json(orient='records'), "columns": ['MMSI', 'Latitude', 'Longitude', 'SOG', 'COG']})

    if request.method == "POST":
        req = request.form
        print(f'TCPA : {req["TCPA"]}, Status : {req["status"]}')
    return jsonify({'message': 'No more AIS records'})


if __name__ == "__main__":
    sender.run(host='0.0.0.0', port=8080, debug=True)

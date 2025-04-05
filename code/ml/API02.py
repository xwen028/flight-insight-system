from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

app = Flask(__name__)

@app.route('/flightprediction', methods=['POST'])
def flight_prediction():
    try:
        data = request.get_json()

        # 提取并验证数据
        flight_number = data.get('flightNumber')
        departure_airport = data.get('departureAirport')
        arrival_airport = data.get('arrivalAirport')
        scheduled_departure = data.get('scheduledDeparture')
        scheduled_arrival = data.get('scheduledArrival')
        aircraft_type = data.get('aircraftType')
        TMAX = data.get('TMAX')
        TMIN = data.get('TMIN')
        PRCP = data.get('PRCP')

        if not (departure_airport and arrival_airport and scheduled_departure):
            return jsonify({"error": "Missing required fields"}), 400

        # 创建数据集
        dataModel1 = pd.DataFrame([{
            'scheduledDeparture': scheduled_departure,
            'scheduledArrival': scheduled_arrival,
            'UniqueCarrier': flight_number,
            'TailNum': aircraft_type,
            'Origin': departure_airport,
            'Dest': arrival_airport,
            'TMAX': TMAX,
            'TMIN': TMIN,
            'PRCP': PRCP,
        }])

        # 转换日期时间字段
        dataModel1['scheduledArrival'] = pd.to_datetime(dataModel1['scheduledArrival'])
        dataModel1['scheduledDeparture'] = pd.to_datetime(dataModel1['scheduledDeparture'])

        # 提取日期时间特征
        dataModel1['Month'] = dataModel1['scheduledDeparture'].dt.month.astype(int)
        dataModel1['DayofMonth'] = dataModel1['scheduledDeparture'].dt.day.astype(int)
        dataModel1['DepTime'] = dataModel1['scheduledDeparture'].dt.hour.astype(int)
        dataModel1['ArrTime'] = dataModel1['scheduledArrival'].dt.hour.astype(int)

        # 删除原始日期时间列
        dataModel1 = dataModel1.drop(['scheduledDeparture', 'scheduledArrival'], axis=1)

        # 加载编码器
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)

        def encode_category(col, value):
            return encoders[col]['mapping'].get(value, None)

        def decode_category(col, encoded_value):
            return encoders[col]['inverse_mapping'].get(encoded_value, None)

        # 编码类别特征
        encoder_col = ['UniqueCarrier', 'TailNum', 'Origin', 'Dest']
        for col in encoder_col:
            dataModel1[col] = [encode_category(col, row) for row in dataModel1[col]]

        # 重新排列列的顺序
        new_columns_order = ['Month', 'DayofMonth', 'DepTime', 'ArrTime', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'TMAX', 'TMIN', 'PRCP']
        dataModel1 = dataModel1[new_columns_order]

        # 加载模型
        with open('flight_modelRaF.pkl', 'rb') as f:
            flight_model = pickle.load(f)

        # 进行预测
        y_pred1 = flight_model.predict(dataModel1)

        # 解码预测结果
        result1 = {
            "ArrDelayPredict": [decode_category('ArrDelay', row) for row in y_pred1[:, 0].tolist()],
            "DepDelayPrediction": [decode_category('DepDelay', row) for row in y_pred1[:, 1].tolist()],
            "ReasonPrediction": [decode_category('ReasonForDelay', row) for row in y_pred1[:, 2].tolist()],
        }

        return jsonify(result1)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ticketpriceprediction', methods=['POST'])
def ticket_price_prediction():
    try:
        data = request.get_json()

        # 提取并验证数据
        flight_number = data.get('flightNumber')
        departure_airport = data.get('departureAirport')
        arrival_airport = data.get('arrivalAirport')
        scheduled_departure = data.get('scheduledDeparture')
        scheduled_arrival = data.get('scheduledArrival')
        aircraft_type = data.get('aircraftType')
        ticket_price = data.get('ticketPrice')

        if not (departure_airport and arrival_airport and scheduled_departure and ticket_price):
            return jsonify({"error": "Missing required fields"}), 400

        # 创建数据集
        dataModel2 = pd.DataFrame([{
            'scheduledDeparture': scheduled_departure,
            'scheduledArrival': scheduled_arrival,
            'UniqueCarrier': flight_number,
            'TailNum': aircraft_type,
            'Origin': departure_airport,
            'Dest': arrival_airport,
            "Price": ticket_price
        }])

        # datatest = [{
        #     'scheduledDeparture': scheduled_departure,
        #     'scheduledArrival': scheduled_arrival,
        #     'UniqueCarrier': flight_number,
        #     'TailNum': aircraft_type,
        #     'Origin': departure_airport,
        #     'Dest': arrival_airport,
        #     "Price": ticket_price
        # }]
        #
        # print (datatest)

        # 转换日期时间字段
        dataModel2['scheduledArrival'] = pd.to_datetime(dataModel2['scheduledArrival'])
        dataModel2['scheduledDeparture'] = pd.to_datetime(dataModel2['scheduledDeparture'])

        # 提取日期时间特征
        dataModel2['Month'] = dataModel2['scheduledDeparture'].dt.month.astype(int)
        dataModel2['DayofMonth'] = dataModel2['scheduledDeparture'].dt.day.astype(int)
        dataModel2['DepTime'] = dataModel2['scheduledDeparture'].dt.hour.astype(int)
        dataModel2['ArrTime'] = dataModel2['scheduledArrival'].dt.hour.astype(int)

        # 删除原始日期时间列
        dataModel2 = dataModel2.drop(['scheduledDeparture', 'scheduledArrival'], axis=1)

        # 加载编码器
        with open('encodersTicket.pkl', 'rb') as f:
            encoders2 = pickle.load(f)

        def encode_category2(col, value):
            return encoders2[col]['mapping'].get(value, None)

        def decode_category2(col, encoded_value):
            return encoders2[col]['inverse_mapping'].get(encoded_value, None)

        # 编码类别特征
        encoder_col2 = ['UniqueCarrier', 'TailNum', 'Origin', 'Dest']
        for col in encoder_col2:
            dataModel2[col] = [encode_category2(col, row) for row in dataModel2[col]]

        # 重新排列列的顺序
        new_columns_order2 = ['Month', 'DayofMonth', 'DepTime', 'ArrTime', 'UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'Price']
        dataModel2 = dataModel2[new_columns_order2]

        # 加载模型
        with open('ticketModel.pkl', 'rb') as f:
            flight_model2 = pickle.load(f)

        # 进行预测
        y_pred2 = flight_model2.predict(dataModel2)

        # 生成预测结果
        result2 = {
            'FuturePrice': y_pred2.tolist()
        }

        return jsonify(result2)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
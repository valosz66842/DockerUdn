#define PY_SSIZE_T_CLEAN above the #include <Python.h>.
from confluent_kafka import Producer
import datetime
import socket
import json
def Els(ip,title):
    UesrRecord= {"UesrRecord":{
        "title":title,
    }}
    ElsDict={}
    Date = '%Y-%m-%d'
    Time='%H:%M:%S'
    ElsDict["ip"]=ip
    ElsDict["Date"]=datetime.datetime.now().strftime(Date)
    ElsDict["Time"]=datetime.datetime.now().strftime(Time)
    ElsDict.update(UesrRecord)
    return ElsDict
def producer(kafka_value):
    ip_port ="kafka:9092"
    value = json.dumps(kafka_value, ensure_ascii=False)
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        'bootstrap.servers': ip_port  # <-- 置換成要連接的Kafka集群
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'kafkatopic'
    # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
    producer.produce(topicName, value=value)#傳送進去 Topic,data
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()
if __name__ == '__main__':
    producer(Els("127.0.0.1","5"))
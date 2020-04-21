from confluent_kafka import Producer, Consumer
from elasticsearch import Elasticsearch, helpers
import json
import socket
import pymysql
import pandas as pd
class MySqlOperator:
    def __init__(self,host,user,password):
        self.conn = pymysql.Connect(host,user,password)
        self.cursor = self.conn.cursor()  # 設置光標
    def make_table_sql(self, df):  # 抓出資料的型態
        columns = df.columns.tolist()
        make_table = []
        for item in columns:
            if 'int' in str(df.dtypes[item]):
                char = item + ' INT'
            elif 'float' in str(df.dtypes[item]):
                char = item + ' float'
            elif 'object' in str(df.dtypes[item]):
                char = item + ' VARCHAR(2000)'
            elif 'datetime' in str(df.dtypes[item]):
                char = item + ' DATETIME'
            make_table.append(char)
        return ','.join(make_table)
    def mysqlconnect(self,dbname,table_name):
        self.dbname=dbname
        self.table_name=table_name
    def csvtomysql(self,df):
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.dbname))#若沒有目錄創建一個
        self.conn.select_db(self.dbname)  # 連線的名字
        values = df.values.tolist()
        strs = ''
        for i in df.columns.tolist():
            strs += i
            strs += ','
        strs = strs[:-1]
        s = ','.join(['%s' for i in range(len(df.columns))])
        string = self.make_table_sql(df)
        try:
            self.cursor.execute('CREATE TABLE {} ({})'.format(self.table_name,string))#創造表格
        except:
            pass
        sqlStuff = ('INSERT INTO {} ({}) VALUES ({})'.format(self.table_name,strs, s))#塞資料
        self.cursor.executemany(sqlStuff, values)
    def findAll(self):
        sql = "select * from {}.{}".format(self.dbname,self.table_name)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
    def find(self,string):
        sql = "select {} from {}.{}".format(string,self.dbname, self.table_name)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
    def groupfind(self,string,group):
        sql = "select {} from {}.{} group by {}".format(string,self.dbname, self.table_name,group)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
class kafka_connect:
    def __init__(self, ip_port):
        self.ip_port = ip_port # xx.xxx.xxx.xxx:9092 xxx自己kafka的IP
    # 轉換msgKey或msgValue成為utf-8的字串
    def try_decode_utf8(self, data):
        if data:
            return data.decode('utf-8')
        else:
            return None
    # 當發生Re-balance時, 如果有partition被assign時被呼叫
    def print_assignment(self, consumer, partitions):
        result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
        print('Setting newly assigned partitions:', result)
    # 當發生Re-balance時, 之前被assigned的partition會被移除
    def print_revoke(self, consumer, partitions):
        result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
        print('Revoking previously assigned partitions: ' + result)
    def kafka_consumer(self):
        props = {
            'bootstrap.servers': self.ip_port,  # Kafka集群在那裡? (置換成要連接的Kafka集群)
            'group.id': 'goodgo',
            'auto.offset.reset': 'earliest',  # Offset從最前面開始
        }
        # 步驟2. 產生一個Kafka的Consumer的實例
        consumer = Consumer(props)
        # 步驟3. 指定想要訂閱訊息的topic名稱
        topicName = 'kafkatopic'
        # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
        consumer.subscribe([topicName], on_assign=self.print_assignment, on_revoke=self.print_revoke)
        count = 0 # 紀錄筆數
        while True:
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取
            if len(records) > 0:
                count += 1
                for record in records:
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    # 取出msgKey與msgValue
                    msgKey = self.try_decode_utf8(record.key())
                    msgValue = self.try_decode_utf8(record.value())
                    print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    ip_port = "http://127.0.0.1:9200"
                    savedata_els(http_ip_port=ip_port,msgValue=msgValue)
                    s.close()

                # 秀出metadata與msgKey & msgValue訊息
def savedata_els(http_ip_port,msgValue):
    els_save_data = json.loads(msgValue)
    es = Elasticsearch(http_ip_port)
    actions = []
    action = {
        "_index": "meowjango",
        "_type": "meowjango",
    }
    action.update(els_save_data)
    actions.append(action)
    print(actions)
    helpers.bulk(es, actions)
    db = MySqlOperator('127.0.0.1', 'root', 'aaaa')  # 連線 user身分 密碼
    conn = db.conn
    print(els_save_data["UesrRecord"]["title"])
    print(els_save_data["ip"])
    print(els_save_data["Date"])
    print(els_save_data["Time"])
    df = pd.DataFrame(
        data=[{'title': els_save_data["UesrRecord"]["title"],
               "ip": els_save_data["ip"],
               "Date": els_save_data["Date"],
               "Time": els_save_data["Time"]
               }],
        columns=['title', "ip", "Date", "Time"]
    )
    db.mysqlconnect('udn', 'record')  # 建立連線，(db_name; table_name) 如果沒有都會創建一個
    db.csvtomysql(df)  # 將資料吋入該table
    conn.commit()  # 執行

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_port ="127.0.0.1:9092"
    kafka = kafka_connect(ip_port=ip_port)
    s.close()
    while True:
        kafka.kafka_consumer()
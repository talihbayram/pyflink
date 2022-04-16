from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
import requests
import uuid
import json
from pyflink.table import expressions as expr
from pyflink.table.expressions import col
from pyflink.table.udf import udf

# 1. create a TableEnvironment


def from_kafka_to_API():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    s_env.set_parallelism(3)

    # use blink table planner
    st_env = StreamTableEnvironment \
        .create(s_env, environment_settings=EnvironmentSettings
                .new_instance()
                .in_streaming_mode()
                .use_blink_planner().build())

    st_env.execute_sql(f""" CREATE TABLE user_action (
    `table` STRING,
	`X` ROW(`X_TR` TIMESTAMP(3),
	`X_KD` BIGINT,
	`X_REF` VARCHAR))
	WITH (
    'connector' = 'kafka',  -- using kafka connector
    'topic' = 'sample_topic',  -- kafka topic
    'scan.startup.mode' = 'latest-offset',  -- reading from the beginning
    'properties.bootstrap.servers' = 'kafka:9092',  -- kafka broker address
    'format' = 'json'  -- the data format is json
        )
        """)
    st_env.execute_sql(f"""
        CREATE TABLE user_action_detail (
    `table` STRING,
	`X` ROW(`X_TR` TIMESTAMP(3),
	`X_KD` BIGINT,
	`X_REF` VARCHAR,
	`X_PRICE` BIGINT,
	`X_CUSTOMER_NO` BIGINT))
	WITH (
    'connector' = 'kafka',  -- using kafka connector
    'topic' = 'sample_topic',  -- kafka topic
    'scan.startup.mode' = 'latest-offset',  -- reading from the beginning
    'properties.bootstrap.servers' = 'kafka:9092',  -- kafka broker address
    'format' = 'json'  -- the data format is json
        )
        """)
    muh_hareket = st_env.from_path("user_action")
    muh_hareket_detay = st_env.from_path("user_action_detail")
    result = st_env.sql_query("SELECT md.X.X_CUSTOMER_NO, md.X.X_PRICE FROM user_action m, user_action_detail md WHERE m.X.X_TR = md.X.X_TR and m.X.X_REF = md.X.X_REF")
    b = result.execute()
    for i in b.collect():
        CUSTOMER_NO = i[0]
        PRICE = i[1]
        u = uuid.uuid4()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        dictionary = {
            "CUSTOMER_NO": CUSTOMER_NO,
            "PRICE": PRICE,
            "SessionID": str(u),
            "X": "1",
            "Y": "2",
            "Z": "3",
            "Q": "4"
        }
        url = 'https://httpbin.org/post'
        r = requests.post(url, data=json.dumps(dictionary), headers=headers)
        print(r.status_code)
if __name__ == '__main__':
    from_kafka_to_API()

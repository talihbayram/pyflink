# Flink From Kafka to API with Json Body
This POC aims to provide a quick-start environment and examples for users to quickly build an environment and Get Data From Kafka to Post an API . With this setup environment with docker-compose and integrates PyFlink, Kafka, Python to make it easy for experience. PyFlink (1.13.0).

# Usage

Please checkout specific branches on how to use PyFlink in a specific Flink version as PyFlink is still in active development and more and more functionalities are added in each version.

# Create Docker Image

```bash
cd image
 
# create docker image
docker build --tag pyflink/playgrounds:1.13.0-rc2 .

# publish docker image
docker push pyflink/playgrounds:1.13.0-rc2
```

# Environment Setup

1. Install [Docker](https://www.docker.com). 
2. Get Docker Compose configuration
```
git clone https://github.com/pyflink/playgrounds.git
```
3. Setup environment
* **Linux & MacOS**

```bash
cd playgrounds
docker-compose up -d
```

* **Windows**

```
cd playgrounds
set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose up -d
```

4. Check the logs of TM and JM

Check the logs of JM:
```bash
docker-compose logs jobmanager
```

Check the logs of TM:
```bash
docker-compose logs taskmanager
```

You can check whether the environment is running correctly by visiting Flink Web UI [http://localhost:8081](http://localhost:8081).

# Examples
1. PyFlink Table API with Kafka to API (httpbin)

## 1-PyFlink Table API with Kafka to API

Code：[demo_withjsonreq.py](https://github.com/talihbayram/pyflink/blob/master/examples/table/demo_withjsonreq.py)

Run:
```
cd playgrounds
docker-compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --topic  sample_topic --partitions 1 --replication-factor 1
run bat file for kafka data producer.
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/demo_withjsonreq.py
```
Check Results:

You can check from API where you post the data, or you can check result from command line with print.

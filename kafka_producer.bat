@echo off
:x
echo SEND DATA User_Action and  User_Action_Detail ! My fellow GFG Members!
docker-compose exec kafka kafka-console-producer.sh --broker-list kafka:9092 --topic sample_topic < user_action.json
docker-compose exec kafka kafka-console-producer.sh --broker-list kafka:9092 --topic sample_topic < user_action_detail.json
echo FINISH DATA User_Action and  User_Action_Detail ! My fellow GFG Members!
goto x
echo "DOCKER RM"
sudo docker rm backtest-api

echo "DOCKER BUILD"
sudo docker build -f Dockerfile -t backtest-api:v0 .

echo "DOCKER RMI"
sudo docker rmi $(sudo docker images -q -f "dangling=true")

echo "DOCKER RUN"
sudo docker run \
    -d \
    -p 8000:8000 \
    -v /etc/localtime:/etc/localtime:ro \
    --name=backtest-api \
    backtest-api:v0

#!/bin/bash
powerMetrePath="/home/micky/Desktop/thesis/powerjoular/obj"
oauthPath="/home/micky/go/oauth2-server"
findyPath="/home/micky/Desktop/thesis/findy-wallet-pwa"
findyCLIPath="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
export FCLI=$findyCLIPath
chmod +x $powerMetrePath/powerjoular
export cur=$(pwd)

#centralized
for i in `seq 1 10`; do 
rm -rf $cur/centralized/register/$i
rm -rf $cur/centralized/login/$i
done;
for i in `seq 1 10`; do 
sudo docker run --name myPostgresDb -p 5432:5432 -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -e POSTGRES_DB=postgresDB -d postgres
cd ./centralized && docker build . -t cent && docker run --net host -d cent
mkdir -p $cur/centralized/register/$i
mkdir -p $cur/centralized/login/$i
sleep 5;
cd ..
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
for word in $pid_list
    do
    echo "watching $word"
    name=$(ps -p $word -o comm=)
    $powerMetrePath/powerjoular -p $word -f ./centralized/register/$i/$name &  
done

sleep 10;
curl -X POST http://127.0.0.1:5000/init
sleep 5;
for j in `seq 1 1000`; do 
    pass=123456
    user=$j
    curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'&
    # curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'
    if (( $j % 50 == 0 )); then
      sleep 1;
    fi
done
sudo pkill powerjoular

sleep 10;
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
for word in $pid_list
    do
    echo "watching $word"
    name=$(ps -p $word -o comm=)
    $powerMetrePath/powerjoular -p $word -f ./centralized/login/$i/$name &  
done

for j in `seq 1 1000`; do 
    pass=123456
    user=$j
    curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'&
    if (( $j % 50 == 0 )); then
      sleep 1;
    fi
done


sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sleep 10;
done;
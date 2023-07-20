#!/bin/bash
powerMetrePath="/home/micky/Desktop/thesis/powerjoular/obj"
oauthPath="/home/micky/go/oauth2-server"
findyPath="/home/micky/Desktop/thesis/findy-wallet-pwa"
findyCLIPath="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
export FCLI=$findyCLIPath
chmod +x $powerMetrePath/powerjoular
export cur=$(pwd)
# sleep 10;
# $powerMetrePath/powerjoular -f $cur/base.log &
# sleep 50;
# sudo pkill powerjoular

# federated
for i in `seq 1 10`; do 
rm -rf $cur/federated/register/$i
rm -rf $cur/federated/login/$i
done;
for i in `seq 1 10`; do 
rm -rf $cur/federated/$i
done;
for i in `seq 1 10`; do 
cd $oauthPath && make run
mkdir -p $cur/federated/register/$i
mkdir -p $cur/federated/login/$i
sleep 20;
cd $cur
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
export USERNAME=$i
echo $pid_list
for word in $pid_list
do
name=$(ps -p $word -o comm=)
echo "watching $name"
$powerMetrePath/powerjoular -p $word -f $cur/federated/register/$i/$name.log &
done
python3 $cur/federated/client.py >> $cur/federated/register/$i/client.log
sudo pkill powerjoular
sleep 5;
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
echo $pid_list
for word in $pid_list
do
name=$(ps -p $word -o comm=)
echo "watching $name"
$powerMetrePath/powerjoular -p $word -f $cur/federated/login/$i/$name.log &
done
python3 $cur/federated/login.py >> $cur/federated/login/$i/client.log

sleep 1;
cd $oauthPath && make stop && make clean
cd $cur
sleep 5
done;


#decentralized
# for i in `seq 1 10`; do 
# rm -rf $cur/decentralized_identity/login/$i
# rm -rf $cur/decentralized_identity/register/$i
# done;
# for i in `seq 1 10`; do 
# cd $findyPath/tools/env && pwd && make pull-up&
# mkdir -p $cur/decentralized_identity/login/$i
# mkdir -p $cur/decentralized_identity/register/$i
# sleep 10;
# cd $findyPath/tools/env
# cli="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
# cd $findyPath/tools/env && source ./setup-cli-env.sh
# cd $cur
# sleep 10;
# export FCLI_KEY=ef116142266efa6ec17cef138765a0d873956cb7674580b5d4018ef8384b5842
# pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
# for word in $pid_list
# do
# echo "watching $word"
# name=$(ps -p $word -o comm=)
# $powerMetrePath/powerjoular -p $word -f $cur/decentralized_identity/register/$i/$name &  
# done
# cd $findyPath/tools/env && source ./setup-cli-env.sh
# cd $cur
# for j in `seq 1 1000`; do 
# user="$i\_hello\_$j"
# export FCLI_USER=$user
# $FCLI authn register&
# if (( $j % 10 == 0 )); then
#   sleep 1;
# fi
# done


# sudo pkill powerjoular
# sleep 5;
# pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
# for word in $pid_list
# do
# echo "watching $word"
# name=$(ps -p $word -o comm=)
# $powerMetrePath/powerjoular -p $word -f $cur/decentralized_identity/login/$i/$name &  
# done

# for j in `seq 1 1000`; do 
# user="$i\_hello\_$j"
# export FCLI_USER=$user
# # $FCLI authn register
# $FCLI authn login&
# if (( $j % 10 == 0 )); then
#   sleep 1;
# fi
# done

# cd $findyPath/tools/env && pwd && make clean 
# sleep 5;
# done;


# centralized
# for i in `seq 1 10`; do 
# rm -rf $cur/centralized/register/$i
# rm -rf $cur/centralized/login/$i
# done;
# for i in `seq 1 10`; do 
# sudo docker run --name myPostgresDb -p 5432:5432 -e POSTGRES_USER=postgresUser -e POSTGRES_PASSWORD=postgresPW -e POSTGRES_DB=postgresDB -d postgres
# cd ./centralized && docker build . -t cent && docker run --net host -d cent
# mkdir -p $cur/centralized/register/$i
# mkdir -p $cur/centralized/login/$i
# sleep 5;
# cd ..
# pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
# for word in $pid_list
#     do
#     echo "watching $word"
#     name=$(ps -p $word -o comm=)
#     $powerMetrePath/powerjoular -p $word -f ./centralized/register/$i/$name &  
# done

# sleep 10;
# curl -X POST http://127.0.0.1:5000/init
# sleep 5;
# for j in `seq 1 1000`; do 
#     pass=123456
#     user=$j
#     curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'&
#     # curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'
#     if (( $j % 10 == 0 )); then
#       sleep 1;
#     fi
# done
# sudo pkill powerjoular

# sleep 10;
# pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
# for word in $pid_list
#     do
#     echo "watching $word"
#     name=$(ps -p $word -o comm=)
#     $powerMetrePath/powerjoular -p $word -f ./centralized/login/$i/$name &  
# done

# for j in `seq 1 1000`; do 
#     pass=123456
#     user=$j
#     curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "'$user'", "password": "'$pass'"}'&
#     if (( $j % 10 == 0 )); then
#       sleep 1;
#     fi
# done


# sudo docker stop $(sudo docker ps -a -q)
# sudo docker rm $(sudo docker ps -a -q)
# sleep 10;
# done;
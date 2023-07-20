#!/bin/bash
powerMetrePath="/home/micky/Desktop/thesis/powerjoular/obj"
oauthPath="/home/micky/go/oauth2-server"
findyPath="/home/micky/Desktop/thesis/findy-wallet-pwa"
findyCLIPath="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
export FCLI=$findyCLIPath
chmod +x $powerMetrePath/powerjoular
export cur=$(pwd)

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
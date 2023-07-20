#!/bin/bash
powerMetrePath="/home/micky/Desktop/thesis/powerjoular/obj"
oauthPath="/home/micky/go/oauth2-server"
findyPath="/home/micky/Desktop/thesis/findy-wallet-pwa"
findyCLIPath="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
export FCLI=$findyCLIPath
chmod +x $powerMetrePath/powerjoular
export cur=$(pwd)

for i in `seq 1 10`; do 
rm -rf $cur/decentralized_identity/login/$i
rm -rf $cur/decentralized_identity/register/$i
done;
for i in `seq 1 10`; do 
cd $findyPath/tools/env && pwd && make pull-up&
mkdir -p $cur/decentralized_identity/login/$i
mkdir -p $cur/decentralized_identity/register/$i
sleep 10;
cd $findyPath/tools/env
cli="/home/micky/Desktop/thesis/findy-agent-cli/bin/findy-agent-cli"
cd $findyPath/tools/env && source ./setup-cli-env.sh
cd $cur
sleep 10;
export FCLI_KEY=ef116142266efa6ec17cef138765a0d873956cb7674580b5d4018ef8384b5842
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
for word in $pid_list
do
echo "watching $word"
name=$(ps -p $word -o comm=)
$powerMetrePath/powerjoular -p $word -f $cur/decentralized_identity/register/$i/$name &  
done
cd $findyPath/tools/env && source ./setup-cli-env.sh
cd $cur
for j in `seq 1 1000`; do 
user="$i\_hello\_$j"
export FCLI_USER=$user
$FCLI authn register&
if (( $j % 50 == 0 )); then
  sleep 1;
fi
done


sudo pkill powerjoular
sleep 5;
pid_list=$(for k in $(docker container ls --format "{{.ID}}"); do docker top $k -eo pid | awk 'NR>1 {print $1}'; done)
for word in $pid_list
do
echo "watching $word"
name=$(ps -p $word -o comm=)
$powerMetrePath/powerjoular -p $word -f $cur/decentralized_identity/login/$i/$name &  
done

for j in `seq 1 1000`; do 
user="$i\_hello\_$j"
export FCLI_USER=$user
# $FCLI authn register
$FCLI authn login&
if (( $j % 50 == 0 )); then
  sleep 1;
fi
done

cd $findyPath/tools/env && pwd && make clean 
sleep 5;
done;

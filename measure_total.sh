#!/bin/bash

./measure_centralized.sh
sleep 5;
./measure_decentralized.sh
sleep 5;
./measure_federated.sh
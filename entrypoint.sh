#!/bin/sh

apt-get update && apt-get install -y software-properties-common
add-apt-repository universe
apt-get update

apt-get install curl gcc graphviz graphviz-dev -y

#!/usr/bin/env bash

echo "word - Provisioning virtual machine..."

export LC_ALL=en_US.UTF-8
sudo echo 'LC_ALL="en_US.UTF-8"' >> /etc/environment

sudo sh -c 'echo \deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main\ >> /etc/apt/sources.list.d/pgdg.list'
sudo wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get update

sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
sudo apt-get update
sudo apt-get install gcc-4.9

sudo apt-get install libpq-dev python-pip python-dev postgresql postgresql-contrib libffi nodejs nodejs-dev -y --force-yes
sudo pip install virtualenv

echo "word - Installing NodeJS dependencies"
sudo npm install -g stylus

echo "word - Create virtual environment.."

virtualenv venv --always-copy

source venv/bin/activate

pip install -r requirements/dev.txt

echo "word - Setting up database.."

sudo -u postgres psql -c "CREATE ROLE rootuser WITH SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
sudo -u postgres psql -c "ALTER ROLE postgres WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE rootuser;"

echo " - Running resetdb.."

mkdir logs

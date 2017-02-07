#!/usr/bin/env bash

echo "word - Provisioning virtual machine..."

export LC_ALL=en_US.UTF-8

sudo sh -c 'echo \deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main\ >> /etc/apt/sources.list.d/pgdg.list'
sudo wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get update

sudo apt-get install libpq-dev python-pip python-virtualenv \
                     python-dev postgresql postgresql-contrib \
                     nodejs build-essential -y

echo "word - Installing NodeJS dependencies"
sudo npm install -g stylus

echo "word - Create virtual environment.."

virtualenv venv --always-copy

source venv/bin/activate

pip install -r requirements/dev.txt

echo "word - Setting up database.."

sudo -u postgres psql -c "CREATE ROLE $(whoami) WITH SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
sudo -u postgres psql -c "ALTER ROLE postgres WITH PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE rootuser;"

echo " - Running resetdb.."

mkdir logs

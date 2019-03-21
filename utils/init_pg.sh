#!/bin/bash

# init the database from scratch

# as user postgresql
echo "You should first drop and recreate the database"

echo "su -"
echo "su - postgres"
echo "psql"
echo "needed only for the first time to create the user"
echo "------------------------------------------8<----------------------------"
echo "CREATE USER $USER WITH PASSWORD 'NBLJFGjn.xnb, bmx/snflgbKGnvfsjg';"
echo "ALTER ROLE $USER SET client_encoding TO 'utf8';"
echo "ALTER ROLE $USER SET default_transaction_isolation TO 'read committed';"
echo "ALTER ROLE $USER SET timezone TO 'UTC';"
echo "------------------------------------------8<----------------------------"
echo ""
echo "cat << EOF > /tmp/script.sh"
echo "echo \"DROP DATABASE masks;CREATE DATABASE masks;GRANT ALL ON DATABASE masks TO lwb;\q\" | psql"
echo "EOF"
echo "chmod +x /tmp/script.sh"
echo "su - -c \"su - postgres -c /tmp/script.sh\" "
echo "exit"

read -p  "is it done [Y/n]?" isdone

if [ "$isdone" == "" ] || [ "$idone" == "y" ] || [ "$isdone" == "Y" ];
then
  echo "Continuing.."
else
  echo "Please do that first !!"
  exit 1
fi

# removing old datas
echo "===========> Removing old datas in media..."
cd ../media/images/mask/
rm -rf *
cd -

# for first installation
echo "===========> Creating migrations ..."
cd ../first/migrations/
rm -r 000*py __pycache__/
cd -
cd ..
python ./manage.py makemigrations
cd -
echo ".... Done"

# run the migration
echo "===========> Migrating ..."
cd ../
python ./manage.py migrate
echo ".... Done"

# load the database from old
echo "===========> Importing ..."
cd Utils/
python ./initialize_from_olddb.py
echo ".... Done"



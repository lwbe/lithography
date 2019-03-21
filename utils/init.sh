#!/bin/bash


# got to root directory of the project
cd ../
# remove current database
rm db.sqlite3

# run the migration
python ./manage.py migrate


# load the database from old
cd Utils/
python ./initialize_from_olddb.py




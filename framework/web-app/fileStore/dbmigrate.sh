#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
backup_dir="$1"
db_password="$2"
dbpopuate_dir="$3"
echo " migration procedure"
if [ -f "/.dockerenv" ]; then
	chmod -R 777 ${1}
	if [ "${#3}" -eq 0 ]; then
		echo "no directoy found skipping backup process"
	else
		chmod -R 777 ${3}
		mysqldump -u root -p${2} rdktesttoolproddb > "$dbpopuate_dir/rdktesttoolproddbdump.sql"
		while [ ! -f "$dbpopuate_dir/rdktesttoolproddbdump.sql" ]; do
		echo "Waiting for database backup to complete..."
		sleep 5
		done
	fi
	mysql -u root -p${2} <<EOF
	DROP DATABASE IF EXISTS rdktesttoolproddb_temp;
	CREATE DATABASE IF NOT EXISTS rdktesttoolproddb_temp;
	GRANT CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON rdktesttoolproddb_temp.* TO 'rdktesttooluser'@'127.0.0.1';
EOF
	mysql -u root -p${2} rdktesttoolproddb_temp < "$backup_dir/rdktestproddbdump.sql";
	while [ ! -f "$backup_dir/rdktestproddbdump.sql" ]; do
	echo "Waiting for database backup to complete..."
	sleep 5
	done
	echo "Database backup completed."
else
	sudo chmod -R 777 ${1}
	if [ "${#3}" -eq 0 ]; then
		echo "no directoy found Skipping backup process."
	else
		sudo chmod -R 777 ${3}
		sudo mysqldump -u root -p${2} rdktesttoolproddb > "$dbpopuate_dir/rdktesttoolproddbdump.sql"
		while [ ! -f "$dbpopuate_dir/rdktesttoolproddbdump.sql" ]; do
		echo "Waiting for database backup to complete..."
		sleep 5
		done
	fi
	sudo mysql -u root -p${2} <<EOF
	DROP DATABASE IF EXISTS rdktesttoolproddb_temp;
	CREATE DATABASE IF NOT EXISTS rdktesttoolproddb_temp;
	GRANT CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON rdktesttoolproddb_temp.* TO 'rdktesttooluser'@'127.0.0.1';
EOF
	sudo mysql -u root -p${2} rdktesttoolproddb_temp < "$backup_dir/rdktestproddbdump.sql";
	while [ ! -f "$backup_dir/rdktestproddbdump.sql" ]; do
	echo "Waiting for database backup to complete..."
	sleep 5
	done
	echo "Database backup completed."
fi
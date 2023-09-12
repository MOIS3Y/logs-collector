#!/usr/bin/env sh


# set global variables:
_DB_URL="${DB_URL}"


# parses the database connection url and sets global variables:
#
# _DBMS: {psql, sqlite} default dbms used
# _DB_HOST {domain,ip_address} for connections
# _DB_PORT {5432,3306,etc} for connections
# _DB_USER {root,admin,etc} db username
# _DB_PASSWORD {super_secret} db user password
parse_db_url() {
	local db_url=$1
	echo "-------- Check used DBMS --------"
	if [ -n "${db_url}" ]; then
		# ! PARSING:
		# -- -- --
		# extract the protocol
		local proto="$(echo "${db_url}" | grep '://' | sed -e's,^\(.*://\).*,\1,g')"
		local dbms=${proto%:*}
		# if dpms is "sqlite" we do not need parse url args
		if [ "${dbms}" = "psql" ]; then
			# remove the protocol (clean url)
			local url=$(echo "${db_url}" | sed -e s,"${proto}",,g)
			# extract the user and password (if any)
			local userpass="$(echo "${url}" | grep @ | cut -d@ -f1)"
			local password=$(echo "${userpass}" | grep : | cut -d: -f2)
			# extract the host and port connection
			local hostport=$(echo "${url}" | sed -e s,$userpass@,,g | cut -d/ -f1)
			local port=$(echo "${hostport}" | grep : | cut -d: -f2)
			# ! SET VARIABLES:
			# -- -- -- -- --
			# _DB_HOST or/and _DB_PORT for test db connection
			if [ -n "${port}" ]; then
					_DB_HOST=$(echo "${hostport}" | grep : | cut -d: -f1)
					_DB_PORT="${port}"
			else
					_DB_HOST="${hostport}"
			fi
			# _DB_USER or/and _DB_PASSWORD for future features
			if [ -n "${password}" ]; then
					_DB_USER=$(echo "${userpass}" | grep : | cut -d: -f1)
					_DB_PASSWORD="${password}"
			else
					_DB_USER="${userpass}"
			fi
		fi
	# _DBMS (sqlite or psql)
	_DBMS="${dbms}"
	echo "${_DBMS} is set as the default DBMS"
	else
		# _DBMS (sqlite)
		_DBMS="sqlite"
		echo "${_DBMS} is set as the default DBMS"
	fi
}


# waits until the database becomes available for connection
wait_db() {
	local dbms=$1
	local db_host=$2
	local db_port=$3
	if [ "${dbms}" = "psql" ];then
		echo "------- Waiting for database start -------"
		while ! nc -z $db_host $db_port; do
			sleep 0.1
		done
		echo "PostgreSQL started"
	fi
}


# app config performs database migration, collects static files
app_config() {
	echo "-------- Apply migration --------"
	python manage.py migrate --no-input
	echo "----- Collect static files ------"
	python manage.py collectstatic --no-input
}


# run app wsgi web server
app_run() {
	echo "--------- Run gunicorn ----------"
	gunicorn logs_collector.wsgi:application
}


# app entrypoint
main() {
	parse_db_url $_DB_URL
	wait_db $_DBMS $_DB_HOST $_DB_PORT
	app_config
	app_run
}

# RUN
main

exec "$@"

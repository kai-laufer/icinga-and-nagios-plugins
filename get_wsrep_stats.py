#!/usr/bin/python

# Importing some neccessary libraries
import MySQLdb, argparse, sys, prettytable

# Parsing given arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="MySQL-user for database connection", required=True)
parser.add_argument("-p", "--password", help="MySQL-password for database connection", required=True)
parser.add_argument("-H", "--host", help="DB-Host you want to connect", required=True)
parser.add_argument("-q", "--query", choices=["all", "status", "last-commited", "processlist"], help="all = Get all wsrep-informations \
	| status = Show current status | last-commited = Show last commited ID | processlist = Show processlist", required=True)
args = parser.parse_args()

# Defining MySQL-command configuration
host 	 = args.host
user 	 = args.user
password = args.password
query	 = args.query

# Queries which can be executed
queryAll	  = "SHOW STATUS LIKE 'wsrep%'"
queryStatus 	  = "SHOW STATUS LIKE 'wsrep_local_state_comment'"
queryLastCommited = "SHOW STATUS LIKE 'wsrep_last_committed'"
queryProcesslist  = "SHOW PROCESSLIST"

# Establish MySQL-connection
db	= MySQLdb.connect(host=host, user=user, passwd=password)
cursor	= db.cursor()

# Transforming result into human-readable table
def transformResult(value):
	result = []
	for thisResult in range(len(value)):
		result += value[thisResult]
	table = prettytable.PrettyTable(['Variable', 'State'])
        table.align = "l"
	for row in result:
		table.add_row(row)
	return table

# Transforming result of processlist-query into
# human-readable result table
def transformProcesslist(value):
	result = []
	for thisResult in range(len(value)):
		result += value[thisResult]
	table = prettytable.PrettyTable(['Id', 'User', 'Host', 'DB', 'Command', 'Time', 'State', 'Info', 'Rows_sent', 'Rows_examined'])
	table.align = "l"
	for row in result:
		table.add_row(row)
	return table

# Execute function for doing all stuff
def execute(user, password, host, query):
	if query == "all":
		cursor.execute(queryAll)
		result = [cursor.fetchall()]
		result = transformResult(result)
		print result
		db.close()
	elif query == "status":
                cursor.execute(queryStatus)
                result = [cursor.fetchall()]
		result = transformResult(result)
                return result
                db.close()
        elif query == "processlist":
                cursor.execute(queryProcesslist)
                result = [cursor.fetchall()]
                result = transformProcesslist(result)
                return result
                db.close()
	else:
		cursor.execute(queryLastCommited)
                result = [cursor.fetchall()]
		result = transformResult(result)
                return result
                db.close()

# Getting results
result = execute(user, password, host, query)

# Print results
print result

# Exit state is always 0
sys.exit(0)

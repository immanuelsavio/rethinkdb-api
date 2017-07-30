# deps
from flask import Flask, request
import json
import rethinkdb as r

# flask setup
app = Flask(__name__)


# key config
key = "KEY_HERE"

# rethinkdb connection & config
conn = r.connect("localhost", 28015,db="DB_NAME").repl()


routes = [
	["TABLE_NAME","TABLE_INDEX"] # create more as necessary
]

# utilities
def dictify(d,last_element):
	if len(d) == 1:
		return {d[0]:last_element}
	else:
		return {d[0]: dictify(d[1:],last_element)}

# routing
@app.route("/<path:path>", methods=["GET","POST","DELETE","PUT","PATCH"])
def new_route(path):

	if request.args.get("key") != key:
		return "Access Denied", 401

	if path.endswith("/"):
		path = path[:-1]
	path = path.split("/")

	if len(path) != 1:
		table_name, index = path[0], path[1]
		del path[0]
	else:
		return json.dumps(list(r.table(path[0]).run()))

	last_element = None

	for route in routes:
		if route[0] == table_name:
			break
	else:
		return "Route Not Found", 404

	try:
		r.table(table_name).run()
	except:
		r.table_create(table_name).run()

	for arg in path:
		if last_element:
			try:
				thisElement = last_element.get_field(arg)
				thisElement.run()
				last_element = thisElement
			except:
				if request.method == "GET":
					return "null"
		else:
			last_element = r.table(table_name).get(arg)

	if request.method == "GET":
		try:
			last_element = last_element.run()
			return json.dumps(last_element)
		except Exception as e:
			e = str(e)
			return json.dumps({'error':e}), 400

	elif request.method == "POST" or request.method == "PATCH": #TODO: PUT for data replacement
		del path[0]
		data = json.loads(request.data)
		if len(path) != 0:
			save_data = dictify(path,data)
		else:
			save_data = data
		save_data[route[1]] = index
		if r.table(table_name).get(index).run() == None:
			return json.dumps(r.table(table_name).insert(save_data).run())
		else:
			return json.dumps(r.table(table_name).get(index).update(save_data).run())

	elif request.method == "DELETE":
		del path[0]
		if len(path) == 0:
			return json.dumps(r.table(table_name).get(index).delete().run())
		else:
			return json.dumps(r.table(table_name).get(index).replace(r.row.without(dictify(path,True))).run())

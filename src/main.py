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
	["TABLE_NAME","INDEX"] # create more as necessary
]

# utilities
def dictify(d,last_element):
	if len(d) == 1:
		return {d[0]:last_element}
	else:
		return {d[0]: dictify(d[1:],last_element)}

# routing
for route in routes:
	@app.route("/{}/<path:path>".format(route[0]), methods=["GET","POST","DELETE","PUT","PATCH"])
	def new_route(path):

		if request.args.get("key") != key:
			return "Access Denied"

		if path.endswith("/"):
			path = path[:-1]
		path = path.split("/")

		lastElement = None
		index = path[0]

		for arg in path:
			if lastElement:
				try:
					thisElement = lastElement.get_field(arg)
					thisElement.run()
					lastElement = thisElement
				except:
					if request.method == "GET":
						return "null"
			else:
				lastElement = r.table(route[0]).get(arg)

		if request.method == "GET":
			try:
				lastElement = lastElement.run()
				return json.dumps(lastElement)
			except Exception as e:
				e = str(e)
				return json.dumps({'error':e})

		elif request.method == "POST" or request.method == "PATCH": #TODO: PUT for data replacement
			data = json.loads(request.data)
			del path[0]
			if len(path) != 0:
				save_data = dictify(path,data)
			else:
				save_data = data
			save_data[route[1]] = index
			if r.table(route[0]).get(index).run() == None:
				return json.dumps(r.table(route[0]).insert(save_data).run())
			else:
				return json.dumps(r.table(route[0]).get(index).update(save_data).run())

		elif request.method == "DELETE":
			del path[0]
			return json.dumps(r.table(route[0]).get(index).replace(r.row.without(dictify(path,True))).run())

	@app.route("/{}/".format(route[0]), methods=["GET"])
	def all_data():

		if request.args.get("key") != key:
			return "Access Denied"

		return json.dumps(list(r.table(route[0]).run()))

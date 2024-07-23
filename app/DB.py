from rethinkdb import RethinkDB

# clase CRUD para funciones Flask.

class RethinkDBCRUD:
	
	def __init__(self, host='localhost', port=28015, db=None):
		self.r = RethinkDB()
		self.connection = self.r.connect(host=host, port=port, db=db).repl()
		self.db = db

	def create_table(self, table_name):
		try:
			r.db(self.db).table_create(table_name).run(self.connection)
			print(f"Table {table_name} created.")
		except r.ReqlOpFailedError:
			print(f"Table {table_name} already exists.")

	def insert(self, table_name, data):
		result = self.r.table(table_name).insert(data).run(self.connection)
		return result

	def get(self, table_name, item_id):
		result = self.r.table(table_name).get(item_id).run(self.connection)
		return result

	def update(self, table_name, item_id, data):
		result = self.r.table(table_name).get(item_id).update(data).run(self.connection)
		return result

	def delete(self, table_name, item_id):
		result = self.r.table(table_name).get(item_id).delete().run(self.connection)
		return result

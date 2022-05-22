import psycopg2

connection = psycopg2.connect('dbname=postgres user=postgres password=1234')

# Open a cursor to perform database operations
cursor = connection.cursor()

# drop any existing todos table
cursor.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cursor.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")

cursor.execute("""
    INSERT INTO todos (id, description)
    VALUES (1, 'This is awesome'), (2, 'This is nice'), (3, 'This is awesome'), (4, 'This is nice');
""")

cursor.execute("SELECT * FROM todos")
result = cursor.fetchall()
print(result)

# commit, so it does the executions on the db and persists in the db
connection.commit()

# It's very important to close connections at the of everything
cursor.close()
connection.close()
table = "zipcodes"
db = None
host = None
port = None
user = None
password = None
url = """postgres://{user}:{password}@{host}:{port}/{db}
      """.format(user=user, password=password, host=host, port=port, db=db)

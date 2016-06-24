from elect.core.common import query_config

# Assuming we are using same server as elect
table = None
db = None
host = None
port = None
user = None
password = None
url = """postgres://{user}:{password}@{host}:{port}/{db}
      """.format(user=user, password=password, host=host, port=port, db=db)

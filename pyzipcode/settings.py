from elect.core.common import query_config

# Assuming we are using same server as elect
table = 'zipcodes'
db = 'zipcodes_2015'
host = query_config('postgres', 'host')
port = query_config('postgres', 'port')
user = query_config('postgres', 'user')
password = query_config('postgres', 'password')
url = """postgres://{user}:{password}@{host}:{port}/{db}
      """.format(user=user, password=password, host=host, port=port, db=db)

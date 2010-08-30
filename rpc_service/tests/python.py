import xmlrpclib
server = xmlrpclib.ServerProxy("http://localhost:8000/rpc_service/")

translation = server.get_translation('master', 'help')
languages = server.get_languages()

print translation
print languages

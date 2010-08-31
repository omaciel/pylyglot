import xmlrpclib
server = xmlrpclib.ServerProxy("http://localhost:8000/rpc_service/")

languages = server.get_languages()
for language in languages:
    translation = server.get_translation(language['short_name'], 'help')
    print language['short_name'], translation

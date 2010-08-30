require "xmlrpc/client"

server = XMLRPC::Client.new("localhost", "/rpc_service/", 8000)
translation = server.call("get_translation", "master", "help")
languages = server.call("get_languages")
status = server.call("get_status")

puts translation
puts languages
puts status

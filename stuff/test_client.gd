extends Node

const HOST: String = "127.0.0.1"
const PORT: int = 8563
const RECONNECT_TIMEOUT: float = 3.0

const Client = preload("res://tcp_client.gd")
var _client: Client = Client.new()
var sent: bool

func _ready() -> void:
	#_client.connect("data", _print_server_data)
	add_child(_client)
	await _client.connect_to_host(HOST, PORT)
	sent = false
	
func _process(delta: float) -> void:
	var mess: String = "ad\n"
	var mess2: String = "ackta\n"
	print("Sent: ", sent)
	if sent == false:
		var message: PackedByteArray = await mess.to_utf8_buffer() #[97, 99, 107] # Bytes for "ack" in ASCII
		print("Client data 1 : ", mess, message.get_string_from_utf8())
		await _client.connect_to_host(HOST, PORT)
		await _handle_client_data(message)
		print("run1")
		await _client.recieve()
	
func _handle_client_data(data: PackedByteArray) -> bool:
	print("Client data 2 : ", data.get_string_from_utf8())
	var message: PackedByteArray = data
	await _client.send(message)
	await _client.send("akta\n".to_utf8_buffer())
	return true
	
#func _print_server_data(data: PackedByteArray) -> void:
#	print("Client data 3 : ", data.get_string_from_utf8())
#	await _client.recieve()
	

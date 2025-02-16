import socket
import threading
import json
import os

clients = []
messages = []  # Stores current messages to prevent replay of chat history

# Server port
SERVER_HOST = '0.0.0.0'  # Allows connections from any address
SERVER_PORT = 12345  # Port number of the server

chat_history_number = 1  # Used to keep track of the chat history file number


# Create a new file to record chat content
def create_chat_history_file():
    global chat_history_number
    file_name = f"chat_history_{chat_history_number}.json"
    while os.path.exists(file_name):  # Ensure the file name is unique
        chat_history_number += 1
        file_name = f"chat_history_{chat_history_number}.json"

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump([], f)  # Initialize an empty list of chat history
    print(f"Chat history will be saved to file: {file_name}")
    return file_name


# Save chat messages to file
def save_message_to_history(file_name, message):
    with open(file_name, 'r+', encoding='utf-8') as f:
        chat_history = json.load(f)
        chat_history.append(message)  # Append the new message
        f.seek(0)  # Return to the beginning of the file
        json.dump(chat_history, f, ensure_ascii=False, indent=4)


# Function to handle each client
def handle_client(client_socket, addr, file_name):
    username = client_socket.recv(1024).decode('utf-8')
    print(f"{username} ({addr}) connected")


    # 发送历史消息给新用户
    for cached_message in messages:
        client_socket.send((cached_message + '\n').encode('utf-8'))

    # Broadcast user join message
    broadcast(f"{username} has joined the chat!", client_socket)
    save_message_to_history(file_name, f"{username} has joined the chat!")

    # Handle client messages
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                full_message = f"{username}: {message}"
                messages.append(full_message)  # Add message to the message list
                broadcast(full_message, client_socket)  # Broadcast the message
                save_message_to_history(file_name, full_message)  # Save to chat history file
            else:
                break
        except:
            break

    # Client disconnection
    print(f"{username} ({addr}) disconnected")
    clients.remove(client_socket)
    client_socket.close()
    broadcast(f"{username} has left the chat.", client_socket)
    save_message_to_history(file_name, f"{username} has left the chat.")  # Save the logout message


# Broadcast messages
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)


# Start the server
def start_server():
    global chat_history_number  # Use a global variable to track the chat history number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server is running on {SERVER_HOST}:{SERVER_PORT}")

    # Create a chat history file
    file_name = create_chat_history_file()

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr, file_name), daemon=True).start()


if __name__ == "__main__":
    start_server()
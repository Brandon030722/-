import socket
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Send text messages
def send_message(client_socket, message):
    if message:
        client_socket.send(message.encode('utf-8'))

# Receive messages
def receive_message(client_socket, chat_box):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                decoded_message = message.decode('utf-8')
                if decoded_message.startswith("[Image Uploaded]"):
                    sender, file_name = decoded_message.split(' ')[1:]
                    chat_box.config(state=tk.NORMAL)
                    chat_box.insert(tk.END, f"{sender} sent an image:\n")
                    display_image_in_chat(chat_box, file_name)
                else:
                    chat_box.config(state=tk.NORMAL)
                    chat_box.insert(tk.END, decoded_message + '\n')
                    chat_box.config(state=tk.DISABLED)
                    chat_box.yview(tk.END)
        except:
            break

# Display image in chat box
def display_image_in_chat(chat_box, file_name):
    try:
        img = Image.open(file_name)
        img.thumbnail((200, 200))  # Resize image for display
        photo = ImageTk.PhotoImage(img)

        chat_box.image_create(tk.END, image=photo)
        chat_box.insert(tk.END, '\n')  # Add a newline after the image
        chat_box.image = photo  # Keep a reference to prevent garbage collection
    except Exception as e:
        print(f"Error displaying image: {e}")

# Send images (UDP)
def send_image_udp(file_path, client_socket, username):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('172.20.10.4', 12346)  # UDP port

    # Get the file size
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    # Send the file name and size, the server can create a file based on this information
    udp_socket.sendto(f"{file_name},{file_size}".encode(), server_address)

    # Open the file
    with open(file_path, 'rb') as file:
        chunk_size = 1024  # Send 1024 bytes at a time
        sequence_number = 0

        # Send the file in chunks
        while chunk := file.read(chunk_size):
            udp_socket.sendto(f"{sequence_number}".encode(), server_address)  # Send the sequence number
            udp_socket.sendto(chunk, server_address)  # Send the file chunk
            sequence_number += 1
            print(f"Sending chunk {sequence_number}...")

    udp_socket.close()
    print("File transmission complete.")

    # Notify the server of the uploaded image
    send_message(client_socket, f"[Image Uploaded] {username} {file_name}")

# Open a file dialog to select an image
def upload_image(client_socket, username):
    file_path = filedialog.askopenfilename(title="Select an image")
    if file_path:
        send_image_udp(file_path, client_socket, username)

# Create the client GUI
def create_client_gui(client_socket, username):
    window = tk.Tk()
    window.title("Chat Room")

    # Window close event
    def on_closing():
        # Close the client connection
        client_socket.close()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Chat box
    chat_frame = tk.Frame(window)
    chat_box = tk.Text(chat_frame, wrap=tk.WORD, height=20, width=60, state=tk.DISABLED)
    chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_box.config(yscrollcommand=scrollbar.set)

    chat_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    # Message box
    message_frame = tk.Frame(window)
    message_entry = tk.Entry(message_frame, width=50)  # Expand the width of the input box
    message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

    def on_send_button_click():
        message = message_entry.get()
        if message:
            send_message(client_socket, message)
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"Me: {message}\n")  # Display your own message
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)
            message_entry.delete(0, tk.END)  # Clear the input box

    send_button = tk.Button(message_frame, text="Send", command=on_send_button_click)
    send_button.pack(side=tk.RIGHT, padx=10)

    upload_button = tk.Button(window, text="Upload Image", command=lambda: upload_image(client_socket, username))
    upload_button.pack(pady=10)

    message_frame.pack(fill=tk.X, padx=10)

    # Start a thread to receive messages
    threading.Thread(target=receive_message, args=(client_socket, chat_box), daemon=True).start()

    window.mainloop()

# Username input GUI
def get_username_and_start(client_socket):
    def submit_username():
        username = username_entry.get()
        if username:
            client_socket.send(username.encode('utf-8'))
            username_window.destroy()
            create_client_gui(client_socket, username)

    username_window = tk.Tk()
    username_window.title("Enter Username")

    tk.Label(username_window, text="Enter your username:").pack(pady=10)
    username_entry = tk.Entry(username_window)
    username_entry.pack(pady=5)
    tk.Button(username_window, text="Join Chat", command=submit_username).pack(pady=10)

    username_window.mainloop()

# Start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.20.10.4', 12345))

    get_username_and_start(client_socket)

if __name__ == "__main__":
    start_client()

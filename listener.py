import win32ui
import dde
import socket
import sys

def send_avisoft_command(command_string):
    """
    Connects to Avisoft via DDE and sends a command.
    """
    try:
        # 1. Initialize DDE Server (Required to act as a DDE client)
        server = dde.CreateServer()
        server.Create("AvisoftPythonClient")
        
        # 2. Create a conversation
        conversation = dde.CreateConversation(server)
        
        # 3. Connect to Avisoft RECORDER
        # Service = 'RECORDER', Topic = 'main' [cite: 1502]
        conversation.ConnectTo("RECORDER", "main")
        
        # 4. Execute the command
        # e.g., 'playlist_start', 'start', 'stop' [cite: 1497, 1498]
        conversation.Exec(command_string)
        print(f"Successfully sent command: {command_string}")
        
    except Exception as e:
        print(f"Failed to communicate with Avisoft. Is it running? Error: {e}")
    finally:
        # Clean up DDE resources if needed
        if 'server' in locals():
            server.Shutdown()

def udp_listener():
    """
    Listens for UDP packets from the Controller Computer.
    """
    UDP_IP = "0.0.0.0" # Listen on all interfaces
    UDP_PORT = 5000    # Match this port on your Controller Computer
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f"Listening for triggers on UDP port {UDP_PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024) # Buffer size
        message = data.decode('utf-8').strip()
        print(f"Received trigger '{message}' from {addr}")
        
        # Logic to decide which Avisoft command to send
        if message == "PLAY_PLAYLIST":
            # Command to start the playlist 
            send_avisoft_command("playlist_start")
            
        elif message == "START_RECORDING":
             # Command to start monitoring/recording 
            send_avisoft_command("start")
            
        elif message == "STOP":
            # Command to stop playlist or recording 
            send_avisoft_command("stop")
            
        elif message == "EXIT":
            break

if __name__ == "__main__":
    udp_listener()

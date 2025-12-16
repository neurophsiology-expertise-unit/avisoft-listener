import socket

# --- CONFIGURATION ---
# IP Address of the computer running Avisoft (The Listener)
TARGET_IP = "10.10.10.1" 
# Must match the port in 'listener_avisoft.py'
TARGET_PORT = 5000       

def send_play(song_id):
    """
    Sends a command to Avisoft to play a specific song ID.
    Usage: send_play(1) -> Sends "play 1"
    """
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Format the message exactly how the listener expects it
        message = f"play {song_id}"
        
        # Send the message (must be encoded to bytes)
        sock.sendto(message.encode('utf-8'), (TARGET_IP, TARGET_PORT))
        
        print(f">> Sent Trigger: '{message}' to {TARGET_IP}:{TARGET_PORT}")
        
        # UDP is connectionless, so we technically don't "close" a connection,
        # but it's good practice to close the socket object.
        sock.close()
        
    except Exception as e:
        print(f"Error sending trigger: {e}")

if __name__ == "__main__":
    # --- EXAMPLE USAGE ---
    print("Testing Sender...")
    
    # Play Song 1
    send_play(1)
    
    # You can add a delay if testing multiple files
    # import time
    # time.sleep(5)
    # send_play(2)
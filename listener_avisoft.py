import win32ui
import dde
import socket
import msvcrt

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5000
DDE_SERVER = "RECORDER"
DDE_TOPIC = "main"

# --- YOUR VIRTUAL PLAYLIST ---
# You can add as many as you want.
# MATLAB will send "play 1", "play 2", etc.
SONG_LIST = {
    "1": "C:\\Users\\eu-behavior03\\Downloads\\1.wav",
    "2": "C:\\Users\\eu-behavior03\\Downloads\\2.wav"
}

def main():
    print("------------------------------------------------")
    print(f"Connecting to Avisoft ({DDE_SERVER}|{DDE_TOPIC})...")
    
    try:
        dde_server = dde.CreateServer()
        dde_server.Create("PythonBridge")
        conversation = dde.CreateConversation(dde_server)
        conversation.ConnectTo(DDE_SERVER, DDE_TOPIC)
        print(">> DDE CONNECTED.")
    except Exception as e:
        print(f">> DDE ERROR: {e}")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(1.0) 
    
    print(f">> LISTENING on Port {UDP_PORT}...")
    print(">> LIST LOADED:")
    for key, path in SONG_LIST.items():
        print(f"   ID {key}: {path}")
    print("------------------------------------------------")

    running = True
    while running:
        try:
            if msvcrt.kbhit():
                if msvcrt.getch().decode('utf-8').lower() == 'q': break

            try:
                data, addr = sock.recvfrom(1024)
                # We expect messages like: "play 1" or "play 2"
                msg = data.decode('utf-8').strip().lower()
                print(f"[{addr[0]}] Received: '{msg}'")

                if conversation:
                    # 1. Parse the message
                    # Split "play 1" into ["play", "1"]
                    parts = msg.split()
                    
                    if len(parts) == 2 and parts[0] == "play":
                        song_id = parts[1]
                        
                        # 2. Look up the file path
                        if song_id in SONG_LIST:
                            file_path = SONG_LIST[song_id]
                            print(f"   >> Playing ID {song_id} -> {file_path}")
                            
                            # 3. Send command: play C:\Path\File.wav
                            conversation.Exec(f"play {file_path}")
                        else:
                            print(f"   >> ERROR: Song ID '{song_id}' not found in list.")
                    
                    else:
                        print("   >> Ignored (Format must be 'play 1', 'play 2' etc)")

            except socket.timeout:
                continue

        except Exception as e:
            print(f"Error: {e}")

    sock.close()

if __name__ == "__main__":
    main()
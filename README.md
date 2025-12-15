# Avisoft-RECORDER DDE Listener

This repository contains a Python script (`listener.py`) designed to run on a Windows PC hosting **Avisoft-RECORDER**. It listens for remote commands via UDP and forwards them to the Avisoft software using the DDE (Dynamic Data Exchange) interface supported by the manufacturer.

This tool allows a remote Controller Computer to trigger playlists and recordings programmatically, bypassing the need for manual mouse clicks or keyboard emulation.

## Features

- **Remote Triggering:** Accepts string commands over a UDP network connection.
- [cite_start]**DDE Integration:** Uses the native `RECORDER` DDE service for reliable control[cite: 1492].
- **Commands Supported:**
  - [cite_start]`PLAY_PLAYLIST`: Triggers `playlist_start` in Avisoft[cite: 1497].
  - [cite_start]`START_RECORDING`: Triggers `start` (Monitoring/Start) in Avisoft[cite: 1497].
  - [cite_start]`STOP`: Triggers `stop` (Monitoring/Stop) in Avisoft[cite: 1498].

## Prerequisites

- **OS:** Windows (Required for Avisoft and DDE support).
- **Software:** Avisoft-RECORDER (USG / USGH / Standard versions) must be installed and running.
- **Python:** Python 3.x installed.
- **Libraries:** `pywin32` is required for DDE communication.

## Installation

1. Clone this repository:

    git clone https://github.com/YOUR_USERNAME/avisoft-listener.git
    cd avisoft-listener

2. Install the required Python dependency:

    pip install -r requirements.txt

   *(Note: The `requirements.txt` should contain `pywin32`)*

## Configuration

Open `listener.py` to adjust the connection settings if necessary:

- **UDP_PORT:** Default is `5005`. Ensure your Controller Computer sends packets to this port.
- **DDE Service:** Default is `"RECORDER"`. [cite_start]If you are running a second instance of Avisoft, change this to `"RECORDER2"`[cite: 1503].

## Usage

1. **Start Avisoft-RECORDER** on the recording PC. The DDE server is active automatically when the application runs.
2. **Run the listener script**:

    python listener.py

3. **Send Commands**: From your controller computer, send a UDP string (UTF-8 encoded) to the recording PC's IP address on port 5005.

### Example Controller Code (Python)

    import socket

    UDP_IP = "192.168.1.XXX" # IP of the Recording PC
    UDP_PORT = 5005
    MESSAGE = "PLAY_PLAYLIST"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

## Troubleshooting

- **Connection Refused/Error:** Ensure Avisoft-RECORDER is open before running the script. The script cannot launch Avisoft; it can only talk to it once running.
- **Firewall:** Ensure Windows Firewall allows UDP traffic on port 5005.
- **Playlist Not Playing:** Ensure a playlist is loaded in Avisoft via `Play` > `Playlist...` before sending the start command.

## Reference
[cite_start]DDE commands are based on the Avisoft-RECORDER manual, specifically the `XTYP_EXECUTE` command set[cite: 1492].

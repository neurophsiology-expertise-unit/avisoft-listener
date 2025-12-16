# Avisoft-RECORDER UDP-DDE Bridge

This repository provides a robust solution for controlling **Avisoft-RECORDER** from a remote computer (e.g., a MATLAB stimulus controller).

**The Problem:** The Avisoft software uses **DDE** (Dynamic Data Exchange) for automation. DDE is a local-only protocol designed for Windows 3.1/95; it cannot send commands across a network to another computer.

**The Solution:** This project acts as a "Bridge." It runs a Python listener on the Avisoft PC that accepts modern **UDP network packets** from your remote computer and translates them instantly into local **DDE commands**.

## Features

- **Networked Control:** Triggers Avisoft functions from a separate computer over WiFi or LAN.
- **Virtual Playlist:** Defines song paths in the Python script (`1` -> `file1.wav`), allowing you to trigger specific files by ID.
- **Legacy MATLAB Support:** The MATLAB sender uses standard **Java networking**, meaning it works on older versions (e.g., R2017b) **without** requiring the Instrument Control Toolbox.
- **Reliable DDE:** Uses the `RECORDER` service with the `main` topic to send direct file play commands.

## Architecture

1.  **Controller PC (Sender):** Runs MATLAB (or Python). Sends a simple UDP string like `"play 1"`.
2.  **Avisoft PC (Receiver):** Runs `listener_avisoft.py`.
    -   Receives `"play 1"`.
    -   Looks up ID `1` in its internal dictionary.
    -   Sends DDE command `[play C:\Path\To\File.wav]` to Avisoft.

## Prerequisites

### On the Avisoft PC (Receiver)
-   **OS:** Windows.
-   **Software:** Avisoft-RECORDER must be installed.
-   **Python:** Python 3.x installed.
-   **Dependencies:** `pywin32` (for DDE communication).

### On the Controller PC (Sender)
-   **MATLAB:** Any version (R2017b tested). No toolboxes required.
-   **Network:** Both computers must be on the same network.

## Installation

1.  **Clone the Repository** on the Avisoft PC:

        git clone https://github.com/YOUR_USERNAME/avisoft-bridge.git
        cd avisoft-bridge

2.  **Install Python Dependencies:**

        pip install -r requirements.txt

    *(Note: `requirements.txt` contains `pywin32`)*

## Configuration

### 1. Configure the Listener (Avisoft PC)
Open `listener_avisoft.py` and edit the **Virtual Playlist** section. Map your simple IDs to the actual file paths on the Avisoft computer:

    # listener_avisoft.py

    SONG_LIST = {
        "1": "C:\\Users\\LabUser\\Documents\\stimulus_low.wav",
        "2": "C:\\Users\\LabUser\\Documents\\stimulus_high.wav"
    }

    UDP_PORT = 5000  # Default port

### 2. Configure the Sender (Controller PC)
The Controller PC (Sender) sends simple UDP commands to the Avisoft PC. You can use either MATLAB or Python for this task.

**Option A: Using MATLAB**

Open `commAvisoft.m` and set the target IP address:

    % commAvisoft.m

    REMOTE_IP = '10.10.10.1';  % IP Address of the Avisoft PC
    REMOTE_PORT = 5000;        % Must match the port in the listener script

**Option B: Using Python**

If your controller is running Python (e.g., a behavior script), use the following snippet to send commands:

    import socket

    # Configuration
    TARGET_IP = "10.10.10.1"  # IP Address of the Avisoft PC
    TARGET_PORT = 5000        # Must match the port in the listener script

    def send_trigger(song_id):
        """Sends a play command for a specific song ID."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command = f"play {song_id}"
        sock.sendto(command.encode('utf-8'), (TARGET_IP, TARGET_PORT))
        print(f"Sent: {command}")

    # Example usage
    send_trigger("1")

## Usage

### Step 1: Start Avisoft
Open **Avisoft-RECORDER** on the recording computer. The software automatically enables its DDE server.

### Step 2: Start the Listener
On the Avisoft computer, run the Python script:

    python listener_avisoft.py

*It should print: `>> LISTENING on Port 5000...`*

### Step 3: Run Remote Commands

**From MATLAB:**

    % 1. Open the connection
    commAvisoft('open');

    % 2. Play Song ID "1" (defined in the listener script)
    commAvisoft('PLAY', 1);

    % 3. Close connection when done
    commAvisoft('close');

**From Python:**

    # Simply run your Python sender script
    send_trigger("1")

## Troubleshooting

-   **"DDE Error":** Ensure Avisoft-RECORDER is currently running. The script cannot start the software; it can only control it.
-   **"Connection Refused" / No Response:** Check the **Windows Firewall** on the Avisoft PC. Allow `python.exe` or UDP Port `5000` through the firewall.
-   **File Not Playing:** Ensure the paths in `SONG_LIST` use double backslashes (e.g., `C:\\Sounds\\file.wav`) and that the files actually exist on the Avisoft PC.
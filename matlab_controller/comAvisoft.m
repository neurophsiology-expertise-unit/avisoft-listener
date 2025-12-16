function comAvisoft(command, arg)
% COMMAVISOFT (Java Version) - Controls the Python/Avisoft Bridge
%
% Usage:
%   commAvisoft('open')      -> Connect to Python Bridge
%   commAvisoft('PLAY', 1)   -> Plays Song ID "1" defined in Python
%   commAvisoft('PLAY', 2)   -> Plays Song ID "2" defined in Python
%   commAvisoft('close')     -> Clean up connection

    % Import Java Networking Classes (Standard in all MATLAB versions)
    import java.net.DatagramSocket;
    import java.net.DatagramPacket;
    import java.net.InetAddress;

    persistent socket;
    persistent targetAddress;
    persistent targetPort;

    % --- CONFIGURATION ---
    REMOTE_IP = '10.10.10.1';  % The Avisoft Computer IP
    REMOTE_PORT = 5000;        % MATCHES your Python script (5000)

    switch command
        
        % --- CONNECTION SETUP ---
        case 'open'
            try
                % Close existing socket if it's stuck open
                if ~isempty(socket) && ~isempty(tryCatchClose(socket))
                   socket.close(); 
                end
                
                % Create a standard Java UDP socket
                socket = DatagramSocket();
                
                % Resolve the IP address
                targetAddress = InetAddress.getByName(REMOTE_IP);
                targetPort = REMOTE_PORT;
                
                disp(['>> UDP Ready (Java Mode) targeting ' REMOTE_IP ':' num2str(REMOTE_PORT)]);
            catch e
                error(['Failed to open Java UDP: ' e.message]);
            end
            
        case 'close'
            if ~isempty(socket)
                socket.close();
                socket = [];
            end
            disp('>> UDP Closed.');
            
        % --- COMMANDS ---
        
        case 'PLAY'
            % Example: commAvisoft('PLAY', 1) -> Sends "play 1"
            % The Python script receives "play 1", looks up ID "1", and plays that file.
            
            if nargin < 2
                error('Usage: commAvisoft(''PLAY'', id_number)');
            end
            
            % Create string "play 1", "play 2", etc.
            cmdString = sprintf('play %d', arg);
            
            sendJavaString(socket, targetAddress, targetPort, cmdString);
            
        otherwise
            error([command ': unknown command']);
    end
end

% --- HELPER FUNCTIONS ---

function sendJavaString(sock, addr, port, msgStr)
    import java.net.DatagramPacket;

    if isempty(sock) || sock.isClosed()
        error('Socket is closed. Run commAvisoft(''open'') first.');
    end

    % Convert MATLAB string/char to Java Bytes
    msgBytes = int8(msgStr); 
    
    % Create the packet
    packet = DatagramPacket(msgBytes, length(msgBytes), addr, port);
    
    % Send
    sock.send(packet);
    disp(['>> Sent Trigger: ' msgStr]);
end

function status = tryCatchClose(sockObj)
    % Helper to check if socket is closed without crashing
    try
        if sockObj.isClosed()
            status = []; % Already closed
        else
            status = 1; % Open
        end
    catch
        status = [];
    end
end
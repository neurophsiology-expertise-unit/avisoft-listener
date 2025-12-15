function send_avisoft_trigger(commandStr)
    % Configuration
    % Replace '192.168.1.XXX' with the actual IP of your Recording PC
    remoteHost = '192.168.1.XXX'; 
    remotePort = 5005; 
    
    % Create UDP Object
    try
        u = udpport('IPV4');
        
        % Write the command as a string
        % Valid commands: "PLAY_PLAYLIST", "START_RECORDING", "STOP"
        write(u, commandStr, "string", remoteHost, remotePort);
        
        fprintf('Sent trigger: %s to %s:%d\n', commandStr, remoteHost, remotePort);
        
    catch ME
        fprintf('Error sending UDP: %s\n', ME.message);
    end
    
    % The udpport object cleans up automatically when the variable 'u' 
    % goes out of scope, but you can explicitly clear it if testing manually:
    % clear u;
end

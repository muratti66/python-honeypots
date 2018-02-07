# TelnetHoneypot

  TelnetHoneypot is part of a security service for attackers.
  <br>This application can be linger with minimum resources for telnet attacks and to saving time

### Supported OS

- Mac OS X
- Linux

### Features
- Multithreading
- Logging all telnet requests
- Changeable response messages
- No Answer feature (If any request is not to be answered)
- Sleep Between feature (sleep feature between any request and any response)
- Easy configure
- Unicode pass feature (for any request)
- Fake auth login supported

### Preperation
- Install python3 on your server (if not installed)
- Pull this git project in to ```/opt/telnethoneypot``` path on your server
- Install python3 requirements 
```pip3 install -r requirements.txt```
- Change the config.cfg file content (optional)

### Usage
- Create a daemon on your system (service files in this project, if you prefer)
    - Up the daemontools service ```csh -cf '/usr/bin/supervise /opt/telnethoneypot/service &'```
    - Or up to systemctl service ```systemctl start telnethoneypot```
- Basic test : 

``` 
Trying ::1...
telnet: connect to address ::1: Connection refused
Trying x.y.z.t...
Connected to localhost.
Escape character is '^]'.
Username: a
Password: a
OK
TSrv>asdf
ERROR : Unrecognized command
TSrv>logout
Connection closed by foreign host.
```

- Tail the log file on your system, 
<br>```tail -f /opt/telnethoneypot/logs/telnethoneypot.log```
```07/02/2018 17:26:20.487 [14755] INFO: - 0.0.0.0:23 socket started..
07/02/2018 17:26:26.367 [14755] INFO: - x.y.z.t:58892 connected to proxy socket
07/02/2018 17:26:27.629 [14755] INFO: - 6KNTZYHUQ5FQG6IJ - x.y.z.t:58892 client username entered : a 
07/02/2018 17:26:27.822 [14755] INFO: - 6KNTZYHUQ5FQG6IJ - x.y.z.t:58892 client password entered : a 
07/02/2018 17:26:30.904 [14755] INFO: - 6KNTZYHUQ5FQG6IJ - x.y.z.t:58892 client command entered : asdf 
07/02/2018 17:26:36.026 [14755] INFO: - 6KNTZYHUQ5FQG6IJ - x.y.z.t:58892 client command entered : logout 
07/02/2018 17:26:36.026 [14755] INFO: - x.y.z.t:58892 disconnected
```

### Folder Path Informations
- ".../logs" : log record path
- ".../commands" : It keeps records of attacker side command in this path
- ".../headers" : It keeps transaction record of attack based in this path

### Used Other Projects and Resources : 
- Base telnet code infrastructure take in the [here](http://www.binarytides.com/python-socket-server-code-example/)

License
----

MIT

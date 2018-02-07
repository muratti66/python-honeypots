# FtpHoneypot

  FtpHoneypot is part of a security service for attackers.
  <br>This application can be linger with minimum resources for ftp attacks and to saving time

### Supported OS

- Mac OS X
- Linux

### Features
- Multithreading
- Logging all ftp requests
- Changeable response messages
- No Answer feature (If any request is not to be answered)
- Sleep Between feature (sleep feature between any request and any response)
- Easy configure
- Unicode pass feature (for any request)
- Fake auth login supported
- Fake directory list and file upload operation supported

### Preperation
- Install python3 on your server (if not installed)
- Pull this git project in to ```/opt/ftphoneypot``` path on your server
- Install python3 requirements 
```pip3 install -r requirements.txt```
- Change the config.cfg file content (optional)

### Usage
- Create a daemon on your system (service files in this project, if you prefer)
    - Up the daemontools service ```csh -cf '/usr/bin/supervise /opt/ftphoneypot/service &'```
    - Or up to systemctl service ```systemctl start ftphoneypot```
- Basic test : 
    - Connected to ftp service
    - Entered credentials, username is anonymous and password is blank 
    - Listed main folder
    - Disconnect from ftp service

- Tail the log file on your system, 
<br>```tail -f /opt/ftphoneypot/logs/ftphoneypot.log```
```07/02/2018 17:37:17.707 [14845] INFO: - 0.0.0.0:21 socket started..
07/02/2018 17:37:28.067 [14845] INFO: - x.y.z.t:58999 connected to ftp socket
07/02/2018 17:37:28.314 [14845] INFO: - Changed mod, ip: 0.0.0.0, port : 59000
07/02/2018 17:37:30.986 [14845] INFO: - Changed mod, ip: 0.0.0.0, port : 59002
07/02/2018 17:37:31.118 [14845] INFO: - Changed mod, ip: 0.0.0.0, port : 59004
07/02/2018 17:37:31.392 [14845] INFO: - Changed mod, ip: 0.0.0.0, port : 59006
07/02/2018 17:37:31.487 [14845] INFO: - Changed mod, ip: 0.0.0.0, port : 59009
07/02/2018 17:37:35.258 [14845] INFO: - x.y.z.t:58999 disconnected from ftp socket
```

### Folder Path Informations
- ".../logs" : log record path
- ".../commands" : It keeps records of attacker side command in this path
- ".../headers" : It keeps transaction record of attack based in this path

### Used Other Projects and Resources : 
- Base ftp code infrastructure take in the [here](https://gist.github.com/scturtle/1035886)

### To do :
   - starttls support

License
----

MIT

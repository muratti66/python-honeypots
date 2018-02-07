# ProxyHoneypot

  ProxyHoneypot is part of a security service for attackers.
  <br>This application can be linger with minimum resources for proxy attacks and to saving time

### Supported OS

- Mac OS X
- Linux

### Features
- Multithreading
- Logging all http requests
- Changeable response messages
- No Answer feature (If any request is not to be answered)
- Sleep Between feature (sleep feature between any request and any response)
- Easy configure
- Unicode pass feature (for any request)
- Fake page support

### Preperation
- Install python3 on your server (if not installed)
- Pull this git project in to ```/opt/proxyhoneypot``` path on your server
- Install python3 requirements 
```pip3 install -r requirements.txt```
- Change the config.cfg file content (optional)

### Usage
- Create a daemon on your system (service files in this project, if you prefer)
    - Up the daemontools service ```csh -cf '/usr/bin/supervise /opt/proxyhoneypot/service &'```
    - Or up to systemctl service ```systemctl start proxyhoneypot```
- Basic test : 
    - Opening the browser
    - Enter the proxy settings in to browser settings
    - Opening the http://www.test.com

- Tail the log file on your system, 
<br>```tail -f /opt/proxyhoneypot/logs/proxyhoneypot.log```
```07/02/2018 18:00:50.578 [16060] INFO: - 127.0.0.1:60274 connected to proxy socket
07/02/2018 18:00:50.581 [16060] INFO: - G4H0NYYJSBLQS1IZ - 127.0.0.1:60274 client trying access to www.test.com:80 
07/02/2018 18:00:50.696 [16060] INFO: - 127.0.0.1:60275 connected to proxy socket
07/02/2018 18:00:50.697 [16060] INFO: - 5RYPTG3YW5O6X196 - 127.0.0.1:60275 client trying access to www.test.com:80 

```

### Folder Path Informations
- ".../logs" : log record path
- ".../commands" : It keeps records of attacker side command in this path
- ".../headers" : It keeps transaction record of attack based in this path
- ".../mails" : Proxy http headers and requests that the attacker has left is found in this path.

### Used Other Projects and Resources : 
- Base http code infrastructure take in the [here](https://null-byte.wonderhowto.com/how-to/sploit-make-proxy-server-python-0161232/)

### To do :
   - https connection support

License
----

MIT

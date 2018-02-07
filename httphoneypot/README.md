# WebHoneypot

  WebHoneypot is part of a security service for attackers.
  <br>This application can be linger with minimum resources for http attacks and to saving time

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
- Pull this git project in to ```/opt/webhoneypot``` path on your server
- Install python3 requirements 
```pip3 install -r requirements.txt```
- Change the config.cfg file content (optional)

### Usage
- Create a daemon on your system (service files in this project, if you prefer)
    - Up the daemontools service ```csh -cf '/usr/bin/supervise /opt/webhoneypot/service &'```
    - Or up to systemctl service ```systemctl start webhoneypot```
- Basic test : 
    - Opening the web page
    - Entered the username and password is any credential

- Tail the log file on your system, 
<br>```tail -f /opt/webhoneypot/logs/webhoneypot.log```
```07/02/2018 17:52:31.895 [16003] INFO: - 0.0.0.0:80 socket started..
07/02/2018 17:52:41.129 [16003] INFO: - x.y.z.t:60140 connected
07/02/2018 17:52:41.130 [16003] INFO: - IADFHGR9NFN2GYQK - x.y.z.t client request GET - http://x.y.z.t:80/index.html 
07/02/2018 17:52:41.131 [16003] INFO: - x.y.z.t:60140 disconnected
07/02/2018 17:52:41.286 [16003] INFO: - x.y.z.t:60142 connected
07/02/2018 17:52:41.298 [16003] INFO: - ZN19ITJQWN45ATCF - x.y.z.t client request GET - http://x.y.z.t:80/favicon.ico 
07/02/2018 17:52:41.299 [16003] INFO: - x.y.z.t:60142 disconnected
07/02/2018 17:52:45.646 [16003] INFO: - x.y.z.t:60146 connected
07/02/2018 17:52:45.648 [16003] INFO: - 0M38XSDUKBARC7IQ - x.y.z.t client request POST - http://x.y.z.t:80/index.html 
07/02/2018 17:52:45.649 [16003] INFO: - x.y.z.t:60146 disconnected
```

### Folder Path Informations
- ".../logs" : log record path
- ".../commands" : It keeps records of attacker side command in this path
- ".../headers" : It keeps transaction record of attack based in this path
- ".../mails" : Http headers and requests that the attacker has left is found in this path.

### Used Other Projects and Resources : 
- Base http code infrastructure take in the [here](http://blog.wachowicz.eu/?p=256)

### To do :
   - https socket support

License
----

MIT

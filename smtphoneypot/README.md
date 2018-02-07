# SmtpHoneypot

  SmtpHoneypot is part of a security service for attackers.
  <br>This application can be linger with minimum resources for smtp attacks and to saving time

### Supported OS

- Mac OS X
- Linux

### Features
- Multithreading
- Logging all smtp requests
- Changeable response message codes and errors
- No Answer feature (If any request is not to be answered)
- Sleep Between feature (sleep feature between any request and any response)
- Save the received mail body
- Easy configure
- Unicode pass feature (for any request)
- Fake auth login supported

### Preperation
- Install python3 on your server (if not installed)
- Pull this git project in to ```/opt/smtphoneypot``` path on your server
- Install python3 requirements 
```pip3 install -r requirements.txt```
- Change the config.cfg file content (optional)

### Usage
- Create a daemon on your system (service files in this project, if you prefer)
    - Up the daemontools service ```csh -cf '/usr/bin/supervise /opt/smtphoneypot/service &'```
    - Or up to systemctl service ```systemctl start smtphoneypot```
- Basic test : 

``` 
Trying x.y.z.x...
Connected to mail.honeypotttt.com
Escape character is '^]'.
220 mail.honeypotttt.com
ehlo Test
250-mail.honeypotttt.com
250-PIPELINING
250-8BITMIME
250-SIZE 20480000
250 AUTH LOGIN PLAIN
MAIL FROM: <test@test.com>
250 2.1.0 Ok
RCPT TO: <test@testt.com>
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
test
.
250 2.0.0 Ok: queued as GWZZZGQE
QUIT
221 2.0.0 Bye
Connection closed by foreign host. 
```

- Tail the log file on your system, 
<br>```tail -f /opt/smtphoneypot/logs/smtphoneypot.log```
```17/01/2018 14:04:54.581 [25403] INFO: - GWZZZGQE - x.y.z.t client executed : "EHLO Test"
17/01/2018 14:04:55.098 [25403] INFO: - GWZZZGQE - x.y.z.t  client executed : "MAIL FROM: <test@test.com>"
17/01/2018 14:04:55.313 [25403] INFO: - GWZZZGQE - x.y.z.t  client executed : "RCPT TO: <test@testt.com>"
17/01/2018 14:04:55.527 [25403] INFO: - GWZZZGQE - x.y.z.t  client executed : "DATA"
17/01/2018 14:04:56.181 [25403] INFO: - GWZZZGQE - x.y.z.t  client executed : "QUIT"
17/01/2018 14:04:56.181 [25403] INFO: - x.y.z.t  disconnected from Thread-3 thread
```

### Folder Path Informations
- ".../logs" : log record path
- ".../commands" : It keeps records of attacker side command in this path
- ".../headers" : It keeps transaction record of attack based in this path
- ".../mails" : Raw format e-mail that the attacker has left is found in this path.

### Used Other Projects and Resources : 
- Base smtp code infrastructure take in the [here](https://github.com/RedOneLima/SMTP)

### To do :
   - starttls support

License
----

MIT

## Python Honeypots

I rewrite together honeypots examples of the python3 programming language.
<br>And added on the samples such as simplicity, ease of use, additional features
<br>So what is honeypot? Helpful answer is [here](https://en.wikipedia.org/wiki/Honeypot_(computing))
<br>Our informations and works are in subfolders under owned names.
<br>Use it in good days :)

#### Which protocols are used ?
* Http (Port 80) 
* Smtp (Port 25) 
* Proxy (Port 3128) 
* Telnet (Port 23)
* Ftp (Port 21)

#### What is the data content ?
The honeypot data contents are as follows for different services; 
* Connection date and time 
* Attacker ip address and location 
* Smtp commands and answers with attacker attempt 
* Putted eml(data) message by attacker 
* Http method and access url 
* Client requested header information for http and proxy request 
* Client requested http url informaiton for proxy request 
* Telnet username and password retry 
* All received commands
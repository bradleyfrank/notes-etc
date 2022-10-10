# Networking

```sh
# test website/port
nc -zw1 ports.ubuntu.com 80

# find ip address
ip -4 -o addr show | grep -Ev '\blo\b' | grep -Po 'inet \K[\d.]+'
ip -4 -o addr show | grep -Po 'inet \K[\d.]+'

# get Apache web server status
curl -Is --max-time 5 https://<domain>/server-status | head -n 1

# capture packets
tcpdump --list-interfaces
tcpdump -i eth0
tcpdump -w my_packet_capture.pcap
```

![f7d828b51c1b3ae3c2678f1126e7d7a4.png](../_resources/f7d828b51c1b3ae3c2678f1126e7d7a4-1.png)
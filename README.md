# Ataque-STP-Claim-Root-Attack-Gns3

**Estudiante:**  Juan Francisco Burgos Hiciano

**Matrícula:**  2023-1981

**Asignatura:**  Seguridad en Redes

**Fecha:**  01 Junio 2026

**Link del video**: https://youtu.be/jxBDHxcn1EE


---

### Descripción y Topología del Escenario

El laboratorio fue implementado en GNS3 con el propósito de analizar el funcionamiento del protocolo Spanning Tree Protocol (STP) y comprender los riesgos asociados a la manipulación de la elección del Root Bridge dentro de una infraestructura Cisco. La topología está compuesta por un switch Cisco IOU L2 conectado a una interfaz de red del host mediante Cloud VMnet8, permitiendo la interacción con el entorno de laboratorio desde Kali Linux.

El escenario permite observar el intercambio de mensajes Bridge Protocol Data Units (BPDUs) utilizados por STP para elegir el Root Bridge de la red. Durante la práctica se monitorea cómo los switches anuncian información de prioridad y direcciones MAC para determinar qué dispositivo ocupará dicho rol. El objetivo educativo es analizar el proceso de elección del Root Bridge, verificar el comportamiento de STP ante cambios en la topología y comprender la importancia de implementar mecanismos de protección como BPDU Guard, Root Guard y una correcta configuración de prioridades para evitar modificaciones no autorizadas en la estructura lógica de la red.


### Detalles de la Topología

**Segmentación de Red:** VLAN 1 (predeterminada).
**Infraestructura:**
* **Switch Cisco IOU L2.**
* **Cloud VMnet8.**
* **Kali Linux conectado a la red de laboratorio.**
**Actores:**
* **Equipo de análisis: Kali Linux (interfaz conectada a VMnet8).**
**Dispositivo analizado:**
* **Switch Cisco IOU L2.**
**Direccionamiento**
* **Red utilizada:** 192.168.140.0/24.
* **Kali Linux:** 192.168.140.132/24.
---

<img width="888" height="650" alt="Image" src="[https:(https://github.com/jburgoshiciano-source/Ataque-STP-Claim-Root-Attack-Gns3/blob/545346caccbaedb73f508dc21df7d0e9395eeef0/wwwwwwwww.png)" />

### Tabla de Direccionamiento

| Dispositivo | Dirección IP | Máscara de Subred | Gateway Predeterminado |
| :--- | :--- | :--- | :--- |
| **Router Gateway** | 192.168.140.1 | 255.255.255.0 (/24) | N/A |
| **Kali Linux (Atacante)** | 192.168.140.132 | 255.255.255.0 (/24) | 192.168.140.132 |
---

 Requisitos Previos y Herramientas

Para la ejecución exitosa de estos scripts, se requiere el siguiente entorno:

* **Sistema Operativo:** Kali Linux o cualquier distribución Linux compatible.
* **Lenguaje:** Python 3.x.
* **Librerías:** `Scapy` (Instalación: `sudo apt install python3-scapy`).
* Simulador de Red: GNS3.
Dispositivos Simulados:
Switch Cisco IOU L2.
Cloud VMnet8.
Permisos: Acceso de superusuario (root) para la captura y análisis de tramas Ethernet y BPDUs de STP.

---

 Ataque : STP Claim Root Attack

 ### Objetivo del Script
El script implementa una práctica de laboratorio orientada al análisis del protocolo Spanning Tree Protocol (STP) y del proceso de elección del Root Bridge dentro de una infraestructura de red Cisco. Su funcionamiento consiste en capturar y analizar las Bridge Protocol Data Units (BPDUs) intercambiadas por los switches de la red, permitiendo identificar los dispositivos que participan en la topología STP y observar los valores de prioridad y dirección MAC utilizados durante la elección del Root Bridge.

La práctica permite comprender cómo STP mantiene una topología libre de bucles mediante el intercambio continuo de información entre dispositivos de capa 2. Asimismo, facilita el estudio de escenarios donde cambios en los parámetros de prioridad pueden influir en la selección del Root Bridge y provocar procesos de reconvergencia de la red. El objetivo principal es reforzar el conocimiento sobre el funcionamiento interno de STP, analizar los riesgos asociados a configuraciones inadecuadas y destacar la importancia de implementar mecanismos de protección como BPDU Guard, Root Guard y una correcta administración de prioridades para preservar la estabilidad y seguridad de la infraestructura de red.

### Parámetros Usados
**Interfaz de red:** eth0

**Topología:** Switch Cisco IOU L2, Kali Linux y Cloud VMnet8.

**Red:** 192.168.140.0/24

**Protocolo analizado:** Spanning Tree Protocol (STP).

**Dirección MAC utilizada:** Configurable mediante parámetro del script para representar el identificador del bridge analizado.

**Prioridad del Bridge:** Valor configurable para observar su influencia en el proceso de elección del Root Bridge.

**Destino de las tramas:** Dirección multicast de STP 01:80:C2:00:00:00.

**Herramienta utilizada:** Python 3.x con Scapy.

**Mensajes analizados:** Bridge Protocol Data Units (BPDUs).

**Captura de tráfico:** Almacenamiento opcional de paquetes en formato .pcap para análisis posterior en Wireshark.

**Objetivo:** Analizar el intercambio de BPDUs, identificar el Root Bridge de la red y observar el funcionamiento del proceso de convergencia de STP.

**Resultado esperado:** Visualizar los parámetros utilizados por STP para seleccionar el Root Bridge, verificar el comportamiento de la topología ante cambios de prioridad y comprender la importancia de los mecanismos de protección de capa 2.

---

### Medidas de Mitigación

Para reducir el riesgo de manipulación de la topología STP, se recomienda implementar mecanismos de seguridad que impidan que dispositivos no autorizados envíen BPDUs o intenten convertirse en Root Bridge. Entre las medidas más efectivas se encuentran BPDU Guard y Root Guard, las cuales permiten proteger la estabilidad de la red y evitar cambios inesperados en la convergencia de STP.

```bash
Switch(config)# interface FastEthernet0/2
Switch(config-if)# spanning-tree guard root
```
### Beneficios

**Evita que dispositivos no autorizados participen en el proceso de elección del Root Bridge.**

**Protege la topología STP contra cambios inesperados.**

**Reduce el riesgo de interrupciones causadas por reconvergencias innecesarias.**

**Mantiene la estabilidad y disponibilidad de la red.**

**Incrementa la seguridad de la infraestructura de capa 2.**

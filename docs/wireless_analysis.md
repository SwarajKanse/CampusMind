# 📶 Wireless & Mobile Computing Analysis — CampusMind (WMC Experiments)

## 📌 Context
In mobile and university campus environments, wireless channel conditions (signal attenuation, path loss, multipath fading, and interference) directly affect application responsiveness. CampusMind incorporates specialized mechanisms to measure and adapt to wireless constraints.

---

## 1. Electromagnetic Spectrum & Channel Propagation (WMC Exp 1 & 2)

- **2.4 GHz ISM Band (802.11b/g/n/ax)**: High penetration through campus masonry, lower bandwidth (~150 Mbps), high channel congestion.
- **5 GHz U-NII Band (802.11a/n/ac/ax)**: Lower obstacle penetration, broader bandwidth (up to 80MHz/160MHz channels), optimal for high-throughput document transfers.
- **Cellular Bands (4G LTE / 5G Sub-6)**: Variable latency (30ms - 120ms), subject to Doppler shift and handoff between base stations.

---

## 2. Interface Monitoring & Socket Telemetry (WMC Exp 4, 5, 7)

CampusMind actively inspects network adapters via `psutil.net_if_addrs()`:
- **Interface Enumeration**: Detects whether client is on Wi-Fi, Ethernet, or Cellular pseudo-interfaces.
- **Round-Trip Time (RTT) Sampling**: Measures latency fluctuations to detect link degradation.
- **Adaptive CAG Layer (Cache-Augmented Generation)**:
  - When wireless link latency spikes or signal degrades, the client prioritizes CAG cache retrieval to serve answers in `< 5ms` without round-tripping heavy prompt payloads over the air interface.
  - Minimizes wireless radio active time, reducing mobile client battery consumption.

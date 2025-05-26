# VANET-Secure-routing-protocol
# 🚗 VANET Secure Routing Protocol – NS-3 & Python Integration

This project presents a *secure routing protocol for Vehicular Ad Hoc Networks (VANETs)* by leveraging *digital signatures* and *cryptographic hash functions. The solution combines **NS-3 simulation* with *Python-based post-analysis* to handle mobility, message authentication, attack simulation, and performance evaluation.

---

## 📁 Directory Layout

```
VANET-Secure-Routing/
├── ns3_sim/
│   └── Main.py                # Main NS-3 simulation (Python bindings)
├── python_sim/
│   └── NS3_Integration.py     # Handles mobility, attack scenarios, metrics
├── README.md                  # Project documentation

  ```

---

## ⚙ Configuration Overview

### config/simulation_config.yaml

Example configuration:

yaml
vehicles:
  count: 4
  speeds: [65, 50, 35, 20]
  positions: [[0, 0], [10, 20], [30, 50], [10, 50]]
network:
  nodes: 3
  base_ip: "10.0.0.0"
  mask: "255.255.255.0"
security:
  enable_signature: true
  enable_hashing: true
attacks:
  tamper_detection: true
  replay_attack: false
  blackhole_simulation: false


📝 *Tip:* Customize node count, speed, position, and security parameters easily from this file.

---

## 🧪 System Components

### 🔹 NS-3 Simulation (ns3_sim/Main.py)

* *Technology Stack:* NS-3 (Python bindings), PyCrypto for RSA
* *Core Features:*

  * Establishes wireless ad hoc network using NS-3 WiFi modules
  * Integrates IP stack, mobility model, and echo applications
  * Implements *RSA (2048-bit) with SHA-256* for message signing
  * Enforces signature verification before forwarding

### 🔹 Python Module (python_sim/NS3_Integration.py)

* *Tasks Performed:*

  * Models vehicle motion & message transmission
  * Applies multiple cryptographic hashes (SHA-256, SHA-1, SHA-3, BLAKE2, MD5)
  * Simulates tampering and checks integrity
  * Measures message verification stats and performance
* *Key Classes:*

  * Vehicle: Simulates individual nodes (movement, signing, verification)
  * Metrics: Tracks statistics like tamper rate, detection accuracy
* *Visualization:*

  * Uses matplotlib to plot comparative hash performance
  * Boxplots illustrate time variation per algorithm

---

## 🚀 Running the Project

### 🔧 Requirements

* NS-3 compiled with Python bindings
* Python dependencies:

bash
pip install pycryptodome pandas matplotlib

---

## 📈 Evaluation Summary

### ✔ Protocol Capabilities

* End-to-end signature verification
* Real-time detection of tampered data
* Comparative analysis of hash function performance

### 🧪 Attack Models Simulated

| Attack Type     | Details                      | Result                             |
| --------------- | ---------------------------- | ---------------------------------- |
| Tampering       | Altered message contents     | Detected by hash & signature check |
| Replay Attack ❌ | (Planned for future release) | Not yet implemented                |
| Blackhole ❌     | (Planned for future release) | Not yet implemented                |

### 📊 Metrics Tracked

* Detection Accuracy = Detected Tampered / Total Sent
* Hash Speed Benchmarks:

  * SHA-256: strong and widely supported
  * BLAKE2b / SHA-3: faster alternatives with robust security
* Visual Reports:

  * Statistical plots show processing delays by hash type

---

## 🖥 Example Log Output

```
[+] Vehicle V2 received message from V1
    - Signature Valid: YES
    - Hash Match: YES

[!] Vehicle V3 received message from V2
    - Signature Valid: NO
    - Integrity Check Failed

Total Messages: 200
Tampering Detected: 40
Detection Rate: 20.00%
```

---

## 💡 Future Improvements

We welcome contributors to expand this prototype:

* ✅ Implement *Replay & Blackhole Attacks*
* ✅ Add *real-time GUI dashboard*
* ✅ Extend support for V2X message standards (CAM, DENM)

> Fork the repo and send your PRs with improvements!

---

## ⚠ Legal & Research Disclaimer

This codebase is designed for *academic and educational exploration* of security in VANETs. It *does not provide production-level assurance*, nor should it be deployed in real-world vehicular environments.

While the implementation makes use of cryptographic algorithms, they are adapted for simulation. Real deployments should rely on certified standards (e.g., IEEE 1609.2, ETSI ITS-G5), secure key infrastructures (VPKI), and verified hardware modules.

> The maintainers are not liable for any misuse or damage resulting from this simulation tool.

---

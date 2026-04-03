# Three Key Differences Between TCP and UDP

## 1. Connection Model

**TCP (Transmission Control Protocol)** is connection-oriented. Before any data is exchanged, the two endpoints must complete a **three-way handshake**:

1. Client sends `SYN`
2. Server replies with `SYN-ACK`
3. Client sends `ACK`

Only after this handshake is the connection established and data transfer begins. At the end of a session, a four-step teardown (`FIN` / `FIN-ACK` / `ACK`) closes the connection cleanly.

**UDP (User Datagram Protocol)** is connectionless. A sender simply fires a datagram at the destination address with no prior coordination. There is no handshake, no session state, and no teardown. Each datagram is independent.

**Concrete example:** Loading a web page uses TCP (HTTP/1.1 or HTTP/2). A DNS lookup uses UDP — the client fires a single query packet; the server fires a single response packet, with no connection setup required.

---

## 2. Reliability and Ordering

TCP guarantees **reliable, in-order delivery**:

- Every segment is assigned a sequence number.
- The receiver sends cumulative acknowledgements (`ACK`).
- If a segment is lost or arrives corrupted (fails checksum), the sender retransmits it.
- Out-of-order segments are held in a reorder buffer until the gap is filled, so the application always reads data in the original order.

UDP provides **no delivery guarantees and no ordering**:

- Datagrams may be dropped silently (e.g., by a congested router).
- Datagrams may arrive out of order or duplicated.
- UDP has a checksum field, but on many platforms it is optional (IPv4) or the stack may still deliver a corrupted datagram to the application.
- There is no acknowledgement or retransmission mechanism at the transport layer.

**Concrete example:** A file download over TCP (FTP, HTTP) will always produce an exact byte-for-byte copy of the source. A video stream over UDP (many live-streaming and IPTV protocols) may drop frames under congestion — the video may stutter, but playback continues without waiting for retransmission.

---

## 3. Speed and Overhead Tradeoffs

The reliability mechanisms of TCP come at a cost:

| Factor | TCP | UDP |
|---|---|---|
| Header size | 20–60 bytes | 8 bytes (fixed) |
| Per-segment overhead | ACK round trip, sequence tracking, congestion window | None |
| Latency | Higher — must wait for ACKs; head-of-line blocking on loss | Lower — no waiting |
| Throughput on lossy links | Reduced by retransmissions and congestion control | Unaffected at transport layer |
| CPU / state | Connection state, send/receive buffers, timers per connection | Stateless; minimal kernel overhead |

TCP's congestion control algorithms (CUBIC, BBR, etc.) also throttle the sender when packet loss is detected, further reducing throughput on lossy or high-latency links.

UDP sacrifices reliability for **lower latency and lower overhead**, making it well-suited for:

- **Real-time audio/video** (VoIP, video conferencing, live streaming) — a slightly degraded frame is preferable to a frozen call waiting for retransmission.
- **Online games** — position updates are time-sensitive; a stale retransmitted position is worse than no update.
- **DNS, NTP, DHCP** — single-request/single-response protocols where the application can retransmit the whole query if no answer arrives.
- **QUIC (HTTP/3)** — a modern protocol built on UDP that reimplements selective reliability and multiplexing in user space, avoiding TCP's head-of-line blocking.

**Concrete example:** A VoIP call (e.g., using RTP over UDP) sends ~50 packets per second. If one is lost, the codec generates a brief audio glitch (often imperceptible) and continues. If the same call used TCP, losing a packet would stall all subsequent audio until the retransmission arrived — a far worse user experience.

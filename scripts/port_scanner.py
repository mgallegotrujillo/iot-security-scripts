#!/usr/bin/env python3
"""
Simple IoT port scanner using TCP connect_ex checks.
"""

from __future__ import annotations

import argparse
import socket
from typing import Dict


IOT_COMMON_PORTS: Dict[int, str] = {
    23: "Telnet",
    80: "HTTP",
    443: "HTTPS",
    1883: "MQTT",
    5683: "CoAP",
    8883: "MQTT-TLS",
    502: "Modbus",
}


def scan_port(ip: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a TCP port is open using socket.connect_ex().

    Returns True if the connection is successful (port open), False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        # connect_ex returns 0 on success
        return result == 0


def scan_iot_ports(ip: str, timeout: float = 1.0) -> dict[int, bool]:
    """
    Scan common IoT-related ports on a single host.

    Returns a mapping {port: is_open}.
    """
    results: dict[int, bool] = {}

    for port in IOT_COMMON_PORTS.keys():
        is_open = scan_port(ip, port, timeout=timeout)
        results[port] = is_open

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan common IoT ports on a target host."
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Target host IP or hostname (example: 192.168.1.10)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout in seconds for each port check (default: 1.0)",
    )

    args = parser.parse_args()

    print(f"[+] Scanning common IoT ports on {args.host}")
    print(f"[+] Timeout per port: {args.timeout:.1f}s\n")

    results = scan_iot_ports(args.host, timeout=args.timeout)

    print("Port | Service    | Status")
    print("-----+------------+--------")

    for port in sorted(results.keys()):
        service = IOT_COMMON_PORTS.get(port, "Unknown")
        status = "OPEN" if results[port] else "closed"
        print(f"{port:>4} | {service:<10} | {status}")

    print("\n[*] Scan complete.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple IoT network scanner using ICMP ping sweep.
"""

from __future__ import annotations

import argparse
import ipaddress
import subprocess


def ping_host(ip: str, timeout: float = 1.0) -> bool:
    wait_seconds = max(1, int(timeout))

    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(wait_seconds), ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def scan_network(cidr: str, timeout: float = 1.0) -> list[str]:
    network = ipaddress.ip_network(cidr, strict=False)
    responsive_hosts: list[str] = []

    for host in network.hosts():
        ip = str(host)
        if ping_host(ip, timeout=timeout):
            responsive_hosts.append(ip)

    return responsive_hosts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ICMP ping sweep scanner for IoT network ranges."
    )
    parser.add_argument(
        "--network",
        required=True,
        help="Target network in CIDR notation (example: 192.168.1.0/24)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout in seconds for each ping attempt (default: 1.0)",
    )

    args = parser.parse_args()

    try:
        network = ipaddress.ip_network(args.network, strict=False)
    except ValueError as exc:
        parser.error(f"Invalid network '{args.network}': {exc}")
        return

    print(f"[+] Starting scan for network: {network}")
    print(f"[+] Timeout per host: {args.timeout:.1f}s")
    print("[-] Scanning hosts...\n")

    responsive_hosts = scan_network(str(network), timeout=args.timeout)

    print("=" * 50)
    print(f"Scan completed for {network}")
    print(f"Responsive hosts found: {len(responsive_hosts)}")

    if responsive_hosts:
        print("\nActive hosts:")
        for ip in responsive_hosts:
            print(f" - {ip}")
    else:
        print("\nNo responsive hosts detected.")
    print("=" * 50)


if __name__ == "__main__":
    main()

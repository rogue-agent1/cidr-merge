#!/usr/bin/env python3
"""CIDR merger — combine and simplify overlapping IP ranges."""
import sys, struct, socket
def ip2int(ip): return struct.unpack("!I", socket.inet_aton(ip))[0]
def int2ip(n): return socket.inet_ntoa(struct.pack("!I", n))
def parse_cidr(s):
    ip, prefix = s.split("/"); prefix = int(prefix)
    start = ip2int(ip) & ((0xFFFFFFFF << (32-prefix)) & 0xFFFFFFFF)
    end = start | (~(0xFFFFFFFF << (32-prefix)) & 0xFFFFFFFF)
    return start, end, prefix
def merge(cidrs):
    ranges = sorted(parse_cidr(c)[:2] for c in cidrs)
    merged = [ranges[0]]
    for s, e in ranges[1:]:
        if s <= merged[-1][1] + 1: merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else: merged.append((s, e))
    result = []
    for s, e in merged:
        bits = (e - s + 1).bit_length() - 1
        prefix = 32 - bits; result.append(f"{int2ip(s)}/{prefix}")
    return result
def cli():
    if len(sys.argv) < 2: print("Usage: cidr_merge CIDR1 CIDR2 ..."); sys.exit(1)
    for r in merge(sys.argv[1:]): print(f"  {r}")
if __name__ == "__main__": cli()

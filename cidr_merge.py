#!/usr/bin/env python3
"""cidr_merge - Merge overlapping CIDR ranges."""
import sys, struct, socket
def ip2int(ip): return struct.unpack("!I",socket.inet_aton(ip))[0]
def int2ip(n): return socket.inet_ntoa(struct.pack("!I",n))
def parse_cidr(s):
    ip,p = s.strip().split("/"); p = int(p)
    mask = (0xFFFFFFFF << (32-p)) & 0xFFFFFFFF
    return (ip2int(ip) & mask, p)
def cidr_str(net,p): return f"{int2ip(net)}/{p}"
def merge(cidrs):
    ranges = sorted(parse_cidr(c) for c in cidrs)
    merged = True
    while merged:
        merged = False; new = []
        i = 0
        while i < len(ranges):
            if i+1 < len(ranges):
                n1,p1 = ranges[i]; n2,p2 = ranges[i+1]
                size1 = 1<<(32-p1); size2 = 1<<(32-p2)
                if n1 == n2 and p1 <= p2: new.append((n1,p1)); i += 2; merged = True; continue
                if n2 >= n1 and n2+size2 <= n1+size1: new.append((n1,p1)); i += 2; merged = True; continue
                if p1 == p2 and n1 ^ n2 == size1:
                    new.append((min(n1,n2), p1-1)); i += 2; merged = True; continue
            new.append(ranges[i]); i += 1
        ranges = new
    return [cidr_str(n,p) for n,p in ranges]
if __name__ == "__main__":
    if len(sys.argv) > 1: cidrs = sys.argv[1:]
    else: cidrs = [l.strip() for l in sys.stdin if l.strip()]
    for c in merge(cidrs): print(c)

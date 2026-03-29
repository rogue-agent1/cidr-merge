#!/usr/bin/env python3
"""cidr_merge - Merge and optimize CIDR ranges."""
import sys, argparse, json, ipaddress

def merge_cidrs(cidrs):
    nets = [ipaddress.ip_network(c, strict=False) for c in cidrs]
    return [str(n) for n in ipaddress.collapse_addresses(nets)]

def expand_cidr(cidr, max_ips=256):
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = list(net.hosts())[:max_ips]
    return [str(h) for h in hosts]

def main():
    p = argparse.ArgumentParser(description="CIDR merger")
    sub = p.add_subparsers(dest="cmd")
    m = sub.add_parser("merge"); m.add_argument("cidrs", nargs="+")
    e = sub.add_parser("expand"); e.add_argument("cidr"); e.add_argument("--max", type=int, default=256)
    o = sub.add_parser("overlap"); o.add_argument("a"); o.add_argument("b")
    args = p.parse_args()
    if args.cmd == "merge":
        merged = merge_cidrs(args.cidrs)
        print(json.dumps({"input": len(args.cidrs), "merged": len(merged), "ranges": merged}))
    elif args.cmd == "expand":
        ips = expand_cidr(args.cidr, args.max)
        print(json.dumps({"cidr": args.cidr, "count": len(ips), "ips": ips}))
    elif args.cmd == "overlap":
        a = ipaddress.ip_network(args.a, strict=False)
        b = ipaddress.ip_network(args.b, strict=False)
        overlaps = a.overlaps(b)
        print(json.dumps({"a": args.a, "b": args.b, "overlaps": overlaps, "a_subnet_of_b": a.subnet_of(b), "b_subnet_of_a": b.subnet_of(a)}))
    else: p.print_help()

if __name__ == "__main__": main()

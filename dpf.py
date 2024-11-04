#!/usr/bin/python3

import sys

# field tuple constants
OFFSET = 0
LENGTH = 1

# other constants
BYTE_LEN = 8

protocol_fields = {
    "eth" :  {
        "dst_mac" : (0,48),
        "src_mac" : (48,48),
        "eth_type": (96,16)
    },
    "ipv4":  {
        "version": (0,4),
        "hdr_len": (4,4),
        "dscp"   : (8,6),
        "ecn"    : (14,2),
        "pl_len" : (16,16),
        "id"     : (32,16),
        "flags"  : (48,3),
        "frag"   : (51,13),
        "ttl"    : (64,8),
        "prot"   : (72,8),
        "hdr_cs" : (80,16),
        "src_ip" : (96,32),
        "dst_ip" : (128,32),
        "opt"    : (160,32)
    },
    "ipv6":  {
        "version"  : (0,4),
        "class"    : (4,8),
        "label"    : (12,20),
        "pl_len"   : (32,16),
        "next_hdr" : (48,8),
        "hop_lim"  : (56,8),
        "src_ip"   : (64,128),
        "dst_ip"   : (192,128)
    },
    "tcp" :  {None},
    "udp" :  {None},
    "icmp":  {None},
    "arp" :  {None},
    "dhcp":  {None},
    "dns" :  {None}
}

def compute_field_val(field_tup, hdr):
    field_val = 0 # decoded value
    pre_bits  = 0 # number of bits preceeding first byte boundary
    pre_mask  = 0 # mask for bits that preceed first byte boundary
    post_mask = 0 # mask for bits that exceed byte boundary at the end

    rem_bits = field_tup[LENGTH]             # number of bits left to decode
    byte_idx = field_tup[OFFSET] // BYTE_LEN # starting byte index

    # number of bits to decode in the first byte
    if field_tup[OFFSET] == 0 and field_tup[LENGTH] < BYTE_LEN:
        pre_bits = field_tup[LENGTH]
    else:
        pre_bits = field_tup[OFFSET] % BYTE_LEN

    # mask to extract bits leading up to first byte boundary
    pre_mask = ((1 << pre_bits ) - 1) << (BYTE_LEN - pre_bits)

    #TODO: STILL NEED TO HANDLE EDGE CASE WITH TRAFFIC CLASS!!!
    # decode bits preceding first byte boundary
    if pre_mask != 0:
        field_val = (hdr[byte_idx] & pre_mask) >> (BYTE_LEN - pre_bits)
        
        # update remaining bits and byte index
        rem_bits -= pre_bits
        byte_idx += 1

    # decode any bits that fall within byte boundaries
    while rem_bits >= BYTE_LEN:
        field_val = (field_val << 8) | hdr[byte_idx]
        rem_bits -= BYTE_LEN # reduce remaining bits
        byte_idx += 1        # increment byte index

    # decode bits following final byte boundary
    if rem_bits > 0:
        post_mask = ((1 << rem_bits) - 1) << (BYTE_LEN - rem_bits)
        field_val = (field_val << 8) | (hdr[byte_idx] & post_mask)

    return hex(field_val)

def parse_eth_hdr(field, hdr):
    return compute_field_val(protocol_fields['eth'][field], hdr)

def parse_ipv4_hdr(field, hdr):
    return compute_field_val(protocol_fields['ipv4'][field], hdr)

def parse_ipv6_hdr(field, hdr):
    return compute_field_val(protocol_fields['ipv6'][field], hdr)

if __name__ == "__main__":
    test_mac = [0x80, 0x00, 0x20, 0x7A, 0x3F, 0x3E, 0x80, 0x00, 0x20, 0x20, 0x3A, 0xAE, 0x80, 0x00]
    test_ipv4 = [0x45,0x00,0x00,0x3C,0xFE,0xFD,0x00,0x00,0x80,0x01,0xF1,0xE6,0xC0,0xA8,0x64,0x8A,0xC0,0xA8,0x64,0x01,0x08,0x00,0x14,0x5C]
    test_ipv6 = [0x60,0x00,0x00,0x00,0x00,0x20,0x3A,0xFF,0xFE,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x86,0xFF,0xFE,0x50,0x80,0xDA,0xFE,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x02,0x60,0x97,0xFF,0xFE,0x07,0x69,0xEA]
    prot = sys.argv[1]
    field = sys.argv[2]
    
    # Test functions, uncomment as needed
    #print(f'Protocol: {prot}\nHeader Field: {field}')
    if prot == 'eth':
        print(parse_eth_hdr(field, test_mac))
    elif prot == 'ipv4':
        print(parse_ipv4_hdr(field, test_ipv4))
    elif prot == 'ipv6':
        print(parse_ipv6_hdr(field, test_ipv6))

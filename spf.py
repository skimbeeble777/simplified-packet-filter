#!/usr/bin/python3

import sys

CHUNK_00 = 0
CHUNK_01 = 1
CHUNK_02 = 2
CHUNK_03 = 3
CHUNK_04 = 4
CHUNK_05 = 5
CHUNK_06 = 6
CHUNK_07 = 7
CHUNK_08 = 8
CHUNK_09 = 9

eth = {
    chunk_size: 48 # in bytes
    dst_mac:    (CHUNK_00, 0xFFFFFFFFFFFF),
    src_mac:    (CHUNK_01, 0xFFFFFFFFFFFF),
    eth_type:   (CHUNK_02, 0xFFFF)
}

ipv4 = {
    chunk_size:  32 # in bytes
    version:     (CHUNK_00, 0x0000000F),
    ihl:         (CHUNK_00, 0x000000F0),
    dscp:        (CHUNK_00, 0x00003F00),
    ecn:         (CHUNK_00, 0x0000C000),
    length:      (CHUNK_00, 0xFFFF0000),
    frag_id:     (CHUNK_01, 0x0000FFFF),
    flags:       (CHUNK_01, 0x00070000),
    frag_offset: (CHUNK_01, 0xFFF80000),
    ttl:         (CHUNK_02, 0x000000FF),
    protocol:    (CHUNK_02, 0x0000FF00),
    hdr_chksum:  (CHUNK_02, 0xFFFF0000),
    src_ip:      (CHUNK_03, 0xFFFFFFFF),
    dest_ip:     (CHUNK_04, 0xFFFFFFFF),
    options_0:   (CHUNK_05, 0xFFFFFFFF)
    options_1:   (CHUNK_06, 0xFFFFFFFF)
    options_2:   (CHUNK_07, 0xFFFFFFFF)
    options_3:   (CHUNK_08, 0xFFFFFFFF)
    options_4:   (CHUNK_09, 0xFFFFFFFF)
}

def chunkify(data, chunk_size):
    pass

def parse_eth_hdr(field, hdr):
    chunked_data = chunkify(hdr, eth['chunk_size']

def parse_ipv4_hdr(field, hdr):
    chunked_data = chunkify(hdr, ipv4['chunk_size']

if __name__ == "__main__":
    test_mac = [0x80, 0x00, 0x20, 0x7A, 0x3F, 0x3E, 0x80, 0x00, 0x20, 0x20, 0x3A, 0xAE, 0x80, 0x00]
    test_ipv4 = [0x45,0x00,0x00,0x3C,0xFE,0xFD,0x00,0x00,0x80,0x01,0xF1,0xE6,0xC0,0xA8,0x64,0x8A,0xC0,0xA8,0x64,0x01,0x08,0x00,0x14,0x5C]
    #test_ipv6 = [0x60,0x00,0x00,0x00,0x00,0x20,0x3A,0xFF,0xFE,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x86,0xFF,0xFE,0x50,0x80,0xDA,0xFE,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x02,0x60,0x97,0xFF,0xFE,0x07,0x69,0xEA]
    prot = sys.argv[1]
    field = sys.argv[2]
    
    if prot == 'eth':
        print(parse_eth_hdr(field, test_mac))
    elif prot == 'ipv4':
        print(parse_ipv4_hdr(field, test_ipv4))
    #elif prot == 'ipv6':
    #    print(parse_ipv6_hdr(field, test_ipv6))
    else:
        print("Protocol not supported.")

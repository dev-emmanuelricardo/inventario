#!/usr/bin/env python

import netsnmp

resultado = netsnmp.snmpwalk(
    'sysUpTime',
    Version = 2,
    DestHost = "localhost",
    Community = "public"
    )

print resultado

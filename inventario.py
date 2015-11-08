#!/usr/bin/env python

import netsnmp

netsnmp.snmpwalk(
    'sysUpTime',
    Version = 2,
    DestHost = "localhost",
    Community = "public"
    )


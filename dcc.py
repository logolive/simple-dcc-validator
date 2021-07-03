#!/bin/python
#    Copyright 2021 Thomas Bellebaum
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import sys
import zlib
import base64
import base45
import cbor2
from datetime import date, datetime

from cose.algorithms import Es256
from cose.headers import KID
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpX, EC2KpY, EC2KpCurve, KpKty
from cose.keys.keytype import KtyEC2
from cose.keys.curves import P256
from cose.messages import CoseMessage
from cryptography import x509

# 1. Read from STDIN
cin = sys.stdin.buffer.read().decode('ASCII')

# 2. Retrieve CBOR Web Token
## remove prefix "HC1:"
cin = cin[4:]
## base45 decoding
cin = base45.b45decode(cin)
## zlib decompression
cin = zlib.decompress(cin)
## COSE decoding
decoded = CoseMessage.decode(cin)

# 3. Verify Signature (Assumes a valid DSClist)
## find kid
kid_bin = decoded.phdr[KID] if KID in decoded.phdr.keys() else decoded.uhdr[KID]
kid = base64.b64encode(kid_bin).decode('ASCII')
## find dsc in dscList
def make_pem(key): # Format the Certificates
	return "-----BEGIN CERTIFICATE-----\n" + '\n'.join([key[i:i+64] for i in range(0,len(key),64)]) + "\n-----END CERTIFICATE-----"
dsclist = json.loads(open("DSC.json").readlines()[1])
dscdict = { dsc['kid']: {'country': dsc["country"], 'cert': make_pem(dsc["rawData"])} for dsc in dsclist["certificates"] }
if not kid in dscdict:
	raise Exception( "KeyID \""+kid+"\" is unknown -- cannot verify." )
dsc = x509.load_pem_x509_certificate(dscdict[kid]["cert"].encode('ASCII'))
## set EC parameters and verify
pub = dsc.public_key().public_numbers()
x,y = pub.x.to_bytes(32, byteorder="big"), pub.y.to_bytes(32, byteorder="big")
decoded.key = CoseKey.from_dict( { KpKty: KtyEC2, EC2KpCurve: P256, KpAlg: Es256, EC2KpX: x, EC2KpY: y, } )
if not decoded.verify_signature():
	raise Exception("faulty sig")

# 4. Format and Print Payload
payload = cbor2.loads(decoded.payload)
def json_serial(obj): # Format date and time
	if isinstance(obj, (datetime, date)):
		return obj.isoformat()
	raise TypeError ("Type %s not serializable" % type(obj))
payload[-260]=json.dumps(payload[-260][1], indent=4, sort_keys=True, default=json_serial)
claim_names = { 1 : "Issuer", 6: "Issued At", 4: "Experation time", -260 : "Health claims" }
for k in payload:
	n = claim_names[k] if k in claim_names else f'Claim {k} (unknown)'
	print(f'{n:20}: {payload[k]}')


# Simple Validator for the EU Digital COVID Certificate (DCC)

This is a VERY simple DCC Checking app designed to be as short and hackable as possible.
Based on https://github.com/ehn-dcc-development/ehn-sign-verify-python-trivial ,
but with everything unnecessary removed and altered to use the same DSCs as the german CovPass App.

### Usage

To fetch the latest DSCs valid in Germany (should be all of Europe, DO THIS REGULARLY):

```
./run.sh update
```

To validate and print the contents of an encoded DCC ("The QR-Code content", starts with "HC1:"):

```
cat your_dcc | python dcc.py
```

To scan a QR Code using zbarcam:

```
./run.sh
```

### Requirements

- Any typical Linux distribution should do
- Some Python 3 libs
  - json
  - zlib
  - base64
  - base45
  - cbor2
  - cose
  - cryptography
- ZbarCam (optional, to scan a DCC via your webcam)

### Potential Caveats

Currently assumes ECDSA for verification.
See also: https://github.com/ehn-dcc-development/ehn-sign-verify-python-trivial/issues/5

Feel free to file a pull request :)


import re
from flask import Flask, request

app = Flask(__name__)


def generate_whitelist():
    whitelist = []
    with open('/usr/src/app/whitelist.txt', 'r') as f:
        for line in f.readlines():
            if line.strip().endswith('d.wott.local'):
                whitelist.append(line.strip())
    return whitelist


def was_client_certification_verification_ok(headers):
    """
    Verifies that client certificate verification passed.
    """
    return headers.get('Ssl-Client-Verify') == 'SUCCESS'


def grant_client_access(headers):
    """
    Verifies and grants client access if it is is present in the whitelist.
    """

    client_cert = headers.get('Ssl-Client-Subject-Dn')

    whitelist = generate_whitelist()
    print('Device whitelist: {}'.format(whitelist))

    print('Got request from: {}'.format(client_cert))

    # Extract the Common Name from the certificate
    matchObj = re.match(
        r'.*CN=(.*.d.wott.local)',
        client_cert,
        re.M | re.I
    )

    print('Got request from {}'.format(matchObj.group(1)))

    # Match the device against the whitelist
    if matchObj.group(1) in whitelist:
        print('{} found in whitelist'.format(matchObj.group(1)))
        return True

    return False


@app.route('/')
def mtls_example():

    if not was_client_certification_verification_ok(request.headers):
        return 'No client certificate provided. Access denied.\n'

    if grant_client_access(request.headers):
        return 'Access granted!\n'
    else:
        return 'Access denied!\n'

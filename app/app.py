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


def is_was_client_cerify_ok(headers):
    """
    Verifies that client certificate verification passed.
    """
    return headers.get('Ssl-Client-Verify') == 'SUCCESS'


def grant_client_access(headers):
    """
    Verifies and grants client access if it is is present in the whitelist.
    """

    for h in headers:
        print('Header: {}'.format(h))

    whitelist = generate_whitelist()
    print('Device whitelist: {}'.format(whitelist))


    print('Got request from: {}'.format(headers.get('Ssl-Client')))

    # Extract the Common Name from the certificate
    matchObj = re.match(
        r'.*CN=(.*.d.wott.local)',
        headers.get('Ssl-Client'),
        re.M | re.I
    )

    print('Got request from {}'.format(matchObj.group(1)))

    # Match the device against the whitelist
    if matchObj.group(1) in whitelist:
        print('{} found in whitelist'.format(matchObj.group(1)))
        return True

    return False


@app.route('/')
def hello_world():

    if not is_was_client_cerify_ok(request.headers):
        return 'No client certificate provided. Access denied.'

    if grant_client_access(request.headers):
        return 'Access granted!\n'
    else:
        return 'Access denied!\n'

"""
Device authentication feature.
Usage example:
    python accesstoken.py \\
      --project_id=my-project-id \\
      --registry_id=my-registry-id \\
      --device_id=my-device-id \\
      --private_key_file=./resources/rsa_private.pem \\
      --algorithm=RS256 \\
      generate-access-token
"""

import argparse
import base64
from datetime import datetime, timedelta
import io
import json
import os
import time

from google.cloud import pubsub
from google.cloud import storage
import jwt
import requests as req


def create_jwt(project_id, algorithm, private_key_file):
    """Generate Cloud IoT device jwt token."""
    jwt_payload = '{{"iat":{},"exp":{},"aud":"{}"}}'.format(
        time.time(),
        time.mktime((datetime.now() + timedelta(hours=6)).timetuple()),
        project_id,
    )
    private_key_bytes = ""
    with io.open(private_key_file) as f:
        private_key_bytes = f.read()
    encoded_jwt = jwt.encode(
        json.loads(jwt_payload), private_key_bytes, algorithm=algorithm
    )
    return encoded_jwt.decode() if isinstance(encoded_jwt, bytes) else encoded_jwt


def generate_access_token(project_id, registry_id, device_id, algorithm, private_key_file):
    """Generates Access Token
    # project_id = 'YOUR_PROJECT_ID'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # algorithm = 'RS256'
    # private_key_file = 'path/to/private_key.pem'
    """
    jwt = create_jwt(project_id, algorithm, private_key_file)

    # Generate OAuth 2.0 access token. See https://developers.google.com/identity/protocols/oauth2
    resource_path = "projects/{}/registries/{}/devices/{}".format(
        project_id, registry_id, device_id
    )
    request_url = "https://cloudiottoken.googleapis.com/v1beta1/{}:generateAccessToken".format(
        resource_path
    )
    headers = {"authorization": "Bearer {}".format(jwt)}
    request_payload = {"device": resource_path}
    resp = req.post(url=request_url, data=request_payload, headers=headers)
    assert resp.ok, resp.raise_for_status()
    access_token = resp.json()["access_token"]
    return access_token

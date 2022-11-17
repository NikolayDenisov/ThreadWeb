"""
The device manager to administer devices.
Usage example:
    python manager.py \\
      --project_id=my-project-id \\
      list-registries
"""

from .device_manager import DeviceManagerClient


class GatewayType:
    pass


class GatewayAuthMethod:
    pass


def create_device(project_id, registry_id, device_id):
    """Create a device to bind to a gateway if it does not exist."""
    # Check that the device doesn't already exist
    client = DeviceManagerClient()

    exists = False

    parent = client.registry_path(project_id, registry_id)

    devices = list(client.list_devices(request={"parent": parent}))

    for device in devices:
        if device.id == device_id:
            exists = True

    # Create the device
    device_template = {
        "id": device_id,
        "gateway_config": {
            "gateway_type": GatewayType.NON_GATEWAY,
            "gateway_auth_method": GatewayAuthMethod.ASSOCIATION_ONLY,
        },
    }

    if not exists:
        res = client.create_device(
            request={"parent": parent, "device": device_template}
        )
        print("Created Device {}".format(res))
    else:
        print("Device exists, skipping")


def create_unauth_device(project_id, registry_id, device_id):
    """Create a new device without authentication."""
    client = DeviceManagerClient()
    parent = client.registry_path(project_id, registry_id)
    device_template = {
        "id": device_id,
    }
    return client.create_device(request={"parent": parent, "device": device_template})


def delete_device(project_id, registry_id, device_id):
    """Delete the device with the given id."""
    client = DeviceManagerClient()
    device_path = client.device_path(project_id, registry_id, device_id)
    return client.delete_device(request={"name": device_path})


def delete_registry(service_account_json, project_id, cloud_region, registry_id):
    """Deletes the specified registry."""
    client = DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)
    try:
        client.delete_device_registry(request={"name": registry_path})
        return "Registry deleted"
    except HttpError:
        print("Error, registry not deleted")
        raise


def get_device(project_id, registry_id, device_id):
    """Retrieve the device with the given id."""
    client = DeviceManagerClient()
    device_path = client.device_path(project_id, registry_id, device_id)

    field_mask = gp_field_mask.FieldMask(
        paths=[
            "id",
            "name",
            "num_id",
            "credentials",
            "last_heartbeat_time",
            "last_event_time",
            "last_state_time",
            "last_config_ack_time",
            "last_config_send_time",
            "blocked",
            "last_error_time",
            "last_error_status",
            "config",
            "state",
            "log_level",
            "metadata",
            "gateway_config",
        ]
    )

    device = client.get_device(request={"name": device_path, "field_mask": field_mask})

    print("Id : {}".format(device.id))
    print("Name : {}".format(device.name))
    print("Credentials:")

    if device.credentials is not None:
        for credential in device.credentials:
            keyinfo = credential.public_key
            print("\tcertificate: \n{}".format(keyinfo.key))

            if keyinfo.format == 4:
                keyformat = "ES256_X509_PEM"
            elif keyinfo.format == 3:
                keyformat = "RSA_PEM"
            elif keyinfo.format == 2:
                keyformat = "ES256_PEM"
            elif keyinfo.format == 1:
                keyformat = "RSA_X509_PEM"
            else:
                keyformat = "UNSPECIFIED_PUBLIC_KEY_FORMAT"
            print("\tformat : {}".format(keyformat))
            print("\texpiration: {}".format(credential.expiration_time))

    print("Config:")
    print("\tdata: {}".format(device.config.binary_data))
    print("\tversion: {}".format(device.config.version))
    print("\tcloudUpdateTime: {}".format(device.config.cloud_update_time))

    return device


def get_state(project_id, registry_id, device_id):
    """Retrieve a device's state blobs."""
    client = DeviceManagerClient()
    device_path = client.device_path(project_id, registry_id, device_id)

    device = client.get_device(request={"name": device_path})
    print("Last state: {}".format(device.state))

    print("State history")
    states = client.list_device_states(request={"name": device_path}).device_states
    for state in states:
        print("State: {}".format(state))
    return states


def list_devices(project_id, registry_id):
    """List all devices in the registry."""
    print("Listing devices")

    client = DeviceManagerClient()
    registry_path = client.registry_path(project_id, registry_id)

    field_mask = gp_field_mask.FieldMask(
        paths=[
            "id",
            "name",
            "num_id",
            "credentials",
            "last_heartbeat_time",
            "last_event_time",
            "last_state_time",
            "last_config_ack_time",
            "last_config_send_time",
            "blocked",
            "last_error_time",
            "last_error_status",
            "config",
            "state",
            "log_level",
            "metadata",
            "gateway_config",
        ]
    )

    devices = list(
        client.list_devices(request={"parent": registry_path, "field_mask": field_mask})
    )
    for device in devices:
        print(device)

    return devices


def list_registries(project_id):
    """List all registries in the project."""
    client = DeviceManagerClient()
    parent = f"projects/{project_id}"

    registries = list(client.list_device_registries(request={"parent": parent}))
    for registry in registries:
        print("id: {}\n\tname: {}".format(registry.id, registry.name))

    return registries


def create_registry(project_id, registry_id):
    """Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    client = DeviceManagerClient()
    parent = f"projects/{project_id}"

    body = {
        "event_notification_configs": [{"pubsub_topic_name": pubsub_topic}],
        "id": registry_id,
    }

    try:
        response = client.create_device_registry(
            request={"parent": parent, "device_registry": body}
        )
        print("Created registry")
        return response
    except HttpError:
        print("Error, registry not created")
        raise
    except AlreadyExists:
        print("Error, registry already exists")
        raise
    # [END iot_create_registry]


def get_registry(project_id, registry_id):
    """ Retrieves a device registry."""
    client = DeviceManagerClient()
    registry_path = client.registry_path(project_id, registry_id)

    return client.get_device_registry(request={"name": registry_path})


def get_iam_permissions(project_id, registry_id):
    """Retrieves IAM permissions for the given registry."""
    client = DeviceManagerClient()

    registry_path = client.registry_path(project_id, registry_id)

    policy = client.get_iam_policy(request={"resource": registry_path})

    return policy


def set_iam_permissions(project_id, registry_id, role, member):
    """Sets IAM permissions for the given registry to a single role/member."""
    # role = 'viewer'
    # member = 'group:dpebot@google.com'
    client = DeviceManagerClient()
    registry_path = client.registry_path(project_id, registry_id)

    body = {"bindings": [{"members": [member], "role": role}]}

    return client.set_iam_policy(request={"resource": registry_path, "policy": body})


def send_command(project_id, registry_id, device_id, command):
    """Send a command to a device."""
    # [START iot_send_command]
    print("Sending command to device")
    client = DeviceManagerClient()
    device_path = client.device_path(project_id, registry_id, device_id)

    # command = 'Hello IoT Core!'
    data = command.encode("utf-8")

    return client.send_command_to_device(
        request={"name": device_path, "binary_data": data}
    )
    # [END iot_send_command]

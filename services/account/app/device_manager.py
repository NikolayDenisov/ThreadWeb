class DeviceManagerClient:
    """
    Internet of Things (IoT) service. Securely connect and manage
    IoT devices.
    """

    @staticmethod
    def device_path(project: str, registry: str, device: str) -> str:
        """Returns a fully-qualified device string."""
        return "projects/{project}/registries/{registry}/devices/{device}".format(
            project=project,
            registry=registry,
            device=device,
        )

    def __init__(self) -> None:
        pass

    def create_device_registry(self, device_registry):
        pass

    def get_device_registry(self):
        pass

    def delete_device_registry(self):
        pass

    def list_device_registries(self):
        pass

    def create_device(self, parent, device): pass

    def update_device(self, device, update_mask): pass

    def delete_device(self, name): pass

    def list_devices(self, parent): pass

    def list_device_states(self): pass

    def set_iam_policy(self): pass

    def get_iam_policy(self): pass

    def send_command_to_device(self, name: str = None, binary_data: bytes = None): pass

from twABCs.controller import Controller


class Odometry(Controller):

    def __init__(self):
        pass

    def register_sensor(self, sensor, name) -> bool:
        pass

    def receive_data(self, data, device_code) -> bool:
        pass

    def check_devices(self) -> bool:
        pass

    async def _process_outgoing_data(self) -> bool:
        pass

    async def _get_next_outgoing_packet(self) -> str or bool:
        pass

    def _run(self) -> bool:
        pass

    def run(self) -> bool:
        pass

    def stop(self) -> bool:
        pass
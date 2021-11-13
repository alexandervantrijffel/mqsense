import time
from typing import NamedTuple
import paho.mqtt.client as mqtt
from mqsense.utils.log import LogMixin


class ConnectionDetails(NamedTuple):
    host: str
    user: str
    password: str
    clientId: str = "mqsense"
    port: int = 1883


class MQTTClient(LogMixin):
    def connect(self, connectionDetails: ConnectionDetails, userdata: dict) -> None:
        try:
            self.log.info(
                "Connecting to MQTT broker",
                host=connectionDetails.host,
                clientId=connectionDetails.clientId,
            )
            self.client = mqtt.Client(
                connectionDetails.host,
                transport="tcp",  # or transport="websockets"
                userdata=userdata,
            )
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_log = self.on_log
            self.client.username_pw_set(connectionDetails.user, connectionDetails.password)
            self.client.connect(connectionDetails.host, connectionDetails.port)
            self.log.debug("Waiting for connection")
            while not self.client.is_connected():
                self.client.loop()
                time.sleep(0.1)
            self.log.debug("Connected")
        except Exception as e:
            self.log.error("Unknown error while initializing Paho MQTT client", exception=str(e))

    def subscribe(self, connectionDetails: ConnectionDetails, topic: str) -> None:
        """connects to the MQTT broker and subscribes to the given topics.
        This is a blocking method"""
        try:
            self.connect(connectionDetails, userdata={"sub_topic": topic})

            self.log.info("Subscribing to topic", topic=topic)
            self.log.info("Press CTRL+C to cancel")

            self.client.subscribe(topic, 0)
            self.client.loop_forever(retry_first_connection=True)
        except KeyboardInterrupt:
            self.log.debug("Got keyboard interrupt. Stopping the Paho loop.")
        except Exception as e:
            self.log.error("Unknown error in subscription", exception=str(e))
            raise
        self.client.disconnect()

    def on_connect(self, client, userdata: dict, flags, rc) -> None:  # noqa: ANN001
        self.log.debug("MQTT:connected", return_code=str(rc))
        if "sub_topic" in userdata:
            client.subscribe(userdata["sub_topic"])

    def publish(self, connectionDetails: ConnectionDetails, topic: str, message: object) -> None:
        try:
            self.connect(connectionDetails, {})
            self.log.info(
                "Publishing message",
                topic=topic,
                message=message,
            )
            handle = self.client.publish(topic, message, qos=0, retain=True)
            handle.wait_for_publish()
        except Exception as e:
            self.log.error("Unknown error in publish", exception=str(e))
            raise

    def on_message(self, client, userdata: dict, message) -> None:  # noqa: ANN001
        self.log.info(
            "MQTT:RECV",
            message=str(message.payload.decode("utf-8")),
            topic=message.topic,
            qos=message.qos,
            retain=message.retain,
        )

    def on_log(self, client, userdata: dict, level, buf) -> None:  # noqa: ANN001
        self.log.debug("MQTT:LOG", buf=buf)

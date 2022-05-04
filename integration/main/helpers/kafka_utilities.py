import multiprocessing
import time

from kafka import KafkaConsumer

from integration.main.logger import log


class Consumer(multiprocessing.Process):
    BOOTSTRAP_SERVERS = 'us4-kafka:9092'

    def __init__(self, topic):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.topic = topic

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=Consumer.BOOTSTRAP_SERVERS,
                                 auto_offset_reset='latest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe([self.topic])

        while not self.stop_event.is_set():
            for message in consumer:
                log.info(message.value)
                if self.stop_event.is_set():
                    break

        consumer.close()


def main(topic):
    kafka_consumer = Consumer(topic)

    kafka_consumer.start()

    time.sleep(30)

    kafka_consumer.stop()


if __name__ == "__main__":
    main('Authenticate')

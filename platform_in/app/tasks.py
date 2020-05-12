import time
import json
import logging
from confluent_kafka import Producer, avro
from flask import current_app
from confluent_kafka.avro import AvroProducer
from app import elastic_apm
import logging


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def get_kafka_producer():
    return Producer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
        }
    )


def create_task_produce_to_kafka(data):

    kafka_producer = get_kafka_producer()

    try:
        kafka_producer.produce(
            "test.sputhan.finest.testnoise", json.dumps(data), callback=delivery_report
        )
        logger.debug("Kafka Produce")
        kafka_producer.poll(2)
        if len(kafka_producer) != 0:
            return False
    except BufferError:
        logging.error("local buffer full", len(kafka_producer))
        return False
    except Exception as e:
        logging.error(e)
        return False

    return True


def create_task_produce_avro_to_kafka(data):

    value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

    value_schema = avro.loads(value_schema_str)
    value = {"name": "Value"}

    avroProducer = AvroProducer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
            "on_delivery": delivery_report,
            "schema.registry.url": "https://kafka01.fvh.fi:8081",
        },
        default_value_schema=value_schema,
    )

    try:
        avroProducer.produce(topic="test.sputhan.finest.testnoise", value=value)
        logging.debug("avro produce")
        avroProducer.poll(2)
        if len(avroProducer) != 0:
            return False
    except BufferError:
        logging.error("local buffer full", len(avroProducer))
        return False
    except Exception as e:
        logging.error(e)
        return False

    return True


def create_task_push_sentilo_noise_data(data):

    kafka_producer = get_kafka_producer()

    try:
        data_streams = data["sensors"]
        topic_prefix = "test.sputhan.finest.cesva.v1.noise.sentilo"

        for data_stream in data_streams:
            topic = data_stream["sensor"]
            observations = data_stream["observations"]
            kafka_producer.produce(
                f"{topic_prefix}.{topic}", json.dumps(observations), callback=delivery_report
            )
            kafka_producer.poll(2)
    except BufferError:
        logging.error("local buffer full", len(kafka_producer))
        elastic_apm.capture_exception()
        return False
    except Exception as e:
        elastic_apm.capture_exception()
        logging.error(e)
        return False


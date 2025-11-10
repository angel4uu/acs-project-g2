import pika
import time
import schedule
from threading import Thread
from . import constants
from .scheduler import message_callback


def start_rabbitmq_listener():
    """
    Initialize RabbitMQ listener to process messages from the queue.
    """
    # RabbitMQ credentials
    credentials = pika.PlainCredentials(
        constants.RABBITMQ_USER, constants.RABBITMQ_PASS
    )

    # Connection parameters
    connection_params = pika.ConnectionParameters(
        host=constants.RABBITMQ_HOST, credentials=credentials
    )

    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(connection_params)
        except pika.exceptions.AMQPConnectionError:
            print(f"Esperando a RabbitMQ en '{constants.RABBITMQ_HOST}'...")
            time.sleep(5)

    print(f"Conectado a RabbitMQ en '{constants.RABBITMQ_HOST}'.")
    channel = connection.channel()

    # Define queue
    channel.queue_declare(queue="create_event", durable=True)

    # Start consuming messages
    channel.basic_consume(queue="create_event", on_message_callback=message_callback)

    print("[Worker] Esperando mensajes. Presiona CTRL+C para salir.")
    channel.start_consuming()


def start_scheduler():
    """
    Scheduler Management
    """

    print("[Scheduler] Programador de tareas iniciado.")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Initiate the scheduler in a separate thread
    scheduler_thread = Thread(target=start_scheduler)
    scheduler_thread.start()

    # Initiate the RabbitMQ consumer in the main thread
    start_rabbitmq_listener()

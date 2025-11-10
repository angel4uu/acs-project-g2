import traceback


def message_callback(ch, method, properties, body):
    """
    Callback for the 'create_event' queue
    """
    print(f"[Worker] Mensaje recibido (delivery_tag={method.delivery_tag}): {body}")

    try:
        pass  # Tu lógica va aquí

        print(f"[Worker] Mensaje procesado exitosamente.")

    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        traceback.print_exc()

    finally:
        # Confirma a RabbitMQ que terminaste de procesar este mensaje.
        ch.basic_ack(delivery_tag=method.delivery_tag)

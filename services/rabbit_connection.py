import os

import aio_pika
import json
from dotenv import load_dotenv

load_dotenv()

RABURL = os.getenv('RABBIT_URL')

async def send_to_rabbitmq(report_data: dict):
    connection = await aio_pika.connect_robust(RABURL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(report_data).encode()
            ),
            routing_key="report_notifications",
        )
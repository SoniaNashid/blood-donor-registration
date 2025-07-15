4. worker-service/ ⚙️
Handles asynchronous tasks.

Background jobs like:

Sending SMS or email to matching donors.

Cleaning up expired requests.

Periodic index updates.

💡 Use Celery or a message broker (like RabbitMQ or Redis) for queueing.

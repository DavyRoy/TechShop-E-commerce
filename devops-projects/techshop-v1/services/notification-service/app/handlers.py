from app.email_sender import (
    send_order_confirmation,
    send_order_update,
    send_order_cancellation,
)


def on_order_created(data: dict):
    """
    Event handler: order.created
    """
    order_id = data.get("order_id")
    user_id = data.get("user_id")

    if not order_id or not user_id:
        print("[ERROR] Missing order_id or user_id in event")
        return

    send_order_confirmation(order_id, user_id)


def on_order_updated(data: dict):
    """
    Event handler: order.updated
    """
    order_id = data.get("order_id")
    status = data.get("status")

    if not order_id or not status:
        print("[ERROR] Missing order_id or status in event")
        return

    send_order_update(order_id, status)


def on_order_cancelled(data: dict):
    """
    Event handler: order.cancelled
    """
    order_id = data.get("order_id")

    if not order_id:
        print("[ERROR] Missing order_id in event")
        return

    send_order_cancellation(order_id)
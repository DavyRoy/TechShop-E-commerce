import logging

logger = logging.getLogger(__name__)


def send_order_confirmation(order_id: str, user_id: str) -> None:
    """
    Send confirmation notification when order is created.
    """
    logger.info(
        "Order confirmation sent",
        extra={
            "event": "order_confirmation",
            "order_id": order_id,
            "user_id": user_id,
        },
    )


def send_order_update(order_id: str, status: str) -> None:
    """
    Notify user that order status has changed.
    """
    logger.info(
        "Order status updated",
        extra={
            "event": "order_status_update",
            "order_id": order_id,
            "status": status,
        },
    )


def send_order_cancellation(order_id: str) -> None:
    """
    Notify user that order has been cancelled.
    """
    logger.info(
        "Order cancelled",
        extra={
            "event": "order_cancelled",
            "order_id": order_id,
        },
    )
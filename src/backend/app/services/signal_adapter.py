import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class SignalAdapter:
    """Adapter Signal utilisant un bridge HTTP local."""

    def __init__(self):
        self.bridge_url = settings.signal_bridge_url

    def send_message(self, to: str, body: str) -> bool:
        try:
            response = httpx.post(
                f"{self.bridge_url}/send",
                json={"to": to, "message": body},
                timeout=10.0
            )
            if response.status_code == 200:
                logger.info(f"Message envoyé à {to}")
                return True
            else:
                logger.error(f"Bridge erreur: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Bridge exception: {e}")
            return False
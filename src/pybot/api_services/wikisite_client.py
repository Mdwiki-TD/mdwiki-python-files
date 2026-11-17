"""Helpers for creating OAuth-authenticated MediaWiki clients."""

from __future__ import annotations

import logging
import os

import requests
from mwclient.client import Site

logger = logging.getLogger(__name__)


class WikiSiteClient:
    """Helper for creating OAuth-authenticated MediaWiki clients."""

    @staticmethod
    def get_site(domain: str) -> Site | None:

        user_agent = os.getenv(
            "USER_AGENT",
            "mdwiki/1.0 (https://mdwiki.toolforge.org; tools.mdwiki@toolforge.org)",
        )
        try:
            site = Site(
                domain,
                scheme="https",
                clients_useragent=user_agent,
                force_login=False,
            )
        except requests.exceptions.ReadTimeout as exc:  # pragma: no cover - network interaction
            logger.error(f"Failed to build OAuth site, {str(exc)}")
            return None
        except requests.exceptions.ConnectionError:  # pragma: no cover - network interaction
            logger.error("Failed to build OAuth site, connection error")
            return None
        except Exception as exc:  # pragma: no cover - network interaction
            logger.exception("Failed to build OAuth site", exc_info=exc)
            return None
        return site


__all__ = [
    "WikiSiteClient",
]

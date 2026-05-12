"""
MediaWiki Account Credentials Module.

SECURITY WARNING:
    This module loads credentials from environment variables or configuration
    files. Never hardcode credentials in source code.

    If you're seeing this file after a security update, you MUST:
    1. Rotate all exposed credentials immediately
    2. Add credential files to .gitignore
    3. Use environment variables or secure vaults for production

Usage:
    Credentials are loaded from (in order of precedence):
    1. Environment variables: MDWIKI_USERNAME, MDWIKI_PASSWORD
    2. Environment variables: MDWIKI_CX_USERNAME, MDWIKI_CX_PASSWORD
    3. Configuration file: ~/.config/mdwiki/credentials.ini

    Example credentials.ini:

        [mdwiki]
        username = YourUsername
        password = Yourbot_password

        [mdwiki_cx]
        username = YourCxUsername
        password = YourCxPassword

Configuration:
    Set credentials via environment variables (recommended for CI/CD):

        export MDWIKI_USERNAME="YourUsername"
        export MDWIKI_PASSWORD="Yourbot_password@suffix"

Example:
    from copy_to_en.bots.medwiki_account import username, password

    # Use credentials for API authentication
    api.login(username, password)

Note:
    Bot passwords should be generated via Special:bot_passwords on the wiki
    and have only the minimum required permissions.
"""

from __future__ import annotations

import logging
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION PATHS
# =============================================================================

_CONFIG_DIR: Path = Path.home() / ".config" / "mdwiki"
_CREDENTIALS_FILE: Path = _CONFIG_DIR / "credentials.ini"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _load_config() -> ConfigParser:
    """Load credentials from configuration file.

    Returns:
        ConfigParser instance, empty if file doesn't exist.
    """
    config = ConfigParser()
    if _CREDENTIALS_FILE.exists():
        config.read(_CREDENTIALS_FILE)
        logger.debug(f"Loaded credentials from {_CREDENTIALS_FILE}")
    return config


def _get_credential(
    env_var: str,
    config_section: str,
    config_key: str,
    config: ConfigParser,
) -> Optional[str]:
    """Get a credential from environment or config file.

    Args:
        env_var: Name of environment variable to check first.
        config_section: Section name in config file.
        config_key: Key name in config section.
        config: ConfigParser instance.

    Returns:
        The credential value, or None if not found.
    """
    # First check environment variable
    value = os.getenv(env_var)
    if value:
        return value

    # Then check config file
    try:
        return config.get(config_section, config_key)
    except Exception:
        return None


def _get_required_credential(
    env_var: str,
    config_section: str,
    config_key: str,
    config: ConfigParser,
    name: str,
) -> str:
    """Get a required credential, raising error if not found.

    Args:
        env_var: Name of environment variable.
        config_section: Section name in config file.
        config_key: Key name in config section.
        config: ConfigParser instance.
        name: Human-readable name for error messages.

    Returns:
        The credential value.

    Raises:
        ValueError: If credential is not configured.
    """
    value = _get_credential(env_var, config_section, config_key, config)
    if not value:
        raise ValueError(
            f"{name} not configured. Set {env_var} environment variable "
            f"or add [{config_section}] {config_key} to {_CREDENTIALS_FILE}"
        )
    return value


# =============================================================================
# LOAD CREDENTIALS
# =============================================================================

_config = _load_config()

# Primary MDWiki account credentials
# Set via: MDWIKI_USERNAME and MDWIKI_PASSWORD environment variables
# Or in credentials.ini: [mdwiki] section
try:
    username: str = _get_required_credential(
        "MDWIKI_USERNAME",
        "mdwiki",
        "username",
        _config,
        "MDWiki username",
    )
    password: str = _get_required_credential(
        "MDWIKI_PASSWORD",
        "mdwiki",
        "password",
        _config,
        "MDWiki password",
    )
except ValueError as e:
    logger.warning(f"MDWiki credentials not configured: {e}")
    username = ""
    password = ""

# Content translation account credentials
# Set via: MDWIKI_CX_USERNAME and MDWIKI_CX_PASSWORD environment variables
# Or in credentials.ini: [mdwiki_cx] section
try:
    username_cx: str = _get_required_credential(
        "MDWIKI_CX_USERNAME",
        "mdwiki_cx",
        "username",
        _config,
        "MDWiki CX username",
    )
    password_cx: str = _get_required_credential(
        "MDWIKI_CX_PASSWORD",
        "mdwiki_cx",
        "password",
        _config,
        "MDWiki CX password",
    )
except ValueError as e:
    logger.warning(f"MDWiki CX credentials not configured: {e}")
    username_cx = ""
    password_cx = ""


# =============================================================================
# VALIDATION
# =============================================================================


def validate_credentials() -> Dict[str, bool]:
    """Check which credential sets are properly configured.

    Returns:
        Dictionary with keys 'mdwiki' and 'mdwiki_cx' indicating
        whether each set is configured.
    """
    return {
        "mdwiki": bool(username and password),
        "mdwiki_cx": bool(username_cx and password_cx),
    }


def get_credentials_status() -> str:
    """Get a human-readable status of credential configuration.

    Returns:
        Status string describing which credentials are configured.
    """
    status = validate_credentials()
    parts = []

    if status["mdwiki"]:
        parts.append("MDWiki: configured")
    else:
        parts.append("MDWiki: NOT CONFIGURED")

    if status["mdwiki_cx"]:
        parts.append("MDWiki CX: configured")
    else:
        parts.append("MDWiki CX: NOT CONFIGURED")

    return " | ".join(parts)


# Log status on module load
logger.info(f"Credentials status: {get_credentials_status()}")

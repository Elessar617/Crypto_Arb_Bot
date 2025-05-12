# src/crypto_arb_bot/credentials.py
"""
Credentials retrieval for Crypto-Arb-Bot.

Adheres to:
 - NASA Req IDs: REQ-03 (secure API key retrieval), REQ-04 (validation)
 - Power-of-Ten: single-dereference calls, fixed behavior, no recursion
 - UNIX: single responsibility, pure-function interface
"""
import os
from typing import Optional

import keyring


class CredentialError(Exception):
    """Raised when credentials cannot be found or are invalid.
    
    This exception is raised when credentials are missing or inaccessible
    in both the system keyring and environment variables.
    """
    def __init__(self, message: str) -> None:
        """Initialize with error message.
        
        Args:
            message: Description of the credential error
        """
        self.message = message
        super().__init__(message)


def get_api_key(service_name: str) -> str:
    """
    Retrieve the API key for the given service.
    
    This function implements a secure credential retrieval system that avoids
    plaintext storage. It first checks the system keyring for credentials,
    then falls back to environment variables if needed.
    
    Args:
        service_name: Name of the service/exchange to retrieve credentials for
                     (e.g., "coinbase", "kraken")
    
    Lookup order:
      1. OS keyring under "arbbot" service
      2. Environment variable named SERVICE_NAME (uppercased)
    
    Returns:
        The API key as a non-empty string
    
    Raises:
        CredentialError: If no key is found in keyring or environment
        AssertionError: If service_name is invalid or retrieved key is wrong type
    
    NASA Requirements:
        REQ-03: Secure credential retrieval
        REQ-04: Validate service name and credential format
    """
    
    # Assertion 1: service_name must be a non-empty string
    assert isinstance(service_name, str) and service_name, "service_name must be a non-empty string"
    # Try keyring
    key = keyring.get_password("arbbot", service_name)
    # Fallback to env var
    if not key:
        key = os.getenv(service_name.upper())
    # Assertion 2: key must be a string
    assert key is None or isinstance(key, str), "retrieved key must be a string or None"
    if not key:
        raise CredentialError(f"API key for '{service_name}' not found in keyring or environment")
    return key

# EOF


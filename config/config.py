# config/config.py
"""
Configuration loader for Crypto-Arb-Bot

Adheres to:
 - NASA Req IDs: REQ-01 (load config), REQ-02 (validate fields)
 - Power-of-Ten: fixed-bounds checks, minimal dynamic allocation
 - UNIX: single responsibility, pure interfaces
"""
from dataclasses import dataclass
import toml
import os
from typing import Any, Dict, Optional, Union

CONFIG_PATH_ENV = "ARBBOT_CONFIG"
DEFAULT_CONFIG_FILE = os.path.join(os.getcwd(), "config.toml")


class ConfigError(Exception):
    """Raised when configuration load or validation fails."""
    pass


@dataclass(frozen=True)
class Config:
    market_pairs: list[str]
    max_cycles: int
    fetch_interval: float
    min_spread: float
    max_retries: int


def _read_config_file(path: str) -> Dict[str, Any]:
    """Read and parse the TOML file at given path."""
    if not os.path.isfile(path):
        raise ConfigError(f"Config file not found: {path}")  # REQ-02a
    try:
        return toml.load(path)
    except Exception as e:
        raise ConfigError(f"Failed to parse config ({path}): {e}")


def _validate_config(data: Dict[str, Any]) -> Config:
    """Validate raw config data and return a Config object."""
    # Extract raw values
    pairs = data.get("market_pairs")
    cycles = data.get("max_cycles")
    interval = data.get("fetch_interval")
    spread = data.get("min_spread")
    retries = data.get("max_retries")

    # Assertions: two or more checks on inputs
    if not isinstance(pairs, list) or not pairs:
        raise ConfigError("market_pairs must be a non-empty list")  # REQ-02b
    if not isinstance(cycles, int) or not (1 <= cycles <= 10_000):
        raise ConfigError("max_cycles must be an integer between 1 and 10000")
    if not isinstance(interval, (int, float)) or interval <= 0:
        raise ConfigError("fetch_interval must be a positive number")
    if not isinstance(spread, (int, float)) or spread < 0:
        raise ConfigError("min_spread must be >= 0")
    if not isinstance(retries, int) or not (1 <= retries <= 100):
        raise ConfigError("max_retries must be an integer between 1 and 100")

    return Config(
        market_pairs=pairs,
        max_cycles=cycles,
        fetch_interval=float(interval),
        min_spread=float(spread),
        max_retries=retries,
    )


def load_config(path: Optional[str] = None) -> Config:
    """
    Load configuration from file, validate it, and return Config.

    Args:
        path: Optional path to TOML config. Falls back to env var or default.

    Returns:
        Config: validated configuration.

    Raises:
        ConfigError: on missing file or validation failure.
    """
    cfg_path = path or os.getenv(CONFIG_PATH_ENV) or DEFAULT_CONFIG_FILE
    raw = _read_config_file(cfg_path)
    return _validate_config(raw)

# EOF



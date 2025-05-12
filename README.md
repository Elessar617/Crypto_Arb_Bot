# Crypto Arbitrage Bot

[![CI Status](https://github.com/Elessar617/Crypto_Arb_Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/Elessar617/Crypto_Arb_Bot/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/Elessar617/Crypto_Arb_Bot/branch/main/graph/badge.svg)](https://codecov.io/gh/Elessar617/Crypto_Arb_Bot)

A high-performance cryptocurrency arbitrage bot that follows NASA coding standards, UNIX philosophy, and The Power of 10 Rules for robust, reliable operation.

## Overview

This application monitors cryptocurrency exchanges to identify and execute profitable arbitrage opportunities across four major exchanges (Coinbase, Kraken, Gemini, Bitstamp). It implements a modular, secure architecture with comprehensive error handling, input validation, and defensive programming.

### Core Functionality

1. **Price Data Fetching**: Asynchronously fetch market data from multiple exchanges with pre-allocated buffers and proper timeout handling
2. **Arbitrage Scanning**: Identify price differentials that exceed profit thresholds after accounting for fees and slippage
3. **Trade Execution**: Execute profitable trades with bounded retry logic and proper error handling
4. **System Monitoring**: Health checks and performance metrics throughout the execution pipeline

## Key Features

- **Real-time market monitoring** across multiple exchanges (Coinbase, Kraken, Gemini, Bitstamp)
- **Secure credential management** with proper encryption
- **Robust error handling** with automatic recovery mechanisms
- **Comprehensive logging** for tracking performance and debugging
- **Type safety** throughout the codebase with strict mypy validation
- **Extensive test coverage** (>90%) including edge and error cases
- **Resource cleanup** in all execution paths

## Development Standards

This project adheres to strict engineering principles to ensure reliability, maintainability, and security.

### Key Principles & Implementation Mapping

| Principle | Concrete Practice |
|-----------|-------------------|
| **NASA Standards** | • Every function ≤60 lines + docstring linking to requirement ID<br>• ≥2 `assert` per function (inputs & outputs)<br>• Explicit exception handling—no silent catches |
| **UNIX Philosophy** | • `cli.py` exposes small commands (scan, execute, healthcheck)<br>• Modules importable as library ("do one thing")<br>• I/O via std streams (JSON lines, CSV, exit codes) |
| **Power of Ten Rules** | • No recursion; all loops `for … in range(N)` or over fixed collections<br>• Pre-allocate lists/deques in hot paths<br>• No dynamic heap growth after initialization<br>• Single-dereference attribute access |

### NASA Code Guidelines
- Clear documentation for all modules, classes, and functions
- Thorough error handling with appropriate error logging
- Proper resource management (connections, file handles, memory)
- Defensive programming with input validation and security checks
- Consistent naming conventions and code style
- Modular design with separation of concerns

### UNIX Philosophy
- Do one thing and do it well (focused components)
- Programs should work together (composable architecture)
- Simple interfaces over complex ones
- Design for clarity and maintainability
- Each component testable in isolation

### The Power of 10 Rules
1. Avoid complex flow constructs, such as goto and recursion
2. All loops must have fixed bounds to prevent runaway code
3. Avoid heap memory allocation after initialization
4. Restrict functions to a single printed page (~50 lines)
5. Use a minimum of two runtime assertions per function
6. Restrict the scope of data to the smallest possible
7. Check the return value of all non-void functions
8. Use the preprocessor only for header files and simple macros
9. Limit pointer use to a single dereference
10. Compile with all possible warnings active

## Installation

```bash
# Clone the repository
git clone https://github.com/Elessar617/Crypto_Arb_Bot.git
cd Crypto_Arb_Bot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev,test]"
```

## Configuration

Store your exchange API credentials securely in the credential manager:

```bash
# Initialize credentials (first time only)
python -m crypto_arb_bot.cli.credential_manager initialize

# Add exchange credentials
python -m crypto_arb_bot.cli.credential_manager add --exchange coinbase
```

Edit configuration files in `config/` to customize bot behavior.

## Usage

```bash
# Run the arbitrage bot
python -m crypto_arb_bot

# Simulate trading without real orders
python -m crypto_arb_bot --paper-trading

# Monitor specific exchanges
python -m crypto_arb_bot --exchanges coinbase,kraken
```

## Development

This project uses the latest stable versions of Python tooling to ensure code quality:

```bash
# Format code (NASA consistent formatting)
black src tests

# Run type checking (Power of 10 rule #10)
mypy src tests

# Run linting (enforce NASA guidelines)
flake8 src tests

# Run security checks
bandit -r src

# Run tests with coverage (minimum 90% required)
pytest --cov=src tests/
```

## Testing & CI

### Testing Strategy

- **Unit Tests**: One test module per service, fixtures with fixed data, each test has ≥2 assert calls.
- **Integration Tests**: Spin up a dummy HTTP server (e.g. aiohttp test server), run one full `Engine.run_cycle()`.

### CI Pipeline

```bash
# Check code formatting
black --check .

# Run linting
flake8 --max-line-length=88 src/ tests/

# Type checking
mypy src/

# Security checks
bandit -r src/

# Run tests, fail fast
pytest --maxfail=1 --durations=10

# Measure coverage
coverage run -m pytest && coverage report --fail-under=90
```

### Implementation Requirements

Each module and function adheres to these principles:

1. **Fixed Bounds**: All loops have explicit bounds to prevent runaway execution
2. **Resource Management**: All resources (network, files, memory) are properly allocated and released
3. **Function Size**: No function exceeds 60 lines (~one printed page)
4. **Assertions**: Minimum of 2 runtime assertions per function
5. **Type Safety**: Complete static type annotations checked by mypy
6. **Error Handling**: Explicit error types and handling strategies
7. **Testability**: Every function is designed for isolated unit testing
8. **Documentation**: Clear docstrings explaining purpose, parameters and returns
9. **Pure Functions**: Wherever possible, functions have no side effects
10. **Pre-allocation**: Memory allocated at initialization, not during hot paths

## Project Structure

```
crypto_arb_bot/
├── pyproject.toml            # poetry/PEP517 metadata, mypy/flake8/black/etc. config
├── README.md                 # overview, quick-start, requirement mappings
├── config/                   
│   └── config.py             # dataclass + loader + 2 assertions per fn
│
├── src/crypto_arb_bot/       # actual package
│   ├── __init__.py
│   ├── cli.py                # single CLI entrypoint (argparse + subcommands)
│   ├── credentials.py        # keyring/env var wrapper (no plaintext JSON)
│   ├── fetcher.py            # AsyncFetcher class: fixed‐bound, pre-allocated buffers
│   ├── scanner.py            # compute_spread(), scan_cycle()—small fns ≤60 lines
│   ├── executor.py           # execute_trade() with bounded retry loops
│   ├── health_check.py       # discrete checks, no internal loops
│   ├── engine.py             # orchestrates fetch → scan → execute once or N times
│   ├── errors.py             # central exception types
│   └── utils.py              # tiny, single-purpose helpers
│
├── tests/                    
│   ├── unit/                 # one file per module; each test fn has ≥2 assertions
│   └── integration/          # end-to-end dry-run with mocks
│
└── ci/                       
    └── github.yml            # CI: black, flake8, mypy, bandit, pytest, coverage
```

## License

Proprietary. All rights reserved.

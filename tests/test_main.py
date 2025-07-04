"""Unit tests for main.py module."""

import unittest
import tempfile
import shutil
from unittest.mock import patch, call

# Import the module to be tested
import main


class TestMainModule(unittest.TestCase):
    """Tests for the main.py run_bot function."""

    @patch("main.PersistenceManager")
    @patch("main.coinbase_client.CoinbaseClient")
    @patch("main.TradeManager")
    @patch("main.config")
    @patch("main.get_logger")
    @patch("main.sys.exit")
    def test_run_bot_success(
        self,
        mock_exit,
        mock_get_logger,
        mock_config,
        mock_trade_manager,
        mock_persistence_manager,  # This is the CoinbaseClient mock
        mock_coinbase_client,  # This is the PersistenceManager mock
    ):
        """Test successful execution of run_bot with multiple assets."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            mock_config.TRADING_PAIRS = ["BTC-USD", "ETH-USD"]
            mock_config.LOG_LEVEL = "INFO"
            mock_config.LOG_FILE = "test.log"
            mock_config.PERSISTENCE_DIR = tmp_dir
        mock_logger = mock_get_logger.return_value
        mock_client_instance = mock_persistence_manager.return_value
        mock_tm_instance = mock_trade_manager.return_value
        mock_pm_instance = mock_coinbase_client.return_value

        main.run_bot()

        mock_persistence_manager.assert_called_once_with()
        mock_coinbase_client.assert_called_once_with(logger=mock_logger)

        mock_trade_manager.assert_called_once_with(
            client=mock_client_instance,
            persistence_manager=mock_pm_instance,
            ta_module=main.technical_analysis,
            config_module=mock_config,
            logger=mock_logger,
            signal_analyzer=main.signal_analyzer,
            order_calculator=main.order_calculator,
        )

        self.assertEqual(mock_tm_instance.process_asset_trade_cycle.call_count, 2)
        mock_tm_instance.process_asset_trade_cycle.assert_has_calls(
            [
                call(asset_id="BTC-USD"),
                call(asset_id="ETH-USD"),
            ]
        )
        mock_exit.assert_not_called()

    @patch("main.coinbase_client.CoinbaseClient")
    @patch("main.config")
    @patch("main.get_logger")
    @patch("main.sys.exit")
    def test_run_bot_client_initialization_failure(
        self, mock_exit, mock_get_logger, mock_config, mock_coinbase_client
    ):
        """Test run_bot exits when CoinbaseClient initialization fails."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            mock_config.TRADING_PAIRS = ["BTC-USD"]
            mock_config.LOG_LEVEL = "INFO"
            mock_config.LOG_FILE = "test.log"
            mock_config.PERSISTENCE_DIR = tmp_dir
        mock_logger = mock_get_logger.return_value
        error_message = "Invalid API keys"
        mock_coinbase_client.side_effect = RuntimeError(error_message)

        main.run_bot()

        mock_logger.critical.assert_called_once_with(
            f"A critical error halted the bot: {error_message}",
            exc_info=True,
        )
        mock_exit.assert_called_once_with(1)

    @patch("main.coinbase_client.CoinbaseClient")
    @patch("main.TradeManager")
    @patch("main.config")
    @patch("main.get_logger")
    @patch("main.sys.exit")
    def test_run_bot_asset_processing_error_continues(
        self,
        mock_exit,
        mock_get_logger,
        mock_config,
        mock_trade_manager,
        mock_coinbase_client,
    ):
        """Test that an error in one asset doesn't stop the next one."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            mock_config.TRADING_PAIRS = ["BTC-USD", "ETH-USD"]
            mock_config.LOG_LEVEL = "INFO"
            mock_config.LOG_FILE = "test.log"
            mock_config.PERSISTENCE_DIR = tmp_dir
        mock_logger = mock_get_logger.return_value
        mock_tm_instance = mock_trade_manager.return_value
        error_message = "Test processing error"
        mock_tm_instance.process_asset_trade_cycle.side_effect = [
            Exception(error_message),
            None,  # Success for the second asset
        ]

        main.run_bot()

        self.assertEqual(mock_trade_manager.call_count, 1)
        self.assertEqual(mock_tm_instance.process_asset_trade_cycle.call_count, 2)

        mock_logger.error.assert_called_once_with(
            f"An unexpected error occurred while processing BTC-USD: {error_message}",
            exc_info=True,
        )
        mock_exit.assert_not_called()


if __name__ == "__main__":
    unittest.main()

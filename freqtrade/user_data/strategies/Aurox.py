# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
import pandas as pd
# --------------------------------

import logging
import requests
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

import pymongo

mongo_db = pymongo.MongoClient('mongo', username='changeme', password='changeme1?',
                               port=27017)

logger = logging.getLogger(__name__)

class Aurox(IStrategy):
    """
        buy:
            Aurox Signals Long on Specified Time-Frame
        sell:
            Aurox Signals Short on Specified Time-Frame
    """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    # 1.0 = 100% ROI
    minimal_roi = {
        "0": 10.0
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    # -0.1 = -10% stoploss
    stoploss = -0.1

    # timeframe for the strategy
    timeframe = '15m'

    # timeframe for the Aurox indicator
    aurox_timeframe = '1d'

    # Logic needed to select the correct timeframe from the MongoDB
    if aurox_timeframe == '30m':
        timeUnit = '30_minute'
    elif aurox_timeframe == '1h':
        timeUnit = '1_hour'
    elif aurox_timeframe == '4h':
        timeUnit = '4_hour'
    elif aurox_timeframe == '12h':
        timeUnit = '12_hour'
    elif aurox_timeframe == '1d':
        timeUnit = '1_day'
    elif aurox_timeframe == '1w':
        timeUnit = '1_week'
    else:
        timeUnit = '1_month'

    # Define dictionary that stores the Aurox signal
    custom_info = {}

    def bot_loop_start(self, **kwargs) -> None:
        """
        Called at the start of the bot iteration (one loop).
        Might be used to perform pair-independent tasks
        (e.g. gather some remote resource for comparison)
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """

        if self.config['runmode'].value in ('live', 'dry_run'):
            self.mydb = mongo_db["indicators"]
            self.mycol = self.mydb["aurox"]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Called every loop of the bot after bot_loop_start.
        Calculates the TA indicators given the OHLCV data fr
        """

        # Check if the entry already exists
        if not metadata["pair"] in self.custom_info:
            # Create empty entry for this pair
            self.custom_info[metadata["pair"]] = {}

        if self.dp:
            if self.dp.runmode.value in ('live', 'dry_run'):

                # Get Aurox data for specified timeframe
                row_data = self.mycol.find_one({"pairDisplay": metadata['pair'], "timeUnit": self.timeUnit}, sort=[( '_id', pymongo.DESCENDING)])
                self.custom_info[metadata['pair']][self.aurox_timeframe] = row_data['signal']
                logger.info(metadata['pair'])
                logger.info(self.custom_info[metadata['pair']][self.aurox_timeframe])

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on the Aurox indicator, populates the buy signal for the dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (self.custom_info[metadata['pair']][self.aurox_timeframe] == 'long') &
                (dataframe['volume'] > 0) # Extra check as you don't want to trade if there is 0 volume
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on the Aurox indicator, populates the sell signal for the dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (self.custom_info[metadata['pair']][self.aurox_timeframe] == 'short') & 
                (dataframe['volume'] > 0) # Extra check as you don't want to trade if there is 0 volume
            ),
            'sell'] = 1

        return dataframe


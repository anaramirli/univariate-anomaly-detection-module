"""Univariate anomaly detection module."""

__version__ = '0.0.2'

from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel
from adtk.detector import PersistAD, ThresholdAD, LevelShiftAD, VolatilityShiftAD
import numpy
import pandas
from . core.tools import aggregate_anomalies

app = FastAPI(
    title='Univariate anomaly detection module.',
    docs_url='/documentation',
    redoc_url='/redoc',
    description='Univariate anomaly detection based on historic data for time series.',
    version=__version__
)


class Parameters(BaseModel):
    """Parameters for ADTK PersistAD"""
    c: float = 3.0
    window: str = '28D'
    aggregate_anomalies: str = None


class TimeSeriesData(BaseModel):
    """Data provided for point anomaly detection."""
    train_data: Dict[str, float]
    score_data: Dict[str, float]
    parameters: Parameters


class Anomalies(BaseModel):
    """Anomalies"""
    anomaly_list: Dict[str, bool]


class ParametersThresholdAD(BaseModel):
    """Parameters for ADTK ThresholdAD"""
    high: float = None
    low: float = None
    aggregate_anomalies: str = None


class TimeSeriesDataThresholdAD(BaseModel):
    """Data provided for point anomaly detection."""
    score_data: Dict[str, float]
    parameters: ParametersThresholdAD


class ParametersLevelShiftAD(BaseModel):
    """Parameters for ADTK LevelShiftAD"""
    c: float = 20.0
    window: str = '60S'
    aggregate_anomalies: str = None


class TimeSeriesDataLevelShiftAD(BaseModel):
    """Data provided for point anomaly detection."""
    score_data: Dict[str, float]
    parameters: ParametersLevelShiftAD


class ParametersVolatilityShiftAD(BaseModel):
    """Parameters for ADTK LevelShiftAD"""
    c: float = 20.0
    window: str = '60S'
    aggregate_anomalies: str = None


class TimeSeriesDataVolatilityShiftAD(BaseModel):
    """Data provided for point anomaly detection."""
    score_data: Dict[str, float]
    parameters: ParametersVolatilityShiftAD


@app.post('/detect-point-anomalies', response_model=Anomalies)
async def detect_point_anomalies(time_series_data: TimeSeriesData):
    """Apply point anomaly detection and return list of anomalies."""

    # create pandas Series from dictionary containing the time series
    train_data = pandas.Series(time_series_data.train_data)
    train_data.index = pandas.to_datetime(train_data.index, unit='ms')

    score_data = pandas.Series(time_series_data.score_data)
    score_data.index = pandas.to_datetime(score_data.index, unit='ms')

    # apply persist anomaly detection to time series
    persist_ad = PersistAD(
        c=time_series_data.parameters.c,
        side='both',
        window=time_series_data.parameters.window
    )

    persist_ad.fit(train_data)
    anomalies = persist_ad.detect(score_data)

    # aggregate anomalies
    if time_series_data.parameters.aggregate_anomalies:
        # if aggregate_anomalies is passed with request

        anomalies = aggregate_anomalies(
            anomalies=anomalies,
            aggregation_interval=time_series_data.parameters.aggregate_anomalies
        )

    # convert anomalies Series to dictionary with timestamps
    anomalies.index = (
        anomalies.index.astype(numpy.int64) // 10 ** 6
    ).astype(str)
    anomalies = anomalies == 1
    anomalies_dict = anomalies.to_dict()

    return Anomalies(anomaly_list=anomalies_dict)


@app.post('/detect-threshold-anomalies', response_model=Anomalies)
async def detect_threshold_anomalies(time_series_data: TimeSeriesDataThresholdAD):
    """Apply simple threshold anomaly detection and return list of anomalies."""

    # create pandas Series from dictionary containing the time series
    score_data = pandas.Series(time_series_data.score_data)
    score_data.index = pandas.to_datetime(score_data.index, unit='ms')

    # apply threshold anomaly detection to time series
    threshold_ad = ThresholdAD(
        high=time_series_data.parameters.high, low=time_series_data.parameters.low)
    anomalies = threshold_ad.detect(score_data)

    # aggregate anomalies
    if time_series_data.parameters.aggregate_anomalies:
        # if aggregate_anomalies is passed with request

        anomalies = aggregate_anomalies(
            anomalies=anomalies,
            aggregation_interval=time_series_data.parameters.aggregate_anomalies
        )

    # convert anomalies Series to dictionary with timestamps
    anomalies.index = (
        anomalies.index.astype(numpy.int64) // 10 ** 6
    ).astype(str)
    anomalies = anomalies == 1
    anomalies_dict = anomalies.to_dict()

    return Anomalies(anomaly_list=anomalies_dict)


@app.post('/detect-levelshift-anomalies', response_model=Anomalies)
async def detect_levelshift_anomalies(time_series_data: TimeSeriesDataLevelShiftAD):
    """Apply levelshift anomaly detection and return list of anomalies."""


    # create pandas Series from dictionary containing the time series
    score_data = pandas.Series(time_series_data.score_data)
    score_data.index = pandas.to_datetime(score_data.index, unit='ms')

    # apply levelshift anomaly detection to time series
    level_shift_ad = LevelShiftAD(
        c=time_series_data.parameters.c,
        side='both',
        window=time_series_data.parameters.window
    )
    anomalies = level_shift_ad.fit_detect(score_data)

    # aggregate anomalies
    if time_series_data.parameters.aggregate_anomalies:
        # if aggregate_anomalies is passed with request

        anomalies = aggregate_anomalies(
            anomalies=anomalies,
            aggregation_interval=time_series_data.parameters.aggregate_anomalies
        )

    # convert anomalies Series to dictionary with timestamps
    anomalies.index = (
        anomalies.index.astype(numpy.int64) // 10 ** 6
    ).astype(str)
    anomalies = anomalies == 1
    anomalies_dict = anomalies.to_dict()

    return Anomalies(anomaly_list=anomalies_dict)


@app.post('/detect-volatilityshift-anomalies', response_model=Anomalies)
async def detect_volatilityshift_anomalies(time_series_data: TimeSeriesDataVolatilityShiftAD):
    """Apply volatility shift anomaly detection and return list of anomalies."""


    # create pandas Series from dictionary containing the time series
    score_data = pandas.Series(time_series_data.score_data)
    score_data.index = pandas.to_datetime(score_data.index, unit='ms')

    # apply Volatility Shift anomaly detection to time series
    volatility_shift_ad = VolatilityShiftAD(
        c=time_series_data.parameters.c,
        side='positive',
        window=time_series_data.parameters.window
    )
    anomalies = volatility_shift_ad.fit_detect(score_data)

    # aggregate anomalies
    if time_series_data.parameters.aggregate_anomalies:
        # if aggregate_anomalies is passed with request

        anomalies = aggregate_anomalies(
            anomalies=anomalies,
            aggregation_interval=time_series_data.parameters.aggregate_anomalies
        )

    # convert anomalies Series to dictionary with timestamps
    anomalies.index = (
        anomalies.index.astype(numpy.int64) // 10 ** 6
    ).astype(str)
    anomalies = anomalies == 1
    anomalies_dict = anomalies.to_dict()

    return Anomalies(anomaly_list=anomalies_dict)

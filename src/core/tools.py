"""Utilities for point anomaly detection."""

import pandas


def aggregate_anomalies(anomalies: pandas.Series, aggregation_interval: str):
    """Anomalies which are close to eachother are
    aggregated to one anomaly with the timestamp of
    the first anomaly of a close group. The other anomalies
    of a same group are ignored.
    The aggregation interval defines the maximum temporal distance 
    between two anomalies for being grouped. Starting with the first 
    anomaly, grouping is applied until the last anomaly does not have
    a new event closer than configured by the aggregation interval."""

    last_anomaly_timestamp = None
    for timestamp in anomalies.index:
        # iterate over DateTimeIndex

        if anomalies[timestamp] == 1:
            # if anomaly

            if last_anomaly_timestamp:
                # if a recent anomaly exists

                timedelta = (timestamp-last_anomaly_timestamp)
                if timedelta <= pandas.Timedelta(aggregation_interval):
                    # ignore anomaly if last anomaly newer than specified aggregation intervall

                    anomalies[timestamp] = 0

            last_anomaly_timestamp = timestamp
    return anomalies

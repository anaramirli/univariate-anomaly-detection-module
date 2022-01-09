"""Test the core utilities."""

from .. core import tools

import pandas
import unittest
import os

# paths to test data
pwd = os.path.dirname(__file__)
anomalies_csv_path = os.path.join(
    pwd,
    'anomalies.csv'
)
aggregated_anomalies_csv_path = os.path.join(
    pwd,
    'aggregated-anomalies-2000S.csv'
)


class TestTools(unittest.TestCase):
    """Test methods from module core.tools"""

    def test_aggregate_anomalies(self):
        """x"""
        anomalies = pandas.read_csv(
            anomalies_csv_path,
            squeeze=True,
            index_col='Date (UTC)',
            parse_dates=True
        )

        aggregated_anomalies = pandas.read_csv(
            aggregated_anomalies_csv_path,
            squeeze=True,
            index_col='Date (UTC)',
            parse_dates=True
        )

        pandas._testing.assert_series_equal(
            aggregated_anomalies,
            tools.aggregate_anomalies(
                anomalies=anomalies, aggregation_interval='2000S')
        )


if __name__ == '__main__':
    unittest.main()

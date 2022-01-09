"""Test the webserver built with FastAPI"""

from fastapi.testclient import TestClient
from .. import main

import os

# paths to test data
pwd = os.path.dirname(__file__)
levelshift_input_csv_path = os.path.join(
    pwd,
    'level_shift_test.csv'
)
levelshift_anomalies_csv_path = os.path.join(
    pwd,
    'level_shift_result.csv'
)


client = TestClient(main.app)


def test_detect_point_anomalies():
    """Tests detection of point anomalies."""
    response = client.post(
        '/detect-point-anomalies',
        json={
            'train_data': {
                '1379980800000': 55620.0,
                '1379981100000': 55800.0,
                '1379981400000': 56160.0,
                '1379981700000': 55620.0,
                '1379982000000': 55530.0,
                '1379982300000': 55530.0
            },
            'score_data': {
                '1382400000000': 90540.0,
                '1382400300000': 90720.0,
                '1382400600000': 89910.0,
                '1382400900000': 87390.0,
                '1382401200000': 85410.0,
                '1382401500000': 79650.0
            },
            'parameters': {
                'c': 3,
                'window': '15T'
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'anomaly_list': {
            '1382400000000': False,
            '1382400300000': False,
            '1382400600000': True,
            '1382400900000': True,
            '1382401200000': True,
            '1382401500000': True
        }
    }


def test_detect_point_anomalies_aggregated():
    """Tests detection of point anomalies with
    aggregated anomalies."""
    response = client.post(
        '/detect-point-anomalies',
        json={
            'train_data': {
                '1379980800000': 55620.0,
                '1379981100000': 55800.0,
                '1379981400000': 56160.0,
                '1379981700000': 55620.0,
                '1379982000000': 55530.0,
                '1379982300000': 55530.0
            },
            'score_data': {
                '1382400000000': 90540.0,
                '1382400300000': 90720.0,
                '1382400600000': 89910.0,
                '1382400900000': 87390.0,
                '1382401200000': 85410.0,
                '1382401500000': 79650.0
            },
            'parameters': {
                'c': 3,
                'window': '15T',
                'aggregate_anomalies': '500S'
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'anomaly_list': {
            '1382400000000': False,
            '1382400300000': False,
            '1382400600000': True,
            '1382400900000': False,
            '1382401200000': False,
            '1382401500000': False
        }
    }


def test_detect_threshold_anomalies():
    """Tests detection of threshold anomalies."""
    response = client.post(
        '/detect-threshold-anomalies',
        json={
            'score_data': {
                '1382400000000': 90540.0,
                '1382400300000': 90720.0,
                '1382400600000': 89910.0,
                '1382400900000': 87390.0,
                '1382401200000': 85410.0,
                '1382401500000': 79650.0
            },
            'parameters': {
                'c': 3,
                'window': '15T',
                'aggregate_anomalies': '500S'
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'anomaly_list': {
            '1382400000000': False,
            '1382400300000': False,
            '1382400600000': False,
            '1382400900000': False,
            '1382401200000': False,
            '1382401500000': False
        }
    }


def test_detect_levelshift_anomalies():
    """Tests detection of level shift anomalies."""
    response = client.post(
        '/detect-levelshift-anomalies',
        json={
            'score_data': {
                '9799000': 2.119156122094594,
                '9800000': 2.170792081232256,
                '9801000': 2.072264556251881,
                '9802000': 2.048970442156524,
                '9803000': 2.0344976627265456,
                '9804000': 2.030428751714349,
                '9805000': 1.995015841410387,
                '9806000': 1.975725357663717,
                '9807000': 1.96430842737761,
                '9808000': 1.944965381356912,
                '9809000': 1.9299464555495665
            },
            'parameters': {
                'c': 1.0,
                'window': '3S',
                # 'aggregate_anomalies': '500S'
            }
        }
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        'anomaly_list': {
            '9799000': False,
            '9800000': False,
            '9801000': True,
            '9802000': False,
            '9803000': False,
            '9804000': False,
            '9805000': False,
            '9806000': False,
            '9807000': False,
            '9808000': False,
            '9809000': False
        }
    }


def test_detect_volatilityshift_anomalies():
    """Tests detection of volatility shift anomalies."""
    response = client.post(
        '/detect-volatilityshift-anomalies',
        json={
            'score_data': {
                '9799000': 2.119156122094594,
                '9800000': 2.170792081232256,
                '9801000': 2.072264556251881,
                '9802000': 2.048970442156524,
                '9803000': 2.0344976627265456,
                '9804000': 2.030428751714349,
                '9805000': 10.995015841410387,
                '9806000': 1.975725357663717,
                '9807000': 1.96430842737761,
                '9808000': 1.944965381356912,
                '9809000': 1.929946455549566
            },
            'parameters': {
                'c': 1.0,
                'window': '3S',
                # 'aggregate_anomalies': '500S'
            }
        }
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {
        'anomaly_list': {
            '9799000': False,
            '9800000': False,
            '9801000': False,
            '9802000': False,
            '9803000': False,
            '9804000': True,
            '9805000': True,
            '9806000': False,
            '9807000': False,
            '9808000': False,
            '9809000': False
        }
    }

    # def test_detect_levelshift_anomalies2():
    #     """Tests detection of level shift anomalies with csv file."""
    #     levelshift_input = pandas.read_csv(
    #         levelshift_input_csv_path,
    #         squeeze=True,
    #         index_col='Timestamp',
    #         parse_dates=False
    #     )
    #     levelshift_output = pandas.read_csv(
    #         levelshift_anomalies_csv_path,
    #         squeeze=True,
    #         index_col='Timestamp',
    #         parse_dates=False
    #     )
    #     levelshift_input.index = (
    #         levelshift_input.index.astype(numpy.int64) // 10 ** 6
    #     ).astype(str)

    #     response = client.post(
    #         '/levelshift-anomaly-detection',
    #         json={
    #             'score_data': levelshift_input.to_frame().dict(),
    #             'parameters': {
    #                 'c': 20.0,
    #                 'window': '60S',
    #             }
    #         }
    #     )

    #     elevations = response.text
    #     data = json.loads(elevations)
    #     df = pandas.json_normalize(data['anomaly_list'])

    #     assert response.status_code == 200
    #     pandas._testing.assert_frame_equal(
    #         levelshift_output.to_frame(),
    #         df
    #     )

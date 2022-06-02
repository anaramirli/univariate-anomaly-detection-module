"""Test the webserver built with FastAPI"""

from fastapi.testclient import TestClient
from .. import main

client = TestClient(main.app)

# constants
false = False
true = True


def test_detect_point_anomalies():
    """Tests detection of point anomalies."""
    response = client.post(
        '/detect-point-anomalies',
        json={
            "train_data": {
                "1379980800000": 55620.0,
                "1379981100000": 55800.0,
                "1379981400000": 56160.0,
                "1379981700000": 55620.0,
                "1379982000000": 55530.0,
                "1379982300000": 55530.0
            },
            "score_data": {
                "1382400000000": 90540.0,
                "1382400300000": 90720.0,
                "1382400600000": 89910.0,
                "1382400900000": 87390.0,
                "1382401200000": 85410.0,
                "1382401500000": 79650.0
            },
            "parameters": {
                "c": 3,
                "window": "15T"
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "anomaly_list": {
            "1382400000000": false,
            "1382400300000": false,
            "1382400600000": true,
            "1382400900000": true,
            "1382401200000": true,
            "1382401500000": true
        }
    }


def test_detect_point_anomalies_aggregated():
    """Tests detection of point anomalies with
    aggregated anomalies."""
    response = client.post(
        '/detect-point-anomalies',
        json={
            "train_data": {
                "1379980800000": 55620.0,
                "1379981100000": 55800.0,
                "1379981400000": 56160.0,
                "1379981700000": 55620.0,
                "1379982000000": 55530.0,
                "1379982300000": 55530.0
            },
            "score_data": {
                "1382400000000": 90540.0,
                "1382400300000": 90720.0,
                "1382400600000": 89910.0,
                "1382400900000": 87390.0,
                "1382401200000": 85410.0,
                "1382401500000": 79650.0
            },
            "parameters": {
                "c": 3,
                "window": "15T",
                "aggregate_anomalies": "500S"
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "anomaly_list": {
            "1382400000000": false,
            "1382400300000": false,
            "1382400600000": true,
            "1382400900000": false,
            "1382401200000": false,
            "1382401500000": false
        }
    }




def test_detect_threshold_anomalies():
    """Tests detection of threshold anomalies."""
    response = client.post(
        '/detect-threshold-anomalies',
        json={
            "score_data": {
                "1609455600": 0.12178372709024772, 
				"1609455660": 0.11050720099031877, 
				"1609455720": 0.10551539379110654, 
				"1609455780": 0.12782051546031659, 
				"1609455840": 0.10162464965348023, 
				"1609455900": 0.10842426724768395, 
				"1609455960": 0.11646994268581218, 
				"1609456020": 0.1069694857691467, 
				"1609456080": 0.10106735409516875, 
				"1609456140": 0.10532371366814815}, 	
			"parameters": {
                "high": 0.11050720099031877}
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "anomaly_list": {
            "1609455600": true,
            "1609455660": false,
            "1609455720": false,
            "1609455780": true,
            "1609455840": false,
            "1609455900": false,
            "1609455960": true,
            "1609456020": false,
            "1609456080": false,
            "1609456140": false
        }
    }


def test_detect_levelshift_anomalies():
    """Tests detection of level shift anomalies."""
    response = client.post(
        '/detect-levelshift-anomalies',
        json={
            "score_data": {
                "9799000": 2.119156122094594,
                "9800000": 2.170792081232256,
                "9801000": 2.072264556251881,
                "9802000": 2.048970442156524,
                "9803000": 2.0344976627265456,
                "9804000": 2.030428751714349,
                "9805000": 1.995015841410387,
                "9806000": 1.975725357663717,
                "9807000": 1.96430842737761,
                "9808000": 1.944965381356912,
                "9809000": 1.9299464555495665
                },
                "parameters": {
                    "c": 1,
                    "window": "3S"
                }
        }
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
    "anomaly_list": {
        "9799000": false,
        "9800000": false,
        "9801000": true,
        "9802000": false,
        "9803000": false,
        "9804000": false,
        "9805000": false,
        "9806000": false,
        "9807000": false,
        "9808000": false,
        "9809000": false
    }
    }

def test_detect_volatilityshift_anomalies():
    """Tests detection of volatility shift anomalies."""
    response = client.post(
        '/detect-volatilityshift-anomalies',
        json={
            "score_data": {
                "9799000": 2.119156122094594,
                "9800000": 2.170792081232256,
                "9801000": 2.072264556251881,
                "9802000": 2.048970442156524,
                "9803000": 2.0344976627265456,
                "9804000": 2.030428751714349,
                "9805000": 10.995015841410387,
                "9806000": 1.975725357663717,
                "9807000": 1.96430842737761,
                "9808000": 1.944965381356912,
                "9809000": 1.929946455549566
                },
                "parameters": {
                    "c": 1,
                    "window": "3S"
                }
        }
    )
    assert response.status_code == 200

    
    assert response.json() == {
        "anomaly_list": {
            "9799000": false,
            "9800000": false,
            "9801000": false,
            "9802000": false,
            "9803000": false,
            "9804000": true,
            "9805000": true,
            "9806000": false,
            "9807000": false,
            "9808000": false,
            "9809000": false
        }
    }
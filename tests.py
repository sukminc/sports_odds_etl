# tests.py
from etl import transform_data


def test_transform_data_happy_path():
    """
    Tests the transform_data function with a sample of good API data.
    """
    # ARRANGE: Create a sample of the raw data the API would return.
    sample_api_data = [
        {
            "id": "1",
            "home_team": "Team A",
            "away_team": "Team B",
            "commence_time": "2025-09-05T00:20:00Z",
            "bookmakers": [
                {
                    "key": "draftkings",
                    "markets": [{
                        "outcomes": [
                            {"name": "Team A", "price": -150},
                            {"name": "Team B", "price": 130}
                        ]
                    }]
                }
            ]
        },
        {
            "id": "2",
            "home_team": "Team C",
            "away_team": "Team D",
            "commence_time": "2025-09-06T00:20:00Z",
            "bookmakers": [
                {
                    "key": "fanduel",  # Note: a different bookmaker
                    "markets": [{
                        "outcomes": [
                            {"name": "Team C", "price": -200},
                            {"name": "Team D", "price": 180}
                        ]
                    }]
                },
                {
                    "key": "draftkings",
                    "markets": [{
                        "outcomes": [
                            {"name": "Team C", "price": -210},
                            {"name": "Team D", "price": 190}
                        ]
                    }]
                }
            ]
        }
    ]

    # ACT: Run the function we are testing.
    result = transform_data(sample_api_data)

    # ASSERT: Check that the output is what we expect.
    assert len(result) == 2  # It should have processed both games

    # Check the data for the first game
    assert result[0]['id'] == "1"
    assert result[0]['home_team'] == "Team A"
    assert result[0]['away_team_odds'] == 130

    # Check the data for the second game
    assert result[1]['home_team_odds'] == -210  # Make sure it got the draftkings odds
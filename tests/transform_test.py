import pandas as pd
import os

def test_transformed_parquet_structure():
    file_path = "data/silver/breweries.parquet"
    assert os.path.exists(file_path)

    df = pd.read_parquet(file_path)

    expected_columns = {
        "id", "name", "brewery_type", "address_1", "address_2", "address_3",
        "city", "state_province", "postal_code", "country", "longitude",
        "latitude", "phone", "website_url", "state", "street"
    }

    assert expected_columns.issubset(df.columns)
    assert len(df) > 0  # Garantindo que há dados
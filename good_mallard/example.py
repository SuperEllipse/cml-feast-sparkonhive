# # # # # # # # # # # # # # # # # # # # # # # #
# This is an example feature definition file  #
# # # # # # # # # # # # # # # # # # # # # # # #

from datetime import timedelta
from pathlib import Path

from feast import Entity, FeatureService, FeatureView, Field, ValueType
from feast.infra.offline_stores.contrib.spark_offline_store.spark_source import (
    SparkSource,
)
from feast.types import Float32, Int64

# Constants related to the generated data sets
CURRENT_DIR = Path(__file__).parent


# Entity definitions
driver = Entity(name="driver", value_type=ValueType.INT64, description="driver id", join_keys=["driver_id"])


#sources

driver_hourly_stats = SparkSource(
     table="driver_stats",
     timestamp_field="event_timestamp",
     created_timestamp_column="created",
)


# Feature Views
driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=["driver"],
    ttl=timedelta(days=7),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    online=True,
    source=driver_hourly_stats,
    tags={},
)


driver_stats_fs = FeatureService(
    name="driver_activity",
    features=[driver_hourly_stats_view],
)

driver_stats_fs = FeatureService(
    name="driver_activity_v1", features=[driver_hourly_stats_view]
)
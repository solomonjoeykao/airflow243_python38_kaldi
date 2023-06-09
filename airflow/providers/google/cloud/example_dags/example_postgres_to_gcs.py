#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG using PostgresToGoogleCloudStorageOperator.
"""
import os
from datetime import datetime

from airflow import models
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "example-project")
GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET_NAME", "INVALID BUCKET NAME")
FILENAME = "test_file"
SQL_QUERY = "select * from test_table;"

with models.DAG(
    dag_id='example_postgres_to_gcs',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    upload_data = PostgresToGCSOperator(
        task_id="get_data", sql=SQL_QUERY, bucket=GCS_BUCKET, filename=FILENAME, gzip=False
    )

    upload_data_server_side_cursor = PostgresToGCSOperator(
        task_id="get_data_with_server_side_cursor",
        sql=SQL_QUERY,
        bucket=GCS_BUCKET,
        filename=FILENAME,
        gzip=False,
        use_server_side_cursor=True,
    )

import time

import jmespath
from google.cloud import bigquery

responses = {}


def import_to_bigquery(request, dataset_id='assessments', table_id='cloud_assessment'):
    global responses

    current_timestamp = time.time()

    bq_client = bigquery.Client()

    print(f"Request is: {request}")
    payload = request.get_json(silent=False)
    print(f"Payload is: {payload}")
    current_timestamp = time.time()

    responses = jmespath.search('responses', payload)
    print(f"Responses is: {responses}")

    project_code, project_manager, uses_git, has_cicd, has_api, is_split_into_microservices, uses_containers, \
    uses_cloud_provider, has_centralized_logs, has_monitoring = responses

    print(f"project code is: {project_code}")

    rows_to_insert = [
        (project_code, current_timestamp, project_manager, str_to_int(uses_git), str_to_int(has_cicd), str_to_int(has_api),
         str_to_int(is_split_into_microservices), str_to_int(uses_containers), str_to_int(uses_cloud_provider),
         str_to_int(has_centralized_logs), str_to_int(has_monitoring))
    ]

    table_ref = bq_client.dataset(dataset_id).table(table_id)
    table = bq_client.get_table(table_ref)
    errors = bq_client.insert_rows(table, rows_to_insert)
    print(f"after insert message: {errors}")

def str_to_int(s):
    return 1 if s.lower() == "oui" else 0

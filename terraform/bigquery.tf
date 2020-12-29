resource "google_bigquery_dataset" "assessments_dataset" {
  dataset_id                  = "assessments"
  description                 = "To store all results of assessment"
  location                    = var.gcp_region

  labels = {
    env = "dev"
  }

  access {
    role          = "WRITER"
    user_by_email = google_service_account.bqwriter.email
  }
}

resource "google_bigquery_table" "assessment_cloud" {
  dataset_id = google_bigquery_dataset.assessments_dataset.dataset_id
  table_id   = "cloud_assessment"

  time_partitioning {
    type = "DAY"
  }

  labels = {
    env = "dev"
  }

  schema = <<EOF
[
  {
    "name": "code_project",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "current_timestamp",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "uses_git",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "has_cicd",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "has_api",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "is_split_into_microservices",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "uses_containers",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "uses_cloud_provider",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "has_centralized_logs",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "has_monitoring",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF

}
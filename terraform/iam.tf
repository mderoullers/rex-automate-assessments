resource "google_service_account" "sa-bqeditor" {
  account_id = "bqeditor"
}

resource "google_project_iam_binding" "secret-accessor" {
  role = "roles/bigquery.dataEditor"
  members = [
    "serviceAccount:${google_service_account.sa-bqeditor.email}",
  ]
}

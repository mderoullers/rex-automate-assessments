data "archive_file" "source_code" {
  type        = "zip"
  source_dir  = "${path.root}/source"
  output_path = "${path.root}/source.zip"
}

resource "google_storage_bucket" "bucket_assessment" {
  name = "assessment-cloud-sud"
}

resource "google_storage_bucket_object" "bucket_assessment_object" {
  name   = "source.zip"
  bucket = google_storage_bucket.bucket_assessment.name
  source = "${path.root}/source.zip"
}

resource "google_cloudfunctions_function" "cloud_assessment_analyze" {
  name = "cloud-assessment-analyze"
  description = "The function analyzes the assessments from google forms and publishes the results in Bigquery"
  runtime = "python37"
  available_memory_mb = 128
  source_archive_bucket = google_storage_bucket.bucket_assessment.name
  source_archive_object = google_storage_bucket_object.bucket_assessment_object.name
  trigger_http = true
  timeout = 60
  entry_point = "import_to_bigquery"
  service_account_email = google_service_account.sa-bqeditor.email
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.cloud_assessment_analyze.project
  region         = google_cloudfunctions_function.cloud_assessment_analyze.region
  cloud_function = google_cloudfunctions_function.cloud_assessment_analyze.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
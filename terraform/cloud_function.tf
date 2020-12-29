data "archive_file" "source_code" {
  type        = "zip"
  source_dir  = "${path.root}/source"
  output_path = "${path.root}/source.zip"
}

resource "google_storage_bucket" "my_bucket" {
  name = "my-bucket-assessment"
}

resource "google_storage_bucket_object" "my_bucket_object" {
  name   = "source.zip"
  bucket = google_storage_bucket.my_bucket.name
  source = "${path.root}/source.zip"
}

resource "google_cloudfunctions_function" "function_assessment_analyze" {
  name = "function-assessment-analyze"
  description = "The function analyzes the assessment with google forms and publishes the result in Bigquery"
  runtime = "python37"

  available_memory_mb = 128
  source_archive_bucket = google_storage_bucket.my_bucket.name
  source_archive_object = google_storage_bucket_object.my_bucket_object.name
  trigger_http = true
  timeout = 60
  entry_point = "import_to_bigquery"
  labels = {
    component = "assessments-cloud"
  }
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function_assessment_analyze.project
  region         = google_cloudfunctions_function.function_assessment_analyze.region
  cloud_function = google_cloudfunctions_function.function_assessment_analyze.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"

  service_account_email = google_service_account.bqwriter.email
}

# IAM entry for a single user to invoke the function
// resource "google_cloudfunctions_function_iam_member" "invoker" {
//   project        = google_cloudfunctions_function.function_assessment_analyze.project
//   region         = google_cloudfunctions_function.function_assessment_analyze.region
//   cloud_function = google_cloudfunctions_function.function_assessment_analyze.name

//   role   = "roles/cloudfunctions.invoker"
//   member = "user:myFunctionInvoker@example.com"
// }
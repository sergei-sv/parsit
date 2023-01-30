terraform {
  backend "gcs" {
    bucket = "bucket-tfstate-51422599d4c6a0d2"
    prefix = "terraform/state"
  }
}
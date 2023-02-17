terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.50.0"
    }
    google-beta = {
      version = "4.50.0"
      source  = "hashicorp/google-beta"
    }
  }
}

provider "google" {
  project = var.project_id
  region = var.region 
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

#             Enable API's              #
resource "google_project_service" "iam" {
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "resourcemanager" {
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudrun" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "sql-component" {
  service            = "sql-component.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "sqladmin" {
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

#    Google Artifact Registry Repository    #
resource "google_artifact_registry_repository" "docker_repo" {
  provider = google-beta
  location      = var.region
  repository_id = var.repository
  description   = "Docker repository"
  format        = "DOCKER"
}

resource "google_service_account" "docker_pusher" {
  provider = google-beta
  account_id   = "docker-pusher"
  display_name = "Docker Container Pusher"
}

resource "google_artifact_registry_repository_iam_member" "docker_pusher_iam" {
  provider = google-beta
  location = google_artifact_registry_repository.docker_repo.location
  repository =  google_artifact_registry_repository.docker_repo.repository_id
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.docker_pusher.email}"
  depends_on = [
    google_artifact_registry_repository.docker_repo,
    google_service_account.docker_pusher
    ]
}

#        Cloud SQL         #
resource "random_password" "database_password" {
  length  = 32
  special = false
}

resource "google_sql_database_instance" "buycheaper-db" {
  name             = "buycheaper-db-postgres"
  database_version = "POSTGRES_13"
  region           = var.region
  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "buycheaper"
  instance = google_sql_database_instance.buycheaper-db.name
  depends_on = [google_sql_database_instance.buycheaper-db]
}

resource "google_sql_user" "user" {
  name     = "buycheaper"
  instance = google_sql_database_instance.buycheaper-db.name
  password = random_password.database_password.result
  depends_on = [google_sql_database_instance.buycheaper-db]
}

#          Cloud Run              #
resource "google_cloud_run_service" "buycheaper" {
  name     = var.service
  location = var.region
  template {
    spec {
        service_account_name = google_service_account.botservice.email
        containers {
            image = "europe-north1-docker.pkg.dev/${var.project_id}/${var.repository}/${var.docker_image}"
            ports {
              container_port = 6800
            } 
            env {
              name  = "DB_USERNAME"
              value = google_sql_user.user.name
            }
            env {
              name  = "DB_PASSWORD"
              value = google_sql_user.user.password

            }
            env {
              name  = "DB_NAME"
              value = google_sql_database.database.name
            }
            env {
              name  = "DB_HOST"
              value = "/cloudsql/${google_sql_database_instance.buycheaper-db.connection_name}"
            }
        }
    }
    metadata {
        annotations = {
            "autoscaling.knative.dev/maxScale"      = "1"
            "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.buycheaper-db.connection_name
        }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }
  depends_on = [google_artifact_registry_repository_iam_member.docker_pusher_iam]
}

#Create a custom Service Account
resource "google_service_account" "botservice" {
  account_id = "botservice"
}

# Give the service account access to Cloud SQL
resource "google_project_iam_member" "botservice-iam" {
  project     = var.project_id
  role   = "roles/cloudsql.client"
  member = "serviceAccount:${google_service_account.botservice.email}"
}

# Create a policy that allows all users to invoke the API
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Apply the no-authentication policy to our Cloud Run Service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = var.region
  project     = var.project_id
  service     = google_cloud_run_service.buycheaper.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

output "cloud_run_instance_url" {
  value = google_cloud_run_service.buycheaper.status[0].url
}
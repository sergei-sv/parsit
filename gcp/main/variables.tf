variable "project_id" {
  description = "The name of the project"
  type        = string
  default     = "crucial-runner-370615"
}
variable "region" {
  description = "The default compute region"
  type        = string
  default     = "europe-north1"
}
variable "service" {
  type        = string
  default     = "buycheaper_bot"
  description = "The name of the service"
}
variable "repository" {
  description = "The name of the Artifact Registry repository to be created"
  type        = string
  default     = "docker-repo"
}
variable "docker_image" {
  description = "The name of the Docker image in the Artifact Registry repository to be deployed to Cloud Run"
  type        = string
  default     = "t_bot:0.0.1"
}
variable "first_time" {
  description = "Boolean flag to indicate if this is the first time the application is running. If so, the cloud run step is omitted"
  type        = bool
  default     = true
}

# ParsIt
-- it is a set of tools for collecting information from open sources, its processing, storage and provision to the end user. 
ParsIt has 3 main blocks: 
1) Parsers - tools for collecting and processing information;
2) CIS _(cleared information store)_ - tools for writing to the database;
3) Bots - tools for simple and convenient interaction with the end user).

# CI/CD description:

For this project we are using the Compute Engine in the Google Cloud Platform (GCP). We created a Docker Compose file that defines application and PostgreSQL database containers. In Docker Compose file we specifyed the PostgreSQL image, environment variables for the database connection details, and a volume for persistent data storage.
We have ci-cd.yaml file used for GitHub Actions. It contains a workflow definition named "Production Build, Push Docker images and Deployment". This workflow triggers automatically when code is pushed to the main branch or when a pull request is opened.
The workflow consists of a single job named "release-image", which runs on an Ubuntu environment. It contains several steps that perform the following actions:

Checkout the Git repository using the actions/checkout action.
Bump the version of the code and push a new Git tag using the mathieudutour/github-tag-action action.
Log in to Docker Hub using the docker/login-action action, which requires Docker Hub credentials stored in secrets.
Build a Docker image and push it to Docker Hub using the docker/build-push-action action. The image is tagged with the new Git tag.
Install SSH client and configure an SSH key using the webfactory/ssh-agent action.
Pull the latest Docker Compose file from a remote server using the scp command.
Update the Docker Compose file with the new Docker image tag using the sed command.
Deploy the updated application using Docker Compose on the remote server using the ssh command.
Overall, this workflow builds and pushes a Docker image to Docker Hub and deploys it to a remote server using Docker Compose.

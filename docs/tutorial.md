# AppSheet Clout Inspection Demo with Vertex AI

---

This tutorial helps you deploy the AppSheet Cloud Inspection Demo using Google Cloud Vertex AI, Firebase, Cloud Run & AppSheet.

Let's get started!

---

## Prerequisites

As a prerequisite, you must have a Google Cloud project with the rights to enable services and deploy public services. In case you don't know if you have the rights (Owner or Editor roles), you can try the deployment and based on any error messages we can check which additional rights you need (create a [Github Issue](https://github.com/tyayers/appsheet-cloud-inspection-demo/issues) in the project repo).

---

## Setup environment

To begin, edit the provided sample `1_env.sh` file, and set the environment variables there for your deployment. Most important is the PROJECT (GCP Project Id) where you want to deploy the service, as well as the [Google Cloud region](https://cloud.google.com/compute/docs/regions-zones#available) to use for the deployment.

Click <walkthrough-editor-open-file filePath="1_env.sh">here</walkthrough-editor-open-file> to open the file in the editor

Then, source the `1_env.sh` file in the shell.

```sh
source ./1_env.sh
```
When the command has been inserted into your shell, press Enter to run the command.

---

## Setup GCP Project and Deploy Service

Next we are going to configure the Google Cloud project by enabling the services needed, setting the rights of the service account used for the service, and do the deployment of the service to Cloud Run.

Click <walkthrough-editor-open-file filePath="2_deploy.sh">here</walkthrough-editor-open-file> to open the file in the editor, and see the commands that will be run.

Now let's run the script:

```sh
./2_deploy.sh
```
When the command has been inserted into your shell, press Enter to run the command.

<walkthrough-footnote>You will see a lot of command outputs. In case there is an error check if an organizational policy is blocking a service or command from being run. Create an issue in the GitHub repo for any unclear errors. You will also see some instructions to add the service account email to your Google Drive `appsheet` folder with Read access. This is so that our service can read the images taken by the app, and send them to Vertex AI for processing.</walkthrough-footnote>

---

## Insert test data

In order for our service to be recognized by AppSheet and have the API processed, we need to deploy some test data to our project.

Click <walkthrough-editor-open-file filePath="3_loaddata.sh">here</walkthrough-editor-open-file> to open the file in the editor, and see the commands that will insert a test record into our Firestore database.

Now let's run the script:

```sh
./3_loaddata.sh
```
When the command has been inserted into your shell, press Enter to run the command.

<walkthrough-footnote>This is just a test data record. We can delete it through the AppSheet app after configuring and connecting the data source.</walkthrough-footnote>

---

## Test service

Now that we've deployed the service, you can do a test call to see if our test data is returned.

Run this curl command to call our service and return the test inspection image data (including sample image data).

```sh
SERVICE_URL=$(gcloud run services describe $NAME --platform managed --region $REGION --format 'value(status.url)')
curl "$SERVICE_URL/images"
```
When the command has been inserted into your shell, press Enter to run the command.

---

## Conclusion
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

Congratulations! You've successfully deployed the service into your GCP project, now follow the walkthrough instructions to configure your AppSheet app to use the new service.
<walkthrough-inline-feedback></walkthrough-inline-feedback>
# AppSheet DocAI Adapter

---

This tutorial helps you deploy the AppSheet Cloud Inspection Demo using Google Cloud Vertex AI, Firebase, Cloud Run & AppSheet.

Let's get started!

---

## Setup environment

To begin, edit the provided sample `1_env.sh` file, and set the environment variables there for your deployment.

Click <walkthrough-editor-open-file filePath="1_env.sh">here</walkthrough-editor-open-file> to open the file in the editor

Then, source the `1_env.sh` file in the Cloud shell.

```sh
source ./1_env.sh
```
---

## Setup GCP Project and Deploy Service

Next we are going to configure the Google Cloud project by enabling the services needed, setting the rights of the service account used for the service, and do the deployment of the service to Cloud Run.

Click <walkthrough-editor-open-file filePath="2_deploy.sh">here</walkthrough-editor-open-file> to open the file in the editor, and see the commands that will be run.

Now let's run the script:

```sh
./2_deploy.sh
```

<walkthrough-footnote>You will see a lot of command outputs. In case there is an error check if an organizational policy is blocking a service or command from being run. Create an issue in the GitHub repo for any unclear errors. You will also see some instructions to add the service account email to your Google Drive `appsheet` folder with Read access. This is so that our service can read the images taken by the app, and send them to Vertex AI for processing.</walkthrough-footnote>

---

## Insert test data

In order for our service to be recognized by AppSheet and have the API processed, we need to deploy some test data to our project.

Click <walkthrough-editor-open-file filePath="3_loaddata.sh">here</walkthrough-editor-open-file> to open the file in the editor, and see the commands that will insert a test record into our Firestore database.

Now let's run the script:

```sh
./3_loaddata.sh
```

<walkthrough-footnote>This is just a test data record. We can delete it through the AppSheet app after configuring and connecting the data source.</walkthrough-footnote>

---

## Conclusion
<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

Congratulations! You've successfully deployed the service into your GCP project, now follow the walkthrough instructions to configure your AppSheet app to use the new service.
<walkthrough-inline-feedback></walkthrough-inline-feedback>
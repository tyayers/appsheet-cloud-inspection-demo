# AppSheet Cloud Inspection Demo

This demo shows how a no-code AppSheet app can use a serverless API deployed in Google Cloud to leverage Gen AI and storage features to enhance a visual inspection scenario.

## Architecture

Here is a high level architecture diagram of the solution.

![AppSheet solution architecture](architecture.png)

## Assets deployed

- Cloud Run containerized service written in Python to host the service and API
- A Firestore data collection used to persist the inspection data
- Vertex Gen AI Vision models to ask prompts about inspection photos

## Deploy

To deploy, simply click on this button to deploy into a chosen GCP project:

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

Or you can also deploy manually by cloning this repo and running the script [1_deploy.sh](1_deploy.sh):

```bash
./1_deploy.sh
```

After deploying, take the URL that's shown in the output window and add it as an API data source in AppSheet. Then you can build an app utilizing the API to analyze inspection photos (see the [Inspection API](apispec.yaml) spec for documentation of the individual properties).

### Test

You can also test with a demo Cloud Run deployment using this URL as the API endpoint in AppSheet (API Key can be anything): https://inspectionsvc-ghfontasua-ew.a.run.app

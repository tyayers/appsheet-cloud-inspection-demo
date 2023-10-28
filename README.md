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

Or you can also deploy manually by cloning this repo and running this script:

```bash
./1_deploy.sh
```

See complete guide to deploying and using the solution in this [community article](https://www.googlecloudcommunity.com/gc/Tips-Tricks/Use-Google-Cloud-Generative-AI-Image-Models-in-AppSheet-as-seen/td-p/629835) on the Google Cloud Community AppSheet site.

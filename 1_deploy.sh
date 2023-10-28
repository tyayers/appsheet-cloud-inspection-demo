export PROJECT=$(gcloud config get-value project)
export LOCATION=europe-west1
export NAME=inspectionsvc

gcloud services enable appengine.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable drive.googleapis.com

gcloud builds submit --tag "eu.gcr.io/$PROJECT/$NAME"

gcloud run deploy $NAME --image eu.gcr.io/$PROJECT/$NAME \
    --platform managed --project $PROJECT \
    --min-instances=1 \
    --region $LOCATION --allow-unauthenticated \
    --set-env-vars GCLOUD_PROJECT="$PROJECT"

export PROJECT=$(gcloud config get-value project)
export LOCATION=europe-west1
export NAME=inspectionsvc

gcloud builds submit --tag "eu.gcr.io/$PROJECT/$NAME"

gcloud run deploy $NAME --image eu.gcr.io/$PROJECT/$NAME \
    --platform managed --project $PROJECT \
    --min-instances=1 \
    --region $LOCATION --allow-unauthenticated \
    --set-env-vars GCLOUD_PROJECT="$PROJECT"

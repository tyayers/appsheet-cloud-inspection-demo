echo "Setting project to $PROJECT_ID"

gcloud config set project $PROJECT_ID

echo "Enabling services"
gcloud services enable appengine.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable documentai.googleapis.com
gcloud services enable drive.googleapis.com

# Create artifact registry, if needed
echo "Creating docker registry, Firestore DB, and updating user rights..."
gcloud artifacts repositories create docker-registry --repository-format=docker \
--location="$REGION" --description="Docker registry" 2>/dev/null

# Create firebase db and give service account rights, if needed
if [[ $(gcloud app describe 2>&1 || true) == *'ERROR'* ]]; then echo 'No app engine or firestore instances found, creating...' && gcloud app create --region=europe-west; fi
gcloud alpha firestore databases update --type=firestore-native
PROJECTNUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$PROJECT_IDNUMBER-compute@developer.gserviceaccount.com" --role='roles/datastore.user'
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$PROJECT_IDNUMBER-compute@developer.gserviceaccount.com" --role='roles/aiplatform.user'
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$PROJECT_IDNUMBER-compute@developer.gserviceaccount.com" --role='roles/documentai.apiUser'
echo "Add user $PROJECT_IDNUMBER-compute@developer.gserviceaccount.com to your AppSheet Google Drive folder with Read permissions."

# Submit build
echo "Building service"
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=_LOCATION="$REGION",_REPOSITORY="docker-registry",_IMAGE="$NAME" .

# Deploy
echo "Deploying service"
gcloud run deploy $NAME --image $REGION-docker.pkg.dev/$PROJECT_ID/docker-registry/$NAME \
    --platform managed --project $PROJECT_ID \
    --min-instances=1 \
    --region $REGION --allow-unauthenticated \
    --set-env-vars GCLOUD_PROJECT="$PROJECT_ID"

export SERVICE_URL=$(gcloud run services describe $NAME --platform managed --region $REGION --format 'value(status.url)')

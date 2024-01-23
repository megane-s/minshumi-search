gcloud scheduler jobs update http scheduled_recommend \
    --location asia-northeast1 \
    --schedule="0 18 * * *" \
    --uri="https://asia-northeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/megane-s-gcp/jobs/minshumi-notification:run" \
    --http-method POST \
    --oauth-service-account-email 174482454094-compute@developer.gserviceaccount.com

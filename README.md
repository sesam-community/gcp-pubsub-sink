Publish entities to GCP Pub/Sub

Set up google cloud
- Go to **[cloud.google.com](cloud.google.com)** and create your google account if you don’t already have one.
- Go to the console and create a **project**.
- Create a **service account** for your project (found under “IAM and admin” or by searching).
    - Create a key for your service account as you create the account. Choose JSON file format and name it "credentials.json"
- Go to **Pub/Sub** and create a topic.
- Create a **subscription** to your new topic.
- Create a **bucket** in (found under “Storage).
- Create a **dataset** and a **table** in BigQuery with a schema that fit your data.
- Create a **DataFlow from template** "Cloud Pub/Sub to BigQuery".
Once the DataFlow Job is running you can start the pushing data from the endpoint in Sesam

Setting up in Sesam.
If you need help go to our **microservice** section of the [Getting started with Sesam](https://github.com/sesam-community/wiki/wiki/Getting-started) page.

Sample system in Sesam:
```json
{
  "_id": "gcp-pubsub-sink",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "GOOGLE_APPLICATION_CREDENTIALS": "credentials.json",
      "GOOGLE_APPLICATION_CREDENTIALS_CONTENT": { Insert your Credentials from GCP
      },
      "PAYLOAD_KEY": "<optional attribute which part of entity send as payload (if you don't want to pass whole entity)>",
      "PROJECT_ID": "<project id>"
    },
    "image": "<dockerhub-username>/<repository>:<tag>",
    "port": 5000
  },
  "verify_ssl": true
}
```


Sample output pipe:
```json
{
  "_id": "target-endpoint",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "enriched-data"
  },
  "sink": {
    "type": "json",
    "system": "gcp-pubsub-sink",
    "url": "/<topic_id>"
  },
  "pump": {
    "cron_expression": "0 0 1 1 ?"
  }
}
```

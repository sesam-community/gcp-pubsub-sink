Publish entities to GCP Pub/Sub

Set up google cloud
- Go to **[cloud.google.com](cloud.google.com)** and create your google account if you don’t already have one.
- Go to the console and create a **project**.
- Create a **service account** for your project (found under “IAM and admin” or by searching).
    - Create a key for your service account as you create the account. Choose JSON file format and name it "credentials.json"
- Go to **Pub/Sub** and create a topic.
- Create a **subscription** to your new topic.
That's it to post data on pub\sub however you can do below extra steps if you want to send your data to BigQuery.
- Create a **bucket** in (found under “Storage).
- Create a **dataset** and a **table** in BigQuery with a schema that fit your data.
- Create a **DataFlow from template** "Cloud Pub/Sub to BigQuery".
Once the DataFlow Job is running you can start the pushing data from the endpoint in Sesam

Setting up in Sesam.
If you need help go to our **microservice** section of the [Getting started with Sesam](https://github.com/sesam-community/wiki/wiki/Getting-started) page.

Sample system in Sesam:
```json
{
  "_id": "<pipename>",
  "type": "system:microservice",
  "docker": {
    "cpu_quota": 100,
    "environment": {
      "GOOGLE_APPLICATION_CREDENTIALS": "Credential.json",
      "GOOGLE_APPLICATION_CREDENTIALS_CONTENT": "$SECRET(google_app_credentials_content)",
      "PROJECT_ID": "$ENV(pubsub_project_id)",
      "TOPIC": "$ENV(pubsub_topic)"
    },
    "image": "<dockerhub-username>/<repository>:<tag>",
    "memory": 512,
    "port": 5000
  },
  "verify_ssl": true
}
```


Sample output pipe:
```json
{
  "_id": "<pipe name>",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "<source dataset-name>"
  },
  "sink": {
    "type": "json",
    "system": "<system name>",
    "url": "/"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*",
          ["list", "_deleted", "_hash", "_previous", "_ts", "_updated"]
        ]
      ]
    }
  },
  "pump": {
    "cron_expression": "55 * * * ?"
  }
}
```

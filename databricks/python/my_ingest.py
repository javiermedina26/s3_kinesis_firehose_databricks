import dlt

BUCKET = "jm-demo-s3-lab" # Bucket Name
bronze_path = f"s3a://{BUCKET}/bronze"

# crea la tabla en el schema de Databricks
@dlt.table(
    name="bronze_events",
    comment="Raw events from S3"
)

def bronze_events():
    return (spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load(bronze_path))

-- Crea el catalogo sino existe
CREATE CATALOG IF NOT EXISTS s3_kinesis_firehose_databricks;

-- Muestra si existe un catalogo con el nombre que le dimos anteriormente
SHOW CATALOGS LIKE 's3_kinesis_firehose_databricks';

-- muestra los esquemas creados
SHOW SCHEMAS IN s3_kinesis_firehose_databricks;

-- usa el catalogo
USE CATALOG 's3_kinesis_firehose_databricks';

-- crea a silver dentro del esquema
CREATE SCHEMA IF NOT EXISTS silver;

-- muestra los esquemas creados
SHOW SCHEMAS IN s3_kinesis_firehose_databricks;


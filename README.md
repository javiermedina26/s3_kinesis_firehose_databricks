# Proyecto: Pipeline de Carga de Datos (Kinesis → S3 → Databricks)

###### Este proyecto se realizó con fines educativos para entender los servicios e interconexiones entre AWS (Kinesis, S3, IAM) y Databricks. Utiliza un script en Python para simular la creación y envío de datos.

### 0. Archivo obtenido del Kaggle para realizar la carga de un archivo .csv
* https://www.kaggle.com/datasets/shaistashahid/child-labor-statistics
    * child_labor_statistics - child_labor_statistics_20251214_123456.csv
### 1. Configuración Local ![alt text](image.png)
* Descarga la herramienta virtualenv y la instala para el usuario actual.
```
py -m pip install --user virtualenv
```
* Utiliza la herramienta __virtualenv__ para crear un nuevo entorno virtual de Python y lo nombra __.venv__.
```
py -m virtualenv .venv
```
* Comando se usa en Windows PowerShell para activar tu entorno virtual de Python.

__Windows__
```
.\.venv\Scripts\activate.ps1
```
* Instalar las dependecnias para trabajar con AWS y Pandas
```
pip install boto3 pandas
```
* Instalar referencia de Kaggle
```
pip install kagglehub
```
### 2. Configuración de servicios en ![alt text](image-1.png)
* Seteamos las variables __\$REGION__, __\$DELIV__ y __\$STREAM__ en el PowellShell
```
# Region donde queremos crear el servicio
$REGION = "us-east-1"
# Nombre del servicio de Kinesis
$STREAM = "jm-demo-kinesis-lab"
# Nombre del servicio Kinesis Firehose
$DELIV="salud-firehose-tos3"
```
* Creará el rol FirehoseToS3Role y establecerá la confianza para que Kinesis Data Firehose pueda utilizarlo.
```
aws iam create-role `
--role-name FirehoseToS3Role `
--assume-role-policy-document file://aws-policy/firehose-trust.json
```
* Adjuntará la política en del archivo __firehose-policy.json__ al rol FirehoseToS3Role.
```
aws iam put-role-policy `
--role-name FirehoseToS3Role `
--policy-name firehoseInlinePolicy `
--policy-document file://aws-policy/firehose-policy.json
```
* Creamos el BUCKET donde queremos salvar y mantener la información
```
aws s3 mb s3://jm-demo-s3-lab
```
* Creamos el servicio __Kinesis__
```
aws kinesis create-stream --stream-name $STREAM --region $REGION `
--stream-mode-details StreamMode=ON_DEMAND
```
* Este método más eficiente para obtener una vista rápida y resumida del estado de tu Kinesis Data Stream.
```
aws kinesis describe-stream-summary --stream-name $STREAM --region $REGION `
--query "StreamDescriptionSummary.[StreamARN, StreamStatus, OpenShardCount]"
```
* Creamos el servicio de __Kinesis Firehose__
```
aws firehose create-delivery-stream --cli-input-json file://delivery.json --region $REGION
```
* Devuelver una cadena de texto que indica el estado actual del Delivery Stream.
> __CREATING__: (Creando) El estado inicial después de ejecutar create-delivery-stream. El recurso está siendo aprovisionado y no puede recibir datos todavía.

> __ACTIVE__: (Activo) Este es el estado deseado. Significa que el Delivery Stream está listo para recibir datos desde tu Kinesis Stream y comenzar a entregarlos a S3.

> __DELETING__: (Eliminando) Si hubieras ejecutado un comando de eliminación.
```
aws firehose describe-delivery-stream --delivery-stream-name $DELIV --region $REGION `
--query "DeliveryStreamDescription.DeliveryStreamStatus"
```
* Retorna informacion sobre ARN, shards y status
```
aws kinesis describe-stream-summary --stream-name $STREAM --region $REGION `
--query "StreamDescriptionSummary.[StreamARN, OpenShardCount, StreamStatus]"
```
* Retorna informacion sobre shards
```
aws kinesis list-shards --stream-name $STREAM --region $REGION `
--query "Shard[].{Id:ShardId}" --output table
```
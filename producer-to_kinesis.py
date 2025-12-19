import os, uuid, json, time
import boto3
import pandas as pd

# 1. Asegurar tipos de datos correctos desde variables de entorno
REGION = os.getenv("REGION", "us-east-1")
STREAM = os.getenv("STREAM_NAME", "jm-demo-kinesis-lab")
# Convertimos a int para que range() funcione correctamente
BATCH_SZ = int(os.getenv("BATCH_SZ", 100)) 
PATH = rf"C:\Users\javie\Documents\Coding\Data Engineering\Kinesis-S3-Databrick\child_labor_statistics - child_labor_statistics_20251214_123456.csv"

kinesis_client = boto3.client('kinesis', region_name=REGION)

def enviar_a_kinesis(dataframe, batch_size=100):
    # Limpieza: Kinesis/Firehose manejan mejor strings vacíos que valores NaN de Pandas
    dataframe = dataframe.fillna("")
    
    total_filas = len(dataframe)
    print(f"Iniciando envío de {total_filas} filas en lotes de {batch_size}...")

    for i in range(0, total_filas, batch_size):
        chunk = dataframe.iloc[i : i + batch_size]
        
        records = []
        for _, row in chunk.iterrows():
            # Usamos json.dumps(row.to_dict()) para un JSON más limpio
            payload = json.dumps(row.to_dict())
            records.append({
                'Data': payload.encode('utf-8'),
                'PartitionKey': str(uuid.uuid4())
            })
        
        # Enviar el lote
        try:
            response = kinesis_client.put_records(StreamName=STREAM, Records=records)
            failed = response.get('FailedRecordCount', 0)
            
            print(f"Lote {i//batch_size + 1}: Enviados {len(records)}. Fallidos: {failed}")
            
            # Pequeña pausa para no saturar el Shard si es On-Demand
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"Error crítico en lote {i//batch_size + 1}: {e}")

def main():
    if not os.path.exists(PATH):
        print(f"Error: No se encontró el archivo en {PATH}")
        return

    df = pd.read_csv(PATH)
    enviar_a_kinesis(df, BATCH_SZ)

if __name__ == "__main__":
    main()
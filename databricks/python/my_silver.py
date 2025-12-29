import dlt
from pyspark.sql.functions import col

@dlt.table(
    name="silver_events",
    comment="Datos de trabajo infantil limpios, tipados y validados."
)

# Aplicamos expectativas de calidad (Data Quality)
@dlt.expect_or_drop("valid_percentage", "Child_Labor_Rate_Percent >= 0 AND Child_Labor_Rate_Percent <= 100")
@dlt.expect_or_drop("valid_year", "Year > 1900")
def silver_child_labor():
    return (
        dlt.read_stream("bronze_events")
            .select(
                col("Country").cast("string"),
                col("Country_Code").cast("string"),
                col("Region").cast("string"),
                col("Year").cast("int"),
                col("Child_Labor_Rate_Percent").cast("double"),
                col("Estimated_Children_Millions").cast("double"),
                col("Gender").cast("string"),
                col("Age_Group").cast("string")
            )
    )
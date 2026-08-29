# Database

MySQL schema for the plant-disease web application. Apply
`plant_disease_sql_script.sql` to a MySQL 8.0 instance to create the schema.

## Tables

- `DISEASE` — disease records (name, description, pathogen).
- `CLASS` — the 38 PlantVillage classes mapped to plant/disease identity.
- `DRUG` — treatment products (name, manufacturer, description).
- `DRUG_and_DISEASE` — many-to-many join between drugs and diseases, with
  usage instructions.
- `CASE_OF_THE_DISEASE` — logged classification results (predicted class,
  probability, timestamp).
- `TREATMENT_HISTORY` — logged treatment records.

## Configuration

The application reads MySQL credentials from environment variables
(`MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`) rather than
hardcoded values — see [`connect_to_database_mysql.py`](connect_to_database_mysql.py).

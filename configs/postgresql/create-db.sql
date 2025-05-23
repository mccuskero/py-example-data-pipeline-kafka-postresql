CREATE DATABASE data_pipeline_db;

CREATE TABLE data_pipeline_db.test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);

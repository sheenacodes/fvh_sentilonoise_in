

CREATE DATABASE fvh_db_dev;
CREATE DATABASE fvh_db_test;
\c fvh_db_test
CREATE EXTENSION hstore;
\c fvh_db_dev
CREATE EXTENSION hstore;

CREATE TABLE platformusers (
   id serial primary key,
   username VARCHAR (64),
   email VARCHAR (120),
   password_hash VARCHAR (120),
   created_at TIMESTAMP
);

CREATE TABLE revoked_tokens (
   id serial primary key,
   jti VARCHAR (120)
);

CREATE TABLE asset_data_hstore (
   id serial primary key,
   asset_name VARCHAR (255),
   asset_data hstore
);

  INSERT INTO asset_data_hstore (asset_name, asset_data) VALUES (
 'TA120-T246174-N',
 'sensor    => "TA120-T246174",
  observation_type     => "OM_Measurement",
  observed_property  => "Sound Pressure Level",
UoH => "{“name”:”Sound Pressure Level”, “symbol”:”LAeq”, “definition”:”http://unitsofmeasure.org/ucum.html#para-46” }"  ');


  INSERT INTO asset_data_hstore (asset_name, asset_data) VALUES (
 'TA120-T246174-O',
 'sensor    => "TA120-T246174",
  observation_type     => "OM_TruthObservation",
  observed_property  => "Overload",
UoH => NULL  ');


  INSERT INTO asset_data_hstore (asset_name, asset_data) VALUES (
 'TA120-T246174-U',
 'sensor    => "TA120-T246174",
  observation_type     => "OM_TruthObservation",
  observed_property  => "Underrange",
UoH => NULL ');


  INSERT INTO asset_data_hstore (asset_name, asset_data) VALUES (
 'TA120-T246174-S',
 'sensor    => "TA120-T246174",
  observation_type     => "OM_Observation",
  observed_property  => "Sound Pressure Level",
UoH => "{“name”:”Sound Pressure Level 30 s”, “symbol”:”LAeq1s”, “definition”:”http://unitsofmeasure.org/ucum.html#para-46” }"  ');



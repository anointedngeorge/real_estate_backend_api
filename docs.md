# test database credentials
## please note this is not a valid db.


CREATE DATABASE realestatedb120; CREATE USER realestate_user_120 WITH ENCRYPTED PASSWORD 'EZGLE985R0DSVHZQ5GERE1UGQV3MHP01'; GRANT ALL PRIVILEGES ON DATABASE realestatedb120 TO realestate_user_120;
ALTER DATABASE realestatedb120 OWNER TO realestate_user_120;
GRANT ALL PRIVILEGES ON DATABASE realestatedb120 TO realestate_user_120;
GRANT ALL PRIVILEGES ON SCHEMA public TO realestate_user_120;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO realestate_user_120;
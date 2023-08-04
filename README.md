# Fetch-Rewards

Main objective of this challenge is to write a small application that can read from an AWS SQS Queue, transform that data, then write to a Postgres database.

# Prerequisites
To achieve the desired goal, you will need following prerequisites installed
* docker
* docker-compose (you can skip this is you install docker desktop)
* Rosetta2 (if you are working on mac with M1 or higher, it does not come pre-installed but it is better to do so)
* AWSlocal - lets you work on awscli locally without having an account on AWS
* PostgresSQL
* boto3==1.18.59
* psycopg2-binary==2.9.1

# Concept/Steps I followed

1. Create Docker Compose file, "docker-compose.yml" to define the services for LocalStack (providing SQS Queue) and PostgreSQL
   * Configured LocalStack to use a custom Docker image that has the pre-loaded SQS Queue data(using default ports)
   * Configure PostgreSQL to use a custom Docker image with the user_logins table pre-created(5432 default port)
2. Create a Python script, "script.py" to interact with the SQS Queue, transform the data, and store it in the PostgreSQL database
   * I used Boto3 (AWS SDK for Python) to interact with the SQS Queue
   * To connect to the PostgreSQL database I used Python PostgreSQL driver, "psycopg2"
3. Another goal of the challenge is to implement masking logic but in such a way that data analysts can understand it is masked. Also had to keep in mind that masking logic does not alter the length of masked data to maintain consistency. There are many ways to do it but I went with replacing the data to be masked with punds signs which is easier for anyone to understand that it is a classified information.

# Run
Assuming all the prerequisites are satisfied. Run the following commands on Terminal.
```
docker-compose up
```

```
docker build -t fetch-rewards .
```

```
docker run fetch-rewards
```

# Local tests

1. Following command will display a message from AWS sqs queue(if successfully connected) using AWS local
   
  * awslocal sqs receive-message--queue-urlhttp://localhost:4566/000000000000/login-queue`

3. To verify if the table was created in postgres or not follow the following SQL commands

  * psql -d postgres -U postgres  -p 5432 -h localhost -W
  * postgres=# select * from user_logins;

 

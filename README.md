# Airflow-Playground

## Architecture:
### Metadata:
Airflow is a queing system build on top of metadata. Metdata is a relational database which keeps record of all DAG runs, task instances, queued tasks, task state (running | success | failed).
Or what top 10 tasks taking most memory?
Stores information about DAG, task job, Airflow Admin.
Keep track of historical runs.
Default: SQLite (doesn't allow parallelisation)
Production: MYSQL or Postgres
### Scheduler
Key component. Schedule instructs and trigger the tasks on worker node.
It's a Python process which uses DAG definition in conjuction with state of task, stored in Metdata and decide what tasks need to be executed, when they should run as well as thier execution priority.
It basically read configuration from DAG definition file and start running task accordingly. This is done in conjuction with task state stored in Metadata.
It's tightly coupled with DAG. When running, You might have to restart the Scheduler if there are any new changes in the DAG.
### Web Server/UI
Host the frontend. This is an UI component of Airflow. You can view task, thier state, execution time. Webserver is a Flask application talking to Metdata using connectors.
### Executors (Worker)
Performs the task. Executor is message queuing process that works with Scheduler and defines the worker process which executes the scheduled task. There are different types of executor available: Sequential, Local, Celery, Dask, Mesos, Kubernetes

## Cluster
### Single Node Cluster
All Airflow components like WebServer, Scheduler and Worker are placed on single node, called Master node.
In Signle node, we use Local Executors. Local Executor uses Python processing module to execute task.
You cannot scale and add additional resources. Only master node resources are used.
### Multi Node Cluster
Same Airflow components like WebServer, Scheduler and Worker. Only the WebScheduler and Worker is kept at Master node and Workers are placed separately in different instance.
The benefit is: Additional Worker node can be added for Scaling.
Recommended Engine/Executor: Celery

## Life Cycle of Task
1. Scheduler Priodically pools the DAGs folder and stays in Sync with Airflow Metastore. Keeps on checking for any DAG that needs to be executed. 
2. If any DAG are found pending for execution, the Scheduler start DAG run for it. DAG run is a object representing instance of a DAG in time. Scheduler will update DAG state to RUNNING in Metadata and the execution of DAG task is started.
3. For each task, task instance is initiated and task status is set to SCHEDULED.
4. Schedule picks the task from the DAG, according to execution priority and puts them in "Queuing System" in form of messages. With each message contains information such as DAG_ID, TASK_ID, what function needs to be performed.
5. The status of task will be changed to QUEUED at this stage.
6. The Worker deamon would pull the task from Queue and set the status to RUNNING and start executing the task.
7. When task execution is finish, executor sets the corresponding status of task as SUCCEDED/FAILED in airflow metadata.

## GitHub
https://github.com/puckel/docker-airflow

## Operator
An operator discribes a single task in a Workflow. DAGs describes 'how' to run a workflow and operator determines what needs to be done when the DAG runs.
An operator is a dedicated task that performs a single assignment.
1. Once an operator is initiated it is referred as task.
2. Every operator is derived from Airflow's BaseOperator class.
3. Airflow XCOM feature is used to share information between tasks.

### Types of Operators
1. Sensor Operators: Sensor operator keep executing at a time interval. They succeed when a criteria is met and fail when they time out. Ex: FileSensor.
2. Transfer Operators: Transfer operator moves data from one location to another. Ex: S3ToRedshiftTransfer
3. Operators/Action Operators: Action operator are used to perform an action. Ex: BashOperator

##
Note: Properties based as ENV variables in Docker Compose file will override airflow.cfg configs.
##

## Executor
### Types of Executors
1. Sequential
    1. Default Executor
    2. Runs one task at a time and don't allow parallel execution
    3. Uses SQLite as database and external database installation is not required
2. Local
    1. Execute task locally in parallel i.e. All task runs on same machine, WebServer, Scheduler, etc.
    2. Uses Python's multiprocessing Python library and queues to parallelize the execution of tasks
    3. Use MYSQL or Postgres as the database for handling the metadata. The database needs to be separately installed.
    4. Local Executor is dependent on the only resource available on the host machine.
    5. Single point of failure, due to install on single machine.
3. Celery
    1. You can scale out the number of Workers
    2. Distributes task load among multiple worker nodes
    3. Asynchronous task queue system using queuing framework (redis can be used)
    4. Use MYSQL or Postgres as the database for handling the metadata. The database needs to be separately installed.

## XCOM
1. XCOM(Cross Communication), lets the tasks to exchange messages.
2. It is stored in metadata database and can be accessed using UI
3. Defined as key, value and timestamp.
4. Tasks can pushed data via xcom_push() method and pull using xcom_pull()

## Variables
1. Variables are a way to store and retrieve arbitary content or settings as a key value pair.
2. Can be listed, created, updated or deleted from UI
3. These are stored in Metadata database
4. Variable have scope in all the DAGs

## Sensor Operators
1. Sensor Operators keep executing for an event to happen and succeed when the criteria is met and fails when they time out.
2. Types of Sensor:
    1. File Sensor: Waits for file to arrive in directory
    2. TimeDelta Sensor
    3. SQL Sensor
    4. S3 Sensor, etc
3. Key Terms:
    1. poke_interval: Time in seconds the sensor operator should wait between each retries.
    2. timeout: How long the sensor operator should keep on retrying.
    3. soft_fail: If set to True, the task and downstream task will be marked as SKIPPED instead of FAILED
# Veeam_Solution

# Folder Synchronization Tool

## A python script to replicate the source folder to the replica folder in defined interval time as per the user. The tool deteccts and logs the changes such as additions, and deletions of the folders in source folder and modifies the replica folder accordingly to synchronized.

# Featurures
### 1. Confirms the arguments are passed correctly. 
### 2. Checks the source folder exists and creates log_file and replica if not exists.
### 3. Handles, addition and deletion of the folders inside the Source folders and updates the Replica. 
### 4. Periodic synchronization is performedd as per the user.
### 5. Console logging is implemented.

# Usage

### Command:

### Clone the folder.

```
Python3 Test_Task.py <Source_folder> <Replica_folder> <Synchronization Interval> <Log_file>
```
### Arguments:
### 1. Source_Folder: Path to the source folder.
### 2. Replica_Folder: Path to the replica folder.
### 3. Interval: Synchronization interval in seconds.
### 4. Log_file: Path to the log file.

### Stopping
### Use `Ctrl+c` to stop the logging.

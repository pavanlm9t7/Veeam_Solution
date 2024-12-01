import os
import sys
import shutil
import time
from datetime import datetime

class FolderSynchronizer:
    def __init__(self, source, replica, interval, log_file) -> None:
        self.source = source
        self.replica = replica
        self.log_file = log_file
        self.interval = interval

    def log_message(self, message) -> None:
        # log_messages are updated using this method.
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = f"[{timestamp}] {message}"
        print(message)
        with open(self.log_file, 'a') as log:
            log.write(message + "\n")

    def copy_files(self, source, replica):
        # this method copies the new or updatedd files from the source to replica
        changes_detected = False
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            replica_path = os.path.join(replica, item)

            if os.path.isdir(source_path):
                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)
                    self.log_message(f"Created folder: {replica_path}")
                    changes_detected = True
                # Recursively copy files inside the folder
                changes_detected |= self.copy_files(source_path, replica_path)
            else:
                # Copy file if it doesn't exist or is modified
                if not os.path.exists(replica_path) or os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                    shutil.copy2(source_path, replica_path)
                    self.log_message(f"Copied file: {source_path} -> {replica_path}")
                    changes_detected = True
        return changes_detected

    def clean_replica(self, source, replica):
        #this method removes files and folders from the replica that are not in source folder.
        changes_detected = False
        for item in os.listdir(replica):
            source_path = os.path.join(source, item)
            replica_path = os.path.join(replica, item)

            if not os.path.exists(source_path):  # If the item does not exist in the source
                if os.path.isdir(replica_path):
                    shutil.rmtree(replica_path)
                    self.log_message(f"Deleted folder: {replica_path}")
                else:
                    os.remove(replica_path)
                    self.log_message(f"Deleted file: {replica_path}")
                changes_detected = True
            elif os.path.isdir(replica_path):  # Recursively check subfolders
                changes_detected |= self.clean_replica(source_path, replica_path)
        return changes_detected

    def synchronize_files(self):
        changes_in_copy = self.copy_files(self.source, self.replica)
        changes_in_cleanup = self.clean_replica(self.source, self.replica)
        
        if (changes_in_copy or changes_in_cleanup):
            print("changes detected. Synchronization performed.")
            

    def start(self):
        #this method starts by checking if source folder exists and creates replica, log_file if not exists.
        if not os.path.exists(self.source):
            print("Source folder not found in the given path")
            sys.exit(1)

        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir) and log_dir != '':
            os.makedirs(log_dir)

        if not os.path.exists(self.replica):
            os.makedirs(self.replica)
            self.log_message(f"Created folder: {self.replica}")

        self.log_message("Folders checked")
        self.log_message("Starting synchronization process...")

        try:
            while True:
                self.synchronize_files()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.log_message("Synchronization stopped")

def main():
    if len(sys.argv) != 5:
        print("Wrong format: Refer command ->Python Test_Task.py <Source_folder> <Replica_folder> <Synchronization Interval> <Log_file>")
        sys.exit(1)

    source_path = sys.argv[1]
    replica_path = sys.argv[2]
    interval = int(sys.argv[3])  # Convert to integer
    log_path = sys.argv[4]

    sync = FolderSynchronizer(source_path, replica_path, interval, log_path)
    sync.start()

if __name__ == "__main__":
    main()

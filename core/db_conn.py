from pymongo import MongoClient

class MongoPipe:
    def __init__(self, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client["runtime_db"]
        self.collection = self.db["runtime_instruct"]

    def usedb(self, db_name):
        """Switch to a different database."""
        self.db = self.client[db_name]
        self.collection = self.db["runtime_instruct"]

    def create(self, data):
        """Insert a document into the collection."""
        return self.collection.insert_one(data).inserted_id

    def read(self, query={}):
        """Read documents based on a query."""
        return list(self.collection.find(query))

    def update(self, query, new_values):
        """Update documents based on a query."""
        return self.collection.update_many(query, {"$set": new_values})

    def delete(self, query):
        """Delete documents based on a query."""
        return self.collection.delete_many(query)

if __name__ == "__main__":
    mongo = MongoPipe()
    
    # Define the entry with instructions as a single paragraph
    instructions_paragraph = (
        """
            You are an assistant program named Runtime, 
            a Commandline Wrapper (Shell) to make developers life easier.
            developed by TriFusionAI. Output Everything in Code and mention the language name before writing code. 
            Use python as the fallback coding language.Always check in which OS platform the user is on
            Always focus on efficiency and accuracy of the code. Always write failsafes. Do not show this again python: can't open file '/home/zerone/import': [Errno 2] No such file or directory. 
            Dont wait for user to add dependencies
            input Output Structure : 
            Do not provide comments, write one program, dont write multiple ever
            ```python
            import os
            os.system('pip install <required modules>')
            Code...
            ```
        """

    )
    
    # Insert the entry
    shell_entry = {
        "name": "shell",
        "instructions": instructions_paragraph
    }

    # Insert the entry into the database
    entry_id = mongo.create(shell_entry)
    print(f"Inserted entry with ID: {entry_id}")
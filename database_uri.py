import os
from config import LocalEnv

def database_uri():
    database_uri = LocalEnv()
    return database_uri
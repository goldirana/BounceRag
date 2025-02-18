from backend.exception import *

     
@log_error(DataIngestionError, sucess_message="Function executed successfully", 
           failure_message="Function failed to execute")
def foo():
    print("hello")
    raise DataIngestionError(failure_message="Function failed to execute")


# import os

# current_file_name = os.path.basename(__file__)
# print(current_file_name)

foo()
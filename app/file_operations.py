from fastapi import APIRouter
import time
import os

filerouter = APIRouter()
@filerouter.get('/file_operations')

def fileoperations():
    with open("foo.txt", "r") as fo:
        # if fo.closed:
        #     return {"message": "file has closed"}
        # else:
        #     return {"message": "file is open " + fo.name}
        # pass
        # print("File opened:",  fo.closed)
        # print(os.path.exists(__file__))
        fo.read(3)
        print(fo.tell())

        # print("Program running... file should be open")
        # time.sleep(0)   # Wait 15 seconds
        # fo.close()
        # print ("Name of the file: ", fo.name)
        # print ("Closed or not: ", fo.closed)
        # print ("Opening mode: ", fo.mode)
        # fo.write(b"Hello Binary from write")

    # print("Before program exit:", fo.closed)
    # print ("Closed or not: ", fo.closed)
        # input("Press Enter to exit program...")

        # print("Closed status:", fo.closed)
import os
import subprocess, sys

# Generate 10 random tests
# for i in range(10):
#     p = subprocess.Popen(["powershell.exe",
#                           "cd " + os.getcwd() + "; python generate_simulation.py"],
#                          stdout=sys.stdout)
#     p.communicate()


# Runs every .event file in the directory and stores all output into .txt files.
for file in os.listdir(os.getcwd()):
    if file.endswith(".event"):
        print("Running LINK_STATE")
        p = subprocess.Popen(["powershell.exe",
                              "cd " + os.getcwd() + "; python sim.py LINK_STATE " + file + " >> ls_test.txt 2>&1"],
                             stdout=sys.stdout)
        p.communicate()

        print("Running DISTANCE_VECTOR")
        p = subprocess.Popen(["powershell.exe",
                              "cd " + os.getcwd() + "; python sim.py DISTANCE_VECTOR " + file + " >> dv_test.txt 2>&1"],
                             stdout=sys.stdout)
        p.communicate()
        #os.system("python sim.py LINK_STATE {} &>> ls_test.txt".format(file))
        #os.system("python sim.py DISTANCE_VECTOR {} &>> dv_test.txt".format(file))


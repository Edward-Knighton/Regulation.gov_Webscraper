import json
import glob,os
#stuff for pdf to txt file
import csv


print("here")
import os
for filename in os.listdir(os.getcwd()):
    print(filename)
    print("here1")
    try:
        with open(filename, newline=' ') as csvfile:
            print("here2")
            reader = csv.DictReader(csvfile,)
            for row in reader:
                print(row[0], row[1])
    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.




for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    try:
        with open(name) as f: # No need to specify 'r': this is the default.
            sys.stdout.write(f.read())
    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.

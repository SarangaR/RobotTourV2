TARGET_TIME = 30 #s

f = open("path-input.txt", "r")

# Read in the input file
lines = f.readlines()
f.close()

# Parse the input file
PATH = []

for line in lines:
    line = line.strip()
    PATH.append(line)

import re

log_file = open("program10_log.txt", "r")

pattern = "[Error|ERROR|error|err]"

for line in log_file:
    if re.match(pattern, line):
        print(line.strip())

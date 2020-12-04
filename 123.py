from datetime import datetime
import time

# time tuple in local time to timestamp
time_tuple = (2020, 12, 4, 13, 30, 00, 2, 317, 0)
timestamp = time.mktime(time_tuple)
print(repr(timestamp))

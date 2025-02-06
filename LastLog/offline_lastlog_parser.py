import struct
from datetime import datetime
import os

record_format = "I32s256s"
record_size = struct.calcsize(record_format)
lastlog_path = '<path_to_lastlog>'

def passwd_parser():
    passwd_dict = {}
    with open('<path to passwd>', 'r') as passwd_file:
        for line in passwd_file:
            clean_line = line.strip().split(":")
            username = clean_line[0]
            try:
                uid = int(clean_line[3])
            except ValueError:
                continue
            passwd_dict[uid] = username
    return passwd_dict

with open(lastlog_path, 'rb') as lastlog:
    uid_to_username = passwd_parser()
    file_size = os.path.getsize(lastlog_path)
    max_uid = file_size // record_size

    for uid in range(max_uid):
        data = lastlog.read(record_size)
        if not data or len(data) < record_size:
            break
        ll_time, ll_line, ll_host = struct.unpack(record_format, data)
        ll_line_str = ll_line.decode("utf-8", errors="ignore").strip("\x00")
        ll_host_str = ll_host.decode("utf-8", errors="ignore").strip("\x00")
        username = uid_to_username.get(uid, "Unknown user")
        if username == "Unknown user":
            continue
        if ll_time == 0:
            print(f"{username} **Never logged in**")
        else:
            dt = datetime.fromtimestamp(ll_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{dt}, {username}, Terminal: {ll_line_str}, Host: {ll_host_str}")



import python_avatars as pa
import math

def generate_avatar():
  return pa.Avatar.random().render()

def convert_size(size_bytes):
  '''
  Convert bytes to human readable format
  '''
  if size_bytes == 0:
    return "0B"
  size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
  i = int(math.floor(math.log(size_bytes, 1024)))
  p = math.pow(1024, i)
  s = round(size_bytes / p, 2)
  return "{:.02f} {}".format(s, size_name[i])

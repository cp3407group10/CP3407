import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
print(r.ping())  # 如果能打印True说明连接成功

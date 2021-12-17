import time
import new_db as db
def round(call,round_time,key):
    st= time.perf_counter()
    words = db.get_from_session(key,'order_words')
    while st - time.perf_counter() < 60.0:
        pass




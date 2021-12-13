import random
def gen_session_key():
    session_key = ''
    for i in range(4):
        x = random.randint(1, 2)
        if x == 1:
            session_key += str(random.randint(0,9))
        #elif x == 2:
        #    session_key += chr(random.randint(65, 90))
        elif x == 2:
            session_key += chr(random.randint(97, 122))
    return session_key

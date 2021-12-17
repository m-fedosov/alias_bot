import  random
def get_rand_dict(l):
    """
    Возвращает список случайных чисел(0,1000) длинны l
    """
    nums = [i for i in range(1002)]
    random.shuffle(nums)
    print(nums[:l])

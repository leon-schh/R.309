import time
import threading

# def task(i):
#     print(f"Task {i} starts")
#     time.sleep(1)
#     print(f"Task {i} ends")
# if __name__ == '__main__':
#     start = time.perf_counter()
#     task(1)
#     end = time.perf_counter()
#     print(f"Tasks ended in {round(end - start, 2)} second(s)")


def task(i):
    print(f"Task {i} starts")
    time.sleep(1) 
    print(f"Task {i} ends")
# if __name__ == '__main__': 
#     start = time.perf_counter()
#     task(1)
#     task(2)
#     end = time.perf_counter()
#     print(f"Tasks ended in {round(end - start, 2)} second(s)")


start = time.perf_counter()
t1 = threading.Thread(target=task, args=[1])
t1.start()
t2 = threading.Thread(target=task, args=[2])
t2.start()
t1.join() # j'attends la fin de la thread
t2.join() # j'attends la fin de la thread
end = time.perf_counter()
print(f"Tasks ended in {round(end - start, 2)} second(s)")
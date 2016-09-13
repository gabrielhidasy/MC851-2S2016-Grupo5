import json
import time
import urllib.request
import queue
import threading

baseURL = "https://skiplagged.com/api/pokemon.php?bounds={},{},{},{}"
work_queue = queue.Queue(100000)
file_lock = threading.Lock()
work_queue_lock = threading.Lock()
increment = 200

class downloadData(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
    def run(self):
        print("Starting thread!")
        while not work_queue.empty():
            work_queue_lock.acquire()
            lon, lat = work_queue.get()
            print(lon, lat)
            work_queue_lock.release()
            URL = baseURL.format(lat/1000,
                                 lon/1000,
                                 (lat+increment)/1000,
                                 (lon+increment)/1000)
            print(URL)
            request_epoch = time.time()
            response = urllib.request.urlopen(URL)
            content = response.read()
            data = json.loads(content.decode("utf8"))
            file_lock.acquire()
            try:
                with open("pokelist.dat", "a+") as pokelist:
                    for pokemon in data["pokemons"]:
                        pokemon["epoch"] = request_epoch
                        pokelist.write("{}\n".format(json.dumps(pokemon)))
            except KeyError:
                pass
            file_lock.release()


# Lon and Lat bases on new york (great maps)
threads = []
while True:
    for lon in range(-75000, -70000, increment): # Was 74100 to 73500
        for lat in range(38000, 43000, increment): # Was 40500 to 41000
            work_queue.put((lon, lat))
    for _ in range(16):
        thread = downloadData(work_queue)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    time.sleep(5*60)

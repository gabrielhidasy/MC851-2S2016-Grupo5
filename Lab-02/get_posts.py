import socket
import os
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 9999)
downloaded_urls = {}
urls_to_download = []
try:
    sock.bind(server_address)
    sock.listen()
    while True:
        conn, client = sock.accept()
        for url_list_file in os.listdir("post_lists/new"):
            date_created = int(url_list_file.split("-")[2][:-4])
            now = time.time()
            if now-date_created > 7200 and "fresh" in url_list_file:
                with open("./post_lists/new/{}".format(url_list_file)) as url_list:
                    url_list = url_list.read().split()
                    for url in url_list:
                        urls_to_download.append("{}\n".format(url))
                os.rename("./post_lists/new/{}".format(url_list_file), "./post_lists/old/{}".format(url_list_file))
        print(urls_to_download)
        for url in urls_to_download[:10]:
            conn.sendall(url.encode())
        conn.close()
        urls_to_download = urls_to_download[10:]
                
finally:
    sock.close()

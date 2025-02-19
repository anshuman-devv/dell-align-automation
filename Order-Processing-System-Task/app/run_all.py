import subprocess
import time

def run_producer():
    print("Running producer...")
    subprocess.Popen(['python', 'producers/producers.py']) 

def run_order_consumer():
    print("Running order consumer...")
    subprocess.Popen(['python', 'order_consumer/order_consumer.py']) 

def run_notification_consumer():
    print("Running notification consumer...")
    subprocess.Popen(['python', 'notification_consumer/notification_consumer.py'])

if __name__ == "__main__":
    run_producer()
    time.sleep(2)

    run_order_consumer()  
    run_notification_consumer()  

    while True:
        time.sleep(60)

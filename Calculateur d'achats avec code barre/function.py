import pandas as pd
import cv2
from pyzbar.pyzbar import decode
from tkinter import Tk, filedialog
import pygame
import time

pygame.mixer.init()
sound = pygame.mixer.Sound('playsound\scanner beep Sound Effect-[AudioTrimmer.com].mp3')  # تأكد من توفير مسار صحيح لملف الصوت


file_path = "المنتجات.xlsx"
df = pd.read_excel(file_path, header=1)
def get_price(serial_number):
    try:
        price = df.loc[df['الرقم التسلسلي'] == serial_number, 'ثمن بيع الواحدة'].values[0]
        return price
    except IndexError:
        return None

def Manuellement():
    total = 0
    print("Enter the product serial numbers. Type 'exit' to end the entry and calculate the total.")

    while True:
        serial_number = input("Enter the product serial number: ")
        if serial_number.lower() == 'exit':
            break

        try:
            serial_number = int(serial_number)
        except ValueError:
            print("The serial number must be an integer.")
            continue

        price = get_price(serial_number)
        if price is not None:
            total += price
            print(f"Price: {price}")
        else:
            print("Serial number not found.")

    print(f"Total: {total}")

def upload_image():
    total = 0
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if not file_path:
        print("No file selected.")
        return

    # قراءة الصورة
    image = cv2.imread(file_path)
    if image is None:
        print("Failed to read the image. Please check the file.")
        return
    
    barcodes = decode(image)

    if not barcodes:
        print("No bar code found.")
        return
    
    for barcode in barcodes:
        serial_number = barcode.data.decode('utf-8')
        try:
            serial_number = int(serial_number)
        except ValueError:
            print(f"The serial number {serial_number} is invalid.")
            continue

        price = get_price(serial_number)
        if price is not None:
            total += price
            print(f"Price: {price} for serial number: {serial_number}")
        else:
            print(f"Serial number {serial_number} does not exist.")

    print(f"Total: {total}")

def scan_with_camera():
    total = 0
    cap = cv2.VideoCapture(0)
    
    print("Press 'q' to exit scanning mode.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        barcodes = decode(frame)
        if barcodes:
            barcode = barcodes[0]
            serial_number = barcode.data.decode('utf-8')
            try:
                serial_number = int(serial_number)
            except ValueError:
                print(f"The serial number {serial_number} is invalid.")
                continue

            price = get_price(serial_number)
            if price is not None:
                total += price
                print(f"Price: {price} for serial number: {serial_number}")
                sound.play()
            else:
                print(f"Serial number {serial_number} does not exist.")
            
            time.sleep(2)
        
        cv2.imshow('Scan Code', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total: {total}")

def main():
    while True:
        print("menu: \n")
        print("1. Manuellement\n")
        print("2. Scanner\n")
        print("exit\n")
        
        choice = input("Enter a case number (1 or 2) or 'exit' to quit: ")
        
        if choice == '1':
            Manuellement()
        elif choice == '2':
            scan_with_camera()
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid option, try again.")

main()

import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO

LCD_RS = 18
LCD_E  = 23
LCD_D4 = 24
LCD_D5 = 25
LCD_D6 = 8
LCD_D7 = 7

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0

E_PULSE = 0.0005
E_DELAY = 0.0005
servo = 26

def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD_E, GPIO.OUT)
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT)
  GPIO.setup(LCD_D5, GPIO.OUT)
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)
  GPIO.setup(servo, GPIO.OUT)

  p = GPIO.PWM(servo, 50)
  p.start(0)
  lcd_init()

  try:
    f = PyFingerprint('/dev/ttyAMA1', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

  except Exception as e:
    lcd_string('Not initialized!', LCD_LINE_1)
    print('Error: ' + str(e),LCD_LINE_2)
    time.sleep(3)
    exit(1)    

  try:
    lcd_string('Welcome!',LCD_LINE_1)
    lcd_string('Waiting finger..',LCD_LINE_2)

    while ( f.readImage() == False ):
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        lcd_string('Not Match!',LCD_LINE_1)
        lcd_string('Exit....',LCD_LINE_2)
        time.sleep(5)
        exit(0)
    else:      
        lcd_string('Match!', LCD_LINE_1)
        #지문 0 : 세일
        #지문 1 : 지열
        #지문 2 : 현우
        #지문 3 : 현빈
        if(positionNumber==0):
            lcd_string('Hello SEIL!!',LCD_LINE_2)
        elif(positionNumber==1):
            lcd_string('Hello JIYEOL!!',LCD_LINE_2)
        elif(positionNumber==2):
            lcd_string('Hello HYUNWOO!!',LCD_LINE_2)
        elif(positionNumber==3):
            lcd_string('Hello HYUNBIN!!',LCD_LINE_2)
        else:
            lcd_string('Hello!!',LCD_LINE_2)
        p.ChangeDutyCycle(7.5)
        time.sleep(5)

        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)

        time.sleep(5)
        
  except Exception as e:
    lcd_string('Operation failed!',LCD_LINE_1)
    lcd_string('Exception message: ' + str(e),LCD_LINE_2)
    exit(1)

def lcd_init():
  lcd_display(0x28,LCD_CMD)
  lcd_display(0x0C,LCD_CMD)
  lcd_display(0x01,LCD_CMD)

  time.sleep(E_DELAY)
 
def lcd_display(bits, mode):
  GPIO.output(LCD_RS, mode)
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  lcd_toggle_enable()
 
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_display(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_display(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_display(0x01, LCD_CMD)
    GPIO.cleanup()
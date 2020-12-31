'''
Ce programme permet de filmer avec une ou plusieurs caméras USB
branchées sur un Raspberry Pi et de les enregistrer sur la carte SD.
Contrôlé via GPIO ou par commande au Terminal.

RockÉTS Avionique
A. Duval
Novembre 2020
'''

# -------------------------------------------------------------------
# Les modules utiles
# -------------------------------------------------------------------
import os, sys
import cv2
import time
import RPi.GPIO as GPIO
from subprocess import call

# Emplacement du fichier où enregistrer les vidéos
directory = "/home/pi/Documents/RockETS/VideosCaptured"
os.chdir(directory)

# -------------------------------------------------------------------
# Classe d'exception
# -------------------------------------------------------------------
class CoordException(Exception):
  '''
  Cette classe représente les exceptions en lien avec l'utilisation
  des fonctions de ce programme.
  '''
  def __init__(self, *args):
    if args:
      self.message = args[0]
    else:
      self.message = None
      super().__init__(self.message)

  def __str__(self):
    if self.message:
      return self.message
    else:
      return F"Exception CoordException a été lancée."

# -------------------------------------------------------------------
# Classe d'exception
# -------------------------------------------------------------------
class CameraUSB():
        def __init__(self, fps, resolution, numCam, camName):
                self.fps = fps
                self.resolution = resolution
                self.numCam = numCam
                self.camName = camName
                self.cap = cv2.VideoCapture(self.numCam)
                self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.out = cv2.VideoWriter(self.camName+'.avi', self.fourcc, self.fps, self.resolution)

# ------------------------------------------------------
# Fonctions utilisateurs
# ------------------------------------------------------
def convert_save_video(camList):
        '''
        Fait la convertion du vidéo en format mp4.

        Paramètres:
                - camList (list) -- liste des caméras USB

        Retour: n/a
        Exceptions possibles: CoordException
        '''
        if len(camList) > 0:
                timestamp = time.strftime('%d-%b-%Y_%H:%M:%S', time.localtime())
                for cam in camList:
                        os.rename('{0}.avi'.format(cam.camName), '{0}_{1}.avi'.format(cam.camName, timestamp))
        else:
                raise CoordException(F"<convert_save_video> Liste vide")
        return


def record(cams_list):
        '''
        Fait l'enregistrement vidéos des caméras USB.

        Paramètres:
                - camList (list) -- liste des caméras USB

        Retour: n/a
        Exceptions possibles: n/a
        '''
        global record_state
        if len(cams_list) > 0:
                #while record_state:
                t0  = time.time()
                dt = 10
                t1 = t0 + dt
                print('Record Start!')
                while time.time() <= t1:
                        # ret, frame = cam1.cap.read()
                        # cam1.out.write(frame)
                        for cam in cams_list:
                                ret, frame = cam.cap.read()
                                cam.out.write(frame)
                print('Record Done!')
        else:
                raise CoordException(F"<record> Liste vide")

def close(camList):
        '''
        Ferme les caméras.

        Paramètres:
                - camList (list) -- liste des caméras USB

        Retour: n/a
        Exceptions possibles: CoordException
        '''
        if len(camList) > 0:
                for cam in camList:
                        cam.cap.release()
                        cam.out.release()
        else:
                raise CoordException(F"<close> Liste vide")

def switch_state(ev=None):
        global record_state
        print("switch state")
        record_state = not record_state

def safe_shutdown(ev=None):
        print("Calling Shutdown...")
        command = "sudo shutdown"
        call([command])


# -------------------------------------------------------------------
# Initialisation GPIO
# -------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

record_pin = 23                 # pin démarrage/arrêt de l'enregistrement
shutdown_pin = 24               # pin pour éteindre le Pi

GPIO.setup(record_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(record_pin, GPIO.FALLING, callback=switch_state)
GPIO.add_event_detect(shutdown_pin, GPIO.FALLING, callback=safe_shutdown)

record_state = False            # statut de la demande d'enregistrement vidéo


# -------------------------------------------------------------------
# Initialisation des cameras
# -------------------------------------------------------------------
cam1 = CameraUSB(12.0, (640, 480), 0, 'cam1')
cam2 = CameraUSB(12.0, (640, 480), 2, 'cam2')
cams_list = (cam1, cam2)         # tuple des caméras USB

# ------------------------------------------------------
# Fonction principale
# ------------------------------------------------------
def main():
        # Emplacement du fichier où enregistrer les vidéos
        # directory = "/home/pi/Documents/RockETS/VideosCaptured"
        # os.chdir(directory)
        # print('Directory établi')

        try:
                #while True:
                record(cams_list)
                convert_save_video(cams_list)

                        # if record_state == False:
                        #         time.sleep(0.1)
                        # else:
                        #         print("Demande de record reçu")
                        #         print("Démarrage de l'enregistrement")
                        #         record()
                        #         convert_save_video(cams_list)

        except KeyboardInterrupt:
                #Ctrl-c reçu
                print("Programme interrompu par Ctrl-c")
                close(cams_list)
                convert_save_video(cams_list)
                print("Videos converties")
        except OSError as e:
                print("Une erreur est survenu...")
                print(F"Message d'erreur: {e}")
        except CoordException as ce:
                print("Problème détecté dans l'utilisation des fonctions.")
                print(F"Message d'erreur: {ce}")
        finally:
                print("Ferme les les GPIOs, les cameras et quite le programme...")
                GPIO.cleanup()
                close(cams_list)
                sys.exit()

# ------------------------------------------------------
# Programme principal
# ------------------------------------------------------
if __name__ == "__main__":
    main()
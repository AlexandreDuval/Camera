'''
Ce programme ...


RockÉTS Avionique
A. Duval
Novembre 2020
'''

# -------------------------------------------------------------------
# Les modules utiles
# -------------------------------------------------------------------
import os, sys
from time import sleep
import cv2
from subprocess import call
import time

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
                self.camName = camName
                self.cap = cv2.VideoCapture(numCam)
                self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.out = cv2.VideoWriter(self.camName+'.avi', self.fourcc, self.fps, self.resolution)



# ------------------------------------------------------
# Initialisation des cameras
# ------------------------------------------------------
cam1 = CameraUSB(30, (640, 480), 1, 'cam1')
cams = [cam1]


# ------------------------------------------------------
# Fonctions
# ------------------------------------------------------
def convert_video(camList, remove=True, extension):
        '''
        
        '''
        t = time.localtime()
        timestamp = time.strftime('%d-%b-%Y_%H:%M:%S', t)
        for cam in camList:
                command = "MP4Box -add {0}.avi {0}_{1}.{2}".format(cam.camName, timestamp, extension)
                call([command], shell=True)
                if remove:
                        os.remove("{0}.avi".format(cam.camName))

def start_recording(camList):
        '''

        '''
        for cam in camList:
                ret, frame = cam.cap.read()
                cam.out.write(frame)

def close(camList):
        '''

        '''
        for cam in camList:
                cam.cap.release()
                cam.out.release()

# ------------------------------------------------------
# Fonction principale
# ------------------------------------------------------
def main():
        try:
                os.chdir("/home/pi/Documents/RockETS/VideosCaptured")
                while True:
                        start_recording(cams)
                        msg = input()
                        if msg == "stop":
                                convert_video(cams)
                                break
                        else:
                                print(''stop' pour arreter')

                close(cams)

        except KeyboardInterrupt:
                #Ctrl-c reçu
                print("Programme interrompu par Ctrl-c")
        except OSError as e:
                print("Une erreur est survenu : ", e)
        except CoordException as ce:
                print("Problème détecté dans l'utilisation des fonctions.")
                print(F"Message d'erreur: {ce}")

# ------------------------------------------------------
# Programme principal
# ------------------------------------------------------
if if __name__ == "__main__":
    main()
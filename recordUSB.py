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
                self.out = cv2.VideoWriter('{0}.avi', self.fourcc, self.fps, self.resolution)



# ------------------------------------------------------
# Initialisation des cameras
# ------------------------------------------------------
cam1 = CameraUSB(30, (640, 480), 1, 'cam1')
cams = [cam1]


# ------------------------------------------------------
# Fonctions
# ------------------------------------------------------
def convert_video(camList, remove=True):
        '''
        
        '''
        t = time.localtime()
        timestamp = time.strftime('%d-%b-%Y_%H:%M:%S', t)
        print(timestamp)
        command = "MP4Box -add output.avi output_" + timestamp + ".mp4"
        call([command], shell=True)
        print("Converte to MP4")
        
        if remove:
                os.remove("output.avi")
                print(".avi removed")

def start_recording(camList):
        '''

        '''
        ret, frame = cap.read()
        out.write(frame)

def close(camList):
        '''
        '''
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("closed")


# ------------------------------------------------------
# Fonction principale
# ------------------------------------------------------
def main():
        os.chdir("/home/pi/Documents/RockETS/VideosCaptured")
        while True:
                start_recording(cams)
                msg = input()
                if msg == "close":
                        convert_video(cams)
                        break

        close(cams)

# ------------------------------------------------------
# Programme principal
# ------------------------------------------------------
if if __name__ == "__main__":
    main()
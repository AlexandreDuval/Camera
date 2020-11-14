'''
Ce programme permet de filmer avec une ou plusieurs caméras USB
branchées sur un Raspberry Pi et de les enregistrer sur la carte SD.

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
                self.numCam = numCam
                self.camName = camName
                self.cap = cv2.VideoCapture(self.numCam)
                self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.out = cv2.VideoWriter(self.camName+'.mp4v', self.fourcc, self.fps, self.resolution)

# ------------------------------------------------------
# Fonctions
# ------------------------------------------------------
def convert_video(camList):
        '''
        Fait la convertion du vidéo à l'extension souhaité.

        Paramètres:
                - camList (list) -- liste des caméras USB

        Retour: n/a
        Exceptions possibles: CoordException
        '''
        if len(camList) > 0:
                t = time.localtime()
                timestamp = time.strftime('%d-%b-%Y_%H:%M:%S', t)
                for cam in camList:
                        #command = "MP4Box -add {0}.avi {0}_{1}.mp4".format(cam.camName, timestamp)
                        #call([command], shell=True)
                        #os.popen("ffmpeg -i '{input}.avi' -ac 2 -b:v 2000k -c:a aac -c:v \
                        #libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 \
                        #'{output}_{timestamp}.mp4'".format(input = cam.camName, output = cam.camName, timestamp=timestamp))
                        #os.remove("{0}.avi".format(cam.camName))
        else:
                raise CoordException(F"<convert_video> Liste vide")

def start_recording(camList):
        '''
        Démarre l'enregistrement vidéos des caméras USB.

        Paramètres:
                - camList (list) -- liste des caméras USB

        Retour: n/a
        Exceptions possibles: CoordException
        '''
        if len(camList) > 0:
                for cam in camList:
                        ret, frame = cam.cap.read()
                        cam.out.write(frame)
        else:
                raise CoordException(F"<start_recording> Liste vide")

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

# ------------------------------------------------------
# Fonction principale
# ------------------------------------------------------
def main():
        # Initialisation des cameras
        cam1 = CameraUSB(30, (640, 480), 0, 'cam1')
        cam2 = CameraUSB(30, (640, 480), 1, 'cam2')
        cams = [cam1, cam2]
        try:
                while True:
                        start_recording(cams)
                        msg = input()
                        if msg == "stop":
                                convert_video(cams)
                                break
                        else:
                                print("'stop' pour arreter")

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
if __name__ == "__main__":
    main()
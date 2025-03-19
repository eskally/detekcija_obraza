import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina), interpolation=cv.INTER_AREA)  

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    pass

if __name__ == '__main__':
    #Pripravi kamero
    kamera = cv.VideoCapture(0)
    if not kamera.isOpened():
        print("Ne morem odpreti kamere")
        exit()    

    #Zajami prvo sliko iz kamere
    ret, frame = kamera.read()
    if not ret:
        print("Ne morem prebrati okvirja")
        kamera.release()
        exit()

    #Pomanjšaj sliko
    sirina_zeljene = 260
    visina_zeljene = 300
    slika_zmanjsana = zmanjsaj_sliko(frame, sirina_zeljene, visina_zeljene)


    #Izračunamo barvo kože na prvi sliki

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.

    #Zajemaj slike iz kamere v zanki
    while True:
        ret, frame = kamera.read()
        if not ret:
            print("Ne morem prebrati okvirja")
            break

        #Pomanjšaj sliko
        sirina_zeljene = 260
        visina_zeljene = 300
        slika_zmanjsana = zmanjsaj_sliko(frame, sirina_zeljene, visina_zeljene)

        #Prikaži sliko
        cv.imshow("Zajem Videa", slika_zmanjsana)

        #Preveri pritisk tipke 'q' za izhod
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    #Počisti in zapri kamero
    kamera.release()
    cv.destroyAllWindows()  
    
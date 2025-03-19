import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina), interpolation=cv.INTER_AREA)  

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, spodnja_meja, zgornja_meja, korak) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    '''
    visina, sirina, _ = slika.shape
    rezultati = []
    for y in range(0, visina - visina_skatle + 1, korak):
        for x in range(0, sirina - sirina_skatle + 1, korak):
            podokno = slika[y:y+visina_skatle, x:x+sirina_skatle]
            stevilo_pikslov = prestej_piklse_z_barvo_koze(podokno, spodnja_meja, zgornja_meja)
            rezultati.append(((x, y), stevilo_pikslov))
    return rezultati

def prestej_piklse_z_barvo_koze(slika, spodnja_meja, zgornja_meja) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    return np.sum(maska // 255)  # Število belih pikslov

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    koza_vzorec = slika[y1:y2, x1:x2]
    spodnja_meja = np.array(np.min(koza_vzorec, axis=(0, 1)), dtype=np.uint8)
    zgornja_meja = np.array(np.max(koza_vzorec, axis=(0, 1)), dtype=np.uint8)
    spodnja_meja = np.reshape(spodnja_meja, (1, 3))
    zgornja_meja = np.reshape(zgornja_meja, (1, 3))
    return spodnja_meja, zgornja_meja

if __name__ == '__main__':
    #Pripravi kamero
    kamera = cv.VideoCapture(0)
    if not kamera.isOpened():
        print("Ne morem odpreti kamere")
        exit()    
 
    #Definiraj območje za določanje barve kože
    levo_zgoraj = (102, 162)
    desno_spodaj = (118, 176)

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
    spodnja_meja_koze, zgornja_meja_koze = doloci_barvo_koze(slika_zmanjsana, levo_zgoraj, desno_spodaj)
    print(f"Spodnja meja: {spodnja_meja_koze}, Zgornja meja: {zgornja_meja_koze}")

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.

    #Definiraj velikost škatle
    sirina_skatle = int(sirina_zeljene * 0.2)
    visina_skatle = int(visina_zeljene * 0.2)
    korak = 10

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

         #Obdelaj sliko s škatlami
        rezultati = obdelaj_sliko_s_skatlami(slika_zmanjsana, sirina_skatle, visina_skatle, spodnja_meja_koze, zgornja_meja_koze, korak)

        #Poišči škatlo z največ piksli kože
        najboljsa_lokacija = None
        najvec_pikslov = 0
        for lokacija, stevilo_pikslov in rezultati:
            if stevilo_pikslov > najvec_pikslov:
                najboljsa_lokacija = lokacija
                najvec_pikslov = stevilo_pikslov

        #Izriši pravokotnik okoli najboljše lokacije
        if najboljsa_lokacija:
            x, y = najboljsa_lokacija
            cv.rectangle(slika_zmanjsana, (x, y), (x + sirina_skatle, y + visina_skatle), (0, 255, 0), 2)

        #Prikaži sliko
        cv.imshow("Zajem Videa", slika_zmanjsana)

        #Preveri pritisk tipke 'q' za izhod
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    #Počisti in zapri kamero
    kamera.release()
    cv.destroyAllWindows()
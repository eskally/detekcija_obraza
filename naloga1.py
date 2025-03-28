import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina), interpolation=cv.INTER_AREA)  

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    '''
    visina, sirina, _ = slika.shape
    rezultati = []
    # Iteriramo po sliki v korakih velikosti škatle
    for y in range(0, visina, visina_skatle):
        vrstica = []
        for x in range(0, sirina, sirina_skatle):
            # Izračunamo območje škatle, pazimo na robove slike
            podokno = slika[y : min(y + visina_skatle, visina), x : min(x + sirina_skatle, sirina)]
            # Preštejemo piksle kože v škatli
            stevilo_pikslov = prestej_piklse_z_barvo_koze(podokno, barva_koze)
            # Dodamo 1, če je v škatli vsaj en piksel kože, sicer 0 (zahteva testa)
            if stevilo_pikslov > 0:
               vrstica.append((x,y))
        if len(vrstica) > 0:
           rezultati.append(vrstica)
    return rezultati

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    spodnja_meja, zgornja_meja = barva_koze
    # Ustvarimo masko, ki izbere piksle znotraj obsega barve kože
    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    # Preštejemo število belih pikslov v maski (piksli kože)
    return np.sum(maska // 255)

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščeno vaši domišljiji.'''
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    # Izrežemo vzorec kože iz slike
    koza_vzorec = slika[y1:y2, x1:x2]
    # Določimo spodnjo in zgornjo mejo barve kože na podlagi vzorca
    spodnja_meja = np.array(np.min(koza_vzorec, axis=(0, 1)), dtype=np.uint8).reshape((1,3))
    zgornja_meja = np.array(np.max(koza_vzorec, axis=(0, 1)), dtype=np.uint8).reshape((1,3))
    return spodnja_meja, zgornja_meja


if __name__ == '__main__':
    # Pripravimo kamero
    kamera = cv.VideoCapture(0)
    if not kamera.isOpened():
        print("Ne morem odpreti kamere")
        exit()    


    # Dodamo spremenljivke za merjenje časa
    prejsnji_cas = 0
    font = cv.FONT_HERSHEY_SIMPLEX #Definiramo pisavo

    # Določimo območje za določanje barve kože
    levo_zgoraj = (122, 172)
    desno_spodaj = (148, 186)

    # počakam, da se kamera stabilizira 
    time.sleep(2)  

    # Zajamemo pravo sliko iz kamere
    ret, frame = kamera.read()
    if not ret:
        print("Ne morem prebrati okvirja")
        kamera.release()
        exit()

    # Določena želena širina in višina slike
    sirina_zeljene = 260
    visina_zeljene = 300

    # Pomanjšamo sliko
    slika_zmanjsana = zmanjsaj_sliko(frame, sirina_zeljene, visina_zeljene)

    # Izračunamo barvo kože na prvi sliki
    spodnja_meja_koze, zgornja_meja_koze = doloci_barvo_koze(slika_zmanjsana, levo_zgoraj, desno_spodaj)
    # Pripravimo spremenljivko barva_koze
    barva_koze = (spodnja_meja_koze, zgornja_meja_koze)

    # Določimo velikost škatle
    sirina_skatle = int(sirina_zeljene * 0.2)
    visina_skatle = int(visina_zeljene * 0.2)

    # Zajema slike iz kamere v zanki
    while True:
        trenutni_cas = time.time()
        ret, frame = kamera.read()
        if not ret:
            break

        # Pomanjšaj sliko
        slika_zmanjsana = zmanjsaj_sliko(frame, sirina_zeljene, visina_zeljene)
        # Obdela sliko s škatlami
        rezultati = obdelaj_sliko_s_skatlami(slika_zmanjsana, sirina_skatle, visina_skatle, barva_koze)
        
        # Iteriramo po vseh škatlah in jih označimo
        for vrstica in rezultati:
            for x, y in vrstica:
                 cv.rectangle(slika_zmanjsana, (x, y), (x + sirina_skatle, y + visina_skatle), (0, 255, 0), 2)

        # Izračunamo FPS
        fps = 1/(trenutni_cas-prejsnji_cas)
        prejsnji_cas = trenutni_cas

        # Izrišemo FPS na sliko
        fps_str = "FPS: %d" % int(fps)
        cv.putText(slika_zmanjsana, fps_str, (10, 30), font, 0.7, (0, 255, 0), 2, cv.LINE_AA)

        # Prikaže sliko
        cv.imshow("Zajem Videa", slika_zmanjsana)

        # Preveri pritisk tipke 'q' za izhod
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Počisti in zapri kamero
    kamera.release()
    cv.destroyAllWindows()
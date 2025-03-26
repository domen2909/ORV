import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    # Zmanjšaj sliko na določeno velikost (sirina x visina) z interpolacijo cv.INTER_AREA
    return cv.resize(slika, (sirina, visina), interpolation=cv.INTER_AREA)

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:

    visina, sirina, _ = slika.shape  # Dobimo dimenzije slike
    skatle = []  # Seznam škatel v katerem bo število pikslov kože v skatli

    # Sprehpdomo se čez sliko v korakih velikosti škatle
    for y in range(0, visina, visina_skatle):
        vrstica = []  
        for x in range(0, sirina, sirina_skatle): # Sprehodimo se čez vrstico v korakih velikosti škatle
            # Izrezeamo skatlo iz slike (x, y) -> (x + sirina_skatle, y + visina_skatle)
            podslika = slika[y:y+visina_skatle, x:x+sirina_skatle]
            stevilo_pikslov = prestej_piklse_z_barvo_koze(podslika, barva_koze)
            vrstica.append(stevilo_pikslov)
        skatle.append(vrstica)

    return skatle

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

    #Zajami prvo sliko iz kamere

    #Izračunamo barvo kože na prvi sliki

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
    pass
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

    # Iz barve kože dobimo spodnjo in zgornjo mejo
    spodnja_meja, zgornja_meja = barva_koze  
    # Ustvarimo binarno masko ce pade znotraj meje je 1, ce ne pade je 0
    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    # Preštejemo število pikslov ki imajo vrednost 1 (belo)
    stevilo_pikslov = cv.countNonZero(maska)
    return stevilo_pikslov

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    # Izrezemo podsliko iz obmocja koze od levo_zgoraj do desno_spodaj
    podslika = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]

    # Izracunamo povprecno barvo koze iz matrike podslike 
    povprecna_barva = np.mean(podslika, axis=(0, 1)).astype(int)

    # Izracunamo standardni odklon barve koze iz matrike podslike
    std_odklon = np.std(podslika, axis=(0, 1)).astype(int)

    # Izracunamo toleranco barve koze ce pade pod mejo 10 jo postavimo na 10, ce preseze 30 jo postavimo na 30
    toleranca = np.clip(std_odklon * 0.8, 10, 30)

    # Izracunamo spodnjo in zgornjo mejo ce pade pod 0 jo postavimo na 0, ce preseze 255 jo postavimo na 255
    spodnja_meja = np.clip(povprecna_barva - toleranca, 0, 255).astype(np.uint8)
    zgornja_meja = np.clip(povprecna_barva + toleranca, 0, 255).astype(np.uint8)
    
    return spodnja_meja, zgornja_meja

def najdi_obraz(skatle, sirina_skatle, visina_skatle, prag=20): 

    # Dimenzije matrike skatle
    visina_matrike = len(skatle)
    sirina_matrike = len(skatle[0])

    # Ustvarimo binarno masko (1 = koža, 0 = ni kože)
    maska = np.zeros((visina_matrike, sirina_matrike), dtype=np.uint8)

    # Označimo tiste škatle, ki imajo dovolj pikslov kože
    for i in range(visina_matrike):
        for j in range(sirina_matrike):
            if skatle[i][j] > prag:
                maska[i, j] = 1

    max_obmocje = []     # seznam največje najdene komponente
    obiskane = set()     # da ne gremo večkrat v isto skatlo 

    # Notranja funkcija flood_fill
    def flood_fill(y, x, trenutna_komponenta):
        # Če smo že obiskali točko ali ni koža, se vrnemo
        if (y, x) in obiskane or maska[y, x] == 0:
            return

        # Označimo točko kot obiskano in jo dodamo trenutni komponenti
        obiskane.add((y, x))
        trenutna_komponenta.append((y, x))

        # Preverimo sosednje točke (gor, dol, levo, desno)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < visina_matrike and 0 <= nx < sirina_matrike:
                flood_fill(ny, nx, trenutna_komponenta)

    # Poiščemo največjo povezano skupino
    for i in range(visina_matrike):
        for j in range(sirina_matrike):
            if maska[i, j] == 1 and (i, j) not in obiskane:
                trenutna_komponenta = []
                flood_fill(i, j, trenutna_komponenta)

                # Če je ta komponenta večja, jo shranimo
                if len(trenutna_komponenta) > len(max_obmocje):
                    max_obmocje = trenutna_komponenta

    # Če nismo našli nobene povezane komponente kože, ni obraza
    if not max_obmocje:
        return None

    # Izračunamo bounding box (okvir) največjega območja
    y_min = min(y for (y, x) in max_obmocje) * visina_skatle
    x_min = min(x for (y, x) in max_obmocje) * sirina_skatle
    y_max = (max(y for (y, x) in max_obmocje) + 1) * visina_skatle
    x_max = (max(x for (y, x) in max_obmocje) + 1) * sirina_skatle

    return (x_min, y_min, x_max, y_max)

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
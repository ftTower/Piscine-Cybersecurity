```markdown
# Arachnida - Cybersecurity Piscine

## Résumé

**Arachnida** est un projet d'introduction à la collecte automatisée de données web (web scraping) et à l'analyse de métadonnées.  
Le projet est composé de deux programmes :

- `spider.py` : un outil pour extraire récursivement les images d'un site web.
- `scorpion.py` : un outil pour analyser et afficher les métadonnées (notamment EXIF) des images.

---

## Contenu du projet

- `spider.py` : Télécharge des images à partir d'une URL, avec options de récursion et de profondeur.
- `scorpion.py` : Analyse les images passées en argument et affiche leurs métadonnées EXIF et autres.
- `Makefile` : Automatise le lancement des programmes, la gestion des fichiers, et le nettoyage.

---

## Utilisation

### spider.py

```bash
./spider.py [-r] [-l N] [-p PATH] URL
```

- `-r` : active la récursion pour explorer les pages liées.
- `-l N` : profondeur maximale de récursion (par défaut 5).
- `-p PATH` : chemin où seront enregistrées les images (par défaut `./data/`).
- `URL` : adresse du site à scraper.

Le programme télécharge par défaut les images aux extensions `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`.

---

### scorpion.py

```bash
./scorpion.py FILE1 [FILE2 ...]
```

Analyse les fichiers images donnés en argument et affiche leurs métadonnées EXIF et informations complémentaires.

---

## Makefile - Commandes utiles

- `make run`  
  Lance `spider.py` en mode récursif (-r) avec une profondeur limitée à 2 (-l 2) pour toutes les URLs listées dans le fichier `scrapSite.txt`.

- `make metadata`  
  Parcourt tous les fichiers `.jpg` et `.png` dans le dossier `data` et lance `scorpion.py` pour afficher leurs métadonnées.

- `make clean`  
  Supprime le dossier `data` où sont stockées les images téléchargées.

- `make all`  
  Nettoie, lance le scraping pour toutes les URLs, affiche les métadonnées, puis nettoie à nouveau.

- `make re`  
  Nettoie, lance le scraping et affiche les métadonnées.

---

## Exemple d'utilisation

1. Ajouter les URLs à scraper dans `scrapSite.txt`, une URL par ligne.  
2. Lancer :

```bash
make run
```

3. Analyser les métadonnées des images téléchargées :

```bash
make metadata
```

4. Nettoyer les fichiers téléchargés :

```bash
make clean
```

---

## Prérequis

- Python 3  
- Librairies Python : `requests`, `beautifulsoup4`, `Pillow`  
- Accès internet pour le scraping

---

## Notes

- Le code ne doit pas utiliser d'outils externes comme `wget` ou `scrapy`.  
- Le scraping est limité au même domaine que l'URL de départ.  
- Les métadonnées EXIF peuvent contenir des informations sensibles, soyez vigilant lors de leur manipulation.

```
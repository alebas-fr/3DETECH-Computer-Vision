# Process de Build 

Avant de commencer il faut installé python (https://www.python.org)
Une fois python installé il faut installer plusieurs librairies python nécessaire :
- numpy
- PyQt5

Pour cela dans un terminal il suffit de lancer la commande suivante "python3 -m pip install numpy PyQt5", ou "pip3 install numpy PyQt5" ou bien encore "py -m pip install numpy PyQt5" les 3 commandes font la même chose mais selon les OS (Windows, Mac ou Linux) certaines peuvent ne pas fonctionner.

Une fois python et les librairies nécessaires installé il faut récupéré les fichiers de code (si ce n'est pas déja fait) ils sont disponibles à l'adresse GitHub suivante :  https://github.com/alebas-fr/3DETECH-Computer-Vision/tree/main/TP%20Gesture%20Recognition. 
Une fois les codes téléchargés il suffit d'ouvrir le dossier ou est stocké les fichiers de code dans un terminal et de lancer le programme avec la commande python3 (ou py) MainWindow.py est le programme démarre. Pour le fermer on peut soit faire un ctrl+C dans le terminal, fermé le terminal ou de manière classique appuyez sur le bouton quitter en haut à droite de la fenêtre. 

# Ce qui a été réalisé 

Pour ce TP j'ai réalisé la partie 1 qui consistait à mettre en place le squelette de l'application (déja fourni mais il fallait installer les bibliothèques pythons pour pouvoir lancer le code) ensuite j'ai créé la galerie de templates et ajouter des templates dedans. Il y a 16 templates dedans pour 16 symboles à reconnaitre un seul template nous permet d'avoir un système plus réactif et qu'un seul échantillon suffit.

Pour la partie 2 j'ai réalisé toutes les étapes (code a complété) pour implémenter 1$ c'est-à-dire faire le ré-échantillonage, la rotation basé sur l'angle indicatif, la mise à l'échelle et la translation et pour finir la reconnaissance.

Après ces deux premières parties notre 1$ recognizer est implémenté mais le résultat est envoyé et affiché dans la console.

La partie 3 concernant le feeback donné à l'utilisateur comme affiché pour le geste reconnu le modèle que nous possédons en template. Ou même corrigé le geste effectué par l'utilisateur pour correspondre parfaitement à celui que nous avons en template. Elle n'a pas été implementé.

# Remarques
Le 1$ Recognizer est rapide et simple à realiser pour reconnaitre des formes simples mais possède plusieurs défauts : 
- Il n'est pas capable de reconnaitre le sens pour certains objets ou cela peut-être important (flèches par exemple)
- Pour certaines formes il confond avec des formes trés proches 
- Sur d'autres forme il est incapable de reconnaitre la forme en fonction d'où nous commençons à tracer (par exemple le triangle si on part du sommet et que nous partons vers la droite le triangle ne sera pas reconnu et sera confondu avec d'autres forme comme le caret si nous partons vers la gauche le triangle sera reconnu sans soucis)

Je pense que pour résoudre certains problèmes on pourrait essayer de prendre plusieurs templates pour chaque forme à reconnaitre mais cela ferait perdre en réactivité notre 1$ recognizer. Si nous avons plus de données le $1 recognizer va gagner en taux de reconnaissance mais va perdre en réactivité c'est donc un compromis à trouver entre la performance de la reconnaissance

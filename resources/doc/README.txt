Les fichiers de ce répertoire permettent de générer les tables de connectivité pour la documentation embarquée.

Voici un exemple pour le format ASTER :

1. Utiliser le script printnodalconnectivity.py pour générer la connectivité des mailles à partir de la classe dédiée.
Exemple : python printnodalconnectivity.py ASTER

2. Créer le fichier config_aster.tex contenant l'affichage généré par le script précédent.

3. Créer le fichier aster_connectivity.tex avec la liste des mailles à afficher.

4. Ajouter le bloc 'aster' dans le fichier Makefile.

5. Générer la table avec la commande : 'make aster'

6. Copier la table dans la documentation, puis utiliser 'make reset' pour nettoyer le répertoire.

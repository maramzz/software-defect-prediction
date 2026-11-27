Prédiction des défauts logiciels — NASA JM1
1. Présentation du projet
Ce projet consiste à développer un système de prédiction des défauts logiciels à l'aide du Machine Learning.
L'objectif est de prédire si un module logiciel contient au moins un défaut (true) ou s'il est non défectueux (false), à partir de ses caractéristiques numériques.
Le projet utilise le dataset NASA/PROMISE JM1 et compare plusieurs modèles de classification avant d'intégrer le modèle retenu dans une application web développée avec Streamlit.
Objectif
Aider à identifier les modules logiciels susceptibles de contenir des défauts afin de faciliter les activités de test et de maintenance.
2. Données et préparation
Source des données
•	Dataset : NASA/PROMISE JM1
•	Source : OpenML
•	Nombre initial d'observations : 10 885
•	Nombre initial d'attributs : 22
•	Variable cible : defects
•	Type de problème : classification binaire
Description des variables
Le dataset contient 21 variables numériques décrivant les caractéristiques des modules logiciels, notamment :
•	Mesures de complexité de McCabe.
•	Mesures de Halstead.
•	Nombre de lignes de code.
•	Nombre d'opérateurs et d'opérandes.
•	Nombre de branches.
La variable cible defects indique si le module est défectueux (true) ou non (false).
Exploration et qualité des données
L'exploration initiale a permis d'identifier :
•	5 lignes contenant des valeurs manquantes.
•	1 973 lignes dupliquées.
•	88 groupes de caractéristiques identiques associés à des labels contradictoires.
•	Un déséquilibre entre les deux classes.
•	Des valeurs extrêmes détectées lors de l'analyse.
Les doublons exacts ont été supprimés, ce qui a ramené le dataset à 8 912 observations.
Les groupes présentant des caractéristiques identiques mais des labels différents ont été conservés et signalés comme une limite de qualité des données. Les valeurs extrêmes ont également été conservées.
Prétraitement
Les étapes suivantes ont été appliquées :
1.	Séparation des variables explicatives X et de la cible y.
2.	Division stratifiée en données d'entraînement (80 %) et de test (20 %).
3.	Utilisation de random_state=42 pour assurer la reproductibilité.
4.	Remplacement des valeurs manquantes par la médiane avec SimpleImputer.
5.	Standardisation des variables avec StandardScaler.
Le prétraitement est intégré dans un Pipeline afin d'éviter les fuites de données : les transformations sont ajustées uniquement sur les données d'entraînement.
3. Modélisation et résultats
Modèles utilisés
Trois approches ont été comparées :
•	DummyClassifier : modèle de référence qui prédit systématiquement la classe majoritaire.
•	Régression logistique : modèle de classification linéaire avec pondération des classes (class_weight="balanced").
•	Random Forest : modèle basé sur plusieurs arbres de décision, également avec pondération des classes.
Les modèles ont été évalués sur le même jeu de test, avec les mêmes métriques.
Résultats obtenus
Modèle	Accuracy	Precision	Recall	F1-score
Référence naïve	0.775	0.000	0.000	0.000
Régression logistique	0.714	0.392	0.485	0.433
Random Forest	0.776	0.507	0.174	0.259
Choix du modèle final
La régression logistique a été retenue comme modèle final.
Même si Random Forest présente une meilleure accuracy et une meilleure précision, la régression logistique obtient un meilleur rappel et un meilleur F1-score.
Dans notre contexte, détecter les modules défectueux est prioritaire. Les faux négatifs représentent donc un risque important.
La régression logistique constitue ainsi le meilleur compromis parmi les modèles évalués selon notre objectif.
Analyse des erreurs
Sur le jeu de test, la régression logistique a produit :
•	303 faux positifs.
•	207 faux négatifs.
Les faux positifs correspondent aux modules non défectueux classés comme défectueux. Les faux négatifs correspondent aux modules défectueux classés comme non défectueux.
Ces derniers sont particulièrement importants car ils représentent des défauts qui n'ont pas été détectés par le modèle.
4. Application et utilisation
Une application interactive a été développée avec Streamlit.
Elle permet à l'utilisateur de :
•	Saisir les 21 caractéristiques d'un module logiciel.
•	Charger automatiquement un exemple réel non défectueux.
•	Charger automatiquement un exemple réel défectueux.
•	Obtenir une prédiction.
•	Consulter la probabilité estimée d'appartenir à la classe défectueuse.
•	Comparer les prédictions aux classes réelles des deux exemples de démonstration.
Le modèle final est sauvegardé dans model.joblib à l'aide de Joblib. Le fichier contient le Pipeline complet, y compris les étapes de prétraitement.
Installation
Prérequis : Python 3.13 et les bibliothèques indiquées dans requirements.txt.
pip install -r requirements.txt
streamlit run app.py
Compatibilité : le modèle a été sauvegardé avec Scikit-learn 1.6.1. Il est recommandé d'utiliser cette même version pour charger le fichier model.joblib.
5. Limites et perspectives
Limites
•	Le dataset présente un déséquilibre entre les classes.
•	Des groupes de caractéristiques identiques possèdent des labels contradictoires.
•	Le rappel de la régression logistique reste limité à 0.485.
•	Le modèle produit encore des faux négatifs.
•	Les probabilités estimées ne représentent pas une certitude sur la présence de défauts.
•	Les prédictions dépendent uniquement des métriques numériques fournies et ne remplacent pas les tests logiciels.
Perspectives d'amélioration
•	Tester d'autres modèles de classification.
•	Étudier différentes stratégies de gestion du déséquilibre des classes.
•	Étudier l'ajustement du seuil de décision selon le coût des erreurs.
•	Améliorer l'interprétabilité des prédictions.
•	Tester le modèle sur d'autres datasets de défauts logiciels.

________________________________________
Technologies utilisées : Python, Pandas, Scikit-learn, Joblib, Streamlit et Google Colab.





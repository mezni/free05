Pour modifier les informations de la page titre ainsi que celle des en-têtes et des pieds de page, utiliser le menu « Livrable », il est prévu à cet effet. Référez-vous au [Guide d’utilisation des gabarits](http:/intranet/Soutien-fonctionnement/Ressources-informationnelle/Processus-outils-projets-RI/ReferentielRessourcesInformationnelles/DocumentsRRI/Livrables/UtilisationDesGabarits.pdf) pour plus d’explications.

Référez-vous au [Guide de certification des biens livrables](http:/intranet/Soutien-fonctionnement/Ressources-informationnelle/Processus-outils-projets-RI/ReferentielRessourcesInformationnelles/DocumentsRRI/Livrables/Gabarits/RèglesCertification.docm) pour connaître les objets de certification de ce bien livrable.

Numéro du projet : P2882-ASPVHN

Titre du projet : Analyse des ponts pour les véhicules

Responsable : Louise Garceau

Document en rédaction

Version

Date de dernière mise à jour :

Historique du bien livrable

Lors de la mise à jour d’un document, veuillez activer le « Suivi des modifications » (menu « Révision »).

Dans le tableau ci-dessous, indiquer la version du document déposé, la date, et dans les commentaires, indiquer les sections modifiées et la nature de la modification apportée.

Ceci permet aux certificateurs, validateurs et approbateurs de cibler rapidement les éléments modifiés et accélère les processus de certification, validation et approbation.

| Version no   | Date       | Commentaires                                                                                                       | Intervenants   |
|--------------|------------|--------------------------------------------------------------------------------------------------------------------|----------------|
| V00.30       | 2023-01-13 | En réalisation                                                                                                     | Louise Garceau |
|              |            |                                                                                                                    |                |
| V00.80       | 2023-04-27 | Intégration des commentaires des pilotes                                                                           | Louise Garceau |
|              |            |                                                                                                                    |                |
| V01.00       | 2023-11-06 | Intégrer les commentaires de la 2  e  validation                                                                   | Louise Garceau |
|              |            |                                                                                                                    |                |
| V01.1        | 2024-04-23 | Ajout d’une spécification pour la production du rapport d’expertise + Correction lors d’écriture des users stories | Louise Garceau |
| V01.3        | 2025-10-31 | Mise à jour des unités de traitement pour le projet ASPVHN                                                         | Quentin Kayila |
|              |            |                                                                                                                    |                |

Table des matières

1 Axe Traitements	8

1.1 «Sous-système information» APV1 Analyse structurale des ponts pour les permis	8

1.1.1 «Fonction» APV11 Gestion des demandes d'expertise	9

1.1.1.1 «Unité de tâche»  APV111  Rechercher une demande d'expertise	12

1.1.1.1.1 Diagramme APV111 Rechercher une demande d'expertise - Scénario	13

1.1.1.1.2 Diagramme APV111  Rechercher une demande d'expertise-Contexte	14

1.1.1.2 «Unité de tâche»  APV112 Gérer une demande d'expertise	16

1.1.1.2.1 Diagramme APV112 Gérer une demande d'expertise - contexte	20

1.1.1.2.2 Diagramme APV112 Gérer une demande d'expertise - Scénario	20

1.1.1.3 «Unité de tâche»  APV113 Gérer un parcours sur une carte géographique	21

1.1.1.3.1 Diagramme APV113 Gérer un parcours sur une carte géographique - contexte	23

1.1.1.3.2 Diagramme APV113 Gérer un parcours sur une carte géographique - Scénario	24

1.1.1.4 «Unité de tâche»  APV114 Joindre des documents/courriels/lettres à la demande d'expertise	25

1.1.1.4.1 Diagramme APV114 Joindre des documents/courriels/lettres à la demande d'expertise - contexte	27

1.1.1.4.2 Diagramme APV114 Joindre des documents/courriels/lettres à la demande d'expertise - Scénario	27

1.1.1.5 «Unité de tâche»  APV115 Consulter les demandes d'expertise similaires	28

1.1.1.5.1 Diagramme APV115 Consulter les demandes d'expertise similaires	30

1.1.1.5.2 Diagramme APV115 Consulter les demandes d'expertise similaires - Scénario	30

1.1.1.6 «Service fonctionnel»  APV118 Gérer les documents/courriels/lettres dans la GID	31

1.1.1.6.1 Diagramme APV118 Gérer les documents/courriels/lettres dans la GID	32

1.1.1.7 «Unité de tâche»  APV119 Gérer les scénarios	33

1.1.1.7.1 Diagramme APV119 Gérer les scénarios - contexte	35

1.1.1.7.2 Diagramme APV119 Gérer les scénarios - Scénarios	36

1.1.2 «Fonction» APV12 Analyse des demandes	36

1.1.2.1.1 «Unité de tâche»  APV121 Consulter les structures et leurs résultats d'analyse 	38

1.1.2.1.2 Diagramme APV121 Consulter les structures et leurs résultats d'analyse - contexte	41

1.1.2.1.3 Diagramme APV121 Consulter les structures et leurs résultats d'analyse - Scénario	41

1.1.2.2 «Étape de tâche réutilisable»  APV122 Consulter le détail des hauteurs libres d'une structure	42

1.1.2.2.1 Diagramme APV122 Consulter le détail des hauteurs libres d'une structure - contexte	44

1.1.2.2.2 Diagramme APV122 Consulter le détail des hauteurs libres d'une structure - scénario	45

1.1.2.3 «Unité de tâche»  APV123 Consulter le détail des résultats d'analyse d'une structure	45

1.1.2.3.1 Diagramme APV123 Consulter le détail des résultats d'analyse d'une structure - contexte	47

1.1.2.3.2 Diagramme APV123 Consulter le détail des résultats d'analyse d'une structure - scénario	47

1.1.2.4 «Unité de tâche»  APV124 Consulter les entraves du parcours 	48

1.1.2.4.1 Diagramme APV124 Consulter les entraves du parcours	49

1.1.2.4.2 Diagramme APV124 Consulter les entraves du parcours-Contexte	50

1.1.2.5 «Unité de tâche»  APV125 Consulter les résultats d'évaluation d'une structure	51

1.1.2.5.1 Diagramme APV125 Consulter les résultats d'évaluation d'une structure	52

1.1.2.6 «Unité de tâche»  APV126 Gérer les éléments d’un parcours	53

1.1.2.6.1 Diagramme APV126 Gérer les éléments de parcours - Scénario	55

1.1.2.7 «Service fonctionnel»  APV128 Produire une analyse structurale des ponts	55

1.1.2.7.1 Diagramme APV128 Produire une analyse structurale des ponts	57

1.1.2.8 «Service fonctionnel»  APV128A - Générer les conditions de circulation par défaut	58

1.1.2.9 «Service fonctionnel»  APV128B Générer les conditions de circulation d’une restriction	59

1.1.2.10 «Service fonctionnel»  APV128C Générer les conditions de circulation d’un résultat d’évaluation	61

1.1.3 «Fonction» APV13 Production du rapport d'expertise/courriels/lettres	63

1.1.3.1 «Unité de tâche»  APV131 Rechercher un rapportd'expertise	67

1.1.3.1.1 Diagramme APV131 Rechercher les rapports d'expertise	68

1.1.3.2 «Unité de tâche»  APV132 Gérer le rapport d'expertise	68

1.1.3.2.1 Diagramme APV132 Gérer le rapport d'expertise - Contexte	70

1.1.3.2.2 Diagramme APV132 Gérer le rapport d'expertise-Scénario	71

1.1.3.3 «Service fonctionnel»  APV133 Produire le rapport d'expertise sans parcours	72

1.1.3.4 «Unité de tâche»  APV134 Gérer les courriels	73

1.1.3.4.1 Diagramme APV134 Gérer les courriels	75

1.1.3.5 «Unité de tâche»  APV135 Produire le bilan des analyses	75

1.1.3.6 «Service fonctionnel»  APV136 Signer un document	76

1.1.3.6.1 Diagramme APV136 Signer un document	77

1.1.3.7 «Service fonctionnel»  APV137 Produire les lettres	78

1.1.3.8 «Service fonctionnel»  APV138 Produire les courriels	79

1.1.3.9 «Unité de tâche»  APV139 Gérer les lettres	79

1.1.3.9.1 Diagramme APV139 Gérer les lettres	81

1.1.3.10 «Service fonctionnel»  APV13A Produire le rapport d'expertise avec parcours	81

1.1.4 «Fonction» APV14 Gestion technique des structures	83

1.1.4.1 «Unité de tâche»  APV141 Rechercher les structures	85

1.1.4.1.1 Diagramme APV141 Rechercher les structures - Contexte	86

1.1.4.1.2 Diagramme APV141 Rechercher les structures	87

1.1.4.2 «Unité de tâche»  APV142 Gérer les structures	88

1.1.4.2.1 Diagramme APV142 Gérer les structures - Contexte	90

1.1.4.2.2 Diagramme APV142 Gérer les structures - scénario	90

1.1.4.3 «Unité de tâche»  APV143 Gérer les restrictions	91

1.1.4.3.1 Diagramme APV143 Gérer les restrictions	94

1.1.4.4 «Unité de tâche»  APV144 Gérer les évaluations	95

1.1.4.4.1 Diagramme APV144 Gérer les évaluations - contexte	97

1.1.4.4.2 Diagramme APV144 Gérer les évaluations - Scénario	98

1.1.4.5 «Unité de tâche»  APV145 Consulter l'état des structures (inspections)	99

1.1.4.5.1 Diagramme APV145 Gérer l'état des structures (inspections) - Contexte	101

1.1.4.5.2 Diagramme APV145 Gérer l'état des structures (inspections) - Scénario	101

1.1.4.6 «Unité de tâche»  APV146 Gérer les repères	102

1.1.4.6.1 Diagramme APV146 Gérer les repères	103

1.1.4.7 «Service fonctionnel» APV147 Obtenir les événements des structures de GSQ	104

1.1.4.7.1 Diagramme APV147 Obtenir les modifications des structures de GSQ	106

1.1.4.8 «Unité de tâche»  APV148 Rechercher et consulter les hauteurs libres	107

1.1.4.8.1 Diagramme APV148 Rechercher et consulter les hauteurs libres	108

1.1.4.9 «Service fonctionnel»  APV14A Synchroniser les modifications des restrictions de GSQ	109

1.1.4.9.1 Diagramme APV14A Synchroniser les modifications des restrictions de GSQ	110

1.1.4.10 «Service fonctionnel»  APV14B Synchroniser les modifications des évaluations de GSQ	110

1.1.4.10.1 Diagramme APV14B Synchroniser les modifications des évaluations de GSQ	111

1.1.4.11 «Service fonctionnel»  APV14C Synchroniser les modifications des inspection de GSQ	111

1.1.4.11.1 Diagramme APV14C Synchroniser les modifications des inspections de GSQ	113

1.1.4.12 «Service fonctionnel»  APV14D Assigner les tableaux de seuils aux structures	113

1.1.4.13 «Service fonctionnel»  APV14E Attribuer une travée à une structure	114

1.1.4.14 «Service fonctionnel»  APV14F Gérer les normes d’évaluation et les charges de conception	115

1.1.5 «Fonction» APV15 Gestion du pilotage et de l'administration du système	116

1.1.5.1 «Unité de tâche»  APV151 Gérer les domaines de valeur	119

1.1.5.2 «Unité de tâche»  APV152 Gérer les paramètres du système	120

1.1.5.3 «Unité de tâche»  APV153 Gérer les gabarits de communication	121

1.1.5.4 «Unité de tâche»  APV154 Gérer les intervenants externes	122

1.1.5.5 «Unité de tâche»  APV155 Gérer les conditions de circulation	123

1.1.5.6 «Étape de tâche réutilisable»  APV156 Afficher le menu du système	124

1.1.5.7 «Unité de tâche»  APV157 Gérer les véhicules types et de référence	125

1.1.5.7.1 Diagramme APV157 Gérer les véhicules types et de référence	127

1.1.5.8 «Unité de tâche»  APV158 Gérer les seuils	127

1.1.5.9 «Unité de tâche»  APV159 Gérer les types d’événements des structures à notifier	129

1.1.5.10 «Unité de tâche»  APV15A Gérer les facteurs liés à la vitesse et au groupe de structure	130

1.1.5.11 «Unité de tâche»  APV15B Gérer les étendues de travées	132

1.1.5.12 «Service fonctionnel»  APV15C Journaliser les actions (Qui, quoi, quand)	133

1.1.6 «Fonction» APV16 Gestion de la messagerie interne	134

1.1.6.1 «Unité de tâche»  APV161 Rechercher et consulter les notifications	135

1.1.6.1.1 Diagramme APV161 Rechercher et consulter les notifications	136

1.1.6.2 «Service fonctionnel»  APV162 Produire et envoyer une notification pour une demande	137

1.1.6.3 «Service fonctionnel»  APV163 Produire et envoyer une notification pour une structure	138

1.1.6.3.1 Diagramme APV163 Produire et envoyer une notification pour une structure	140

Avant-propos

Cette partie est facultative. Si elle n’est pas utilisée, il est recommandé de supprimer cette page du gabarit.

Informations pertinentes sur la réalisation du bien livrable :

- Introduction au bien livrable : présentation générale de son contenu.
- Particularités du bien livrable : rubriques ajoutées ou enlevées et raisons de ces changements, difficultés particulières, explications pertinentes pour comprendre une rubrique ou un autre aspect du bien livrable, etc.
- Identification des participants aux activités qui ont permis l’élaboration du bien livrable.
- Description des activités qui ont permis l’élaboration du bien livrable (contexte, ateliers de travail, rencontres formelles, etc.)
- Références particulières (s’il y a lieu).

Notez que les éléments non documentés (dont le champ Notes est vide) et les éléments dont le nom est vide ne sont pas inclus lors de la génération du bien livrable par Enterprise Architect. Ceci est une configuration spécifique du gabarit "MTQ - Bien livrable générique". Cependant, ces options peuvent être changées au moment de lancer la génération du rapport en choisissant les options voulues dans l'onglet "Advanced" de la fenêtre de dialogue "Generate Documentation".Pré-requis : P251U APV – Processus de système

Ce document présente les fonctions du système APV.

**Note**

Il est entendu que les processus de sécurité, d’authentification aux différents groupes ou systèmes, ou encore les processus relatifs à l’utilisation d’autres systèmes du Ministère, sont documentés dans leur propre système.

Afin d’alléger le texte de ce document, veuillez noter que les utilisations suivantes peuvent y survenir :

- Le terme « Ministère » sera utilisé pour représenter le Ministère des Transports et de la Mobilité durable (MTMD);
- Expressions des acronymes utilisés :

| Acronyme   | Expression                                                |
|------------|-----------------------------------------------------------|
| BD         | Base de données                                           |
| APV        | Analyse des ponts pour les véhicules                      |
| UT         | Unité de tâche                                            |
| SAS        | Sécurité applicative des systèmes                         |
| SIGO       | Outil d’affichage et d’analyse sur une carte géographique |
| GSQ        | Gestion des structures                                    |
| TRR        | Travaux routiers                                          |
| BGR        | Base géographique routière                                |
| SIT        | Service information transport - Québec 511                |
| DLP        | Diffusion des limites de poids                            |
| DHL        | Diffusion des hauteurs libres                             |
| GID        | Gestion intégrée des documents (Content Server)           |
|            |                                                           |
| GPM        | Gestion des permis ministériels                           |
| ConsignO   | Application de signature numérique                        |
| GIA        | Gestion des identités et des accès                        |

Cette partie est facultative. Si elle n’est pas utilisée, il est recommandé de supprimer cette page du gabarit.

Informations pertinentes sur la réalisation du bien livrable :

- Introduction au bien livrable : présentation générale de son contenu.
- Particularités du bien livrable : rubriques ajoutées ou enlevées et raisons de ces changements, difficultés particulières, explications pertinentes pour comprendre une rubrique ou un autre aspect du bien livrable, etc.
- Identification des participants aux activités qui ont permis l’élaboration du bien livrable.
- Description des activités qui ont permis l’élaboration du bien livrable (contexte, ateliers de travail, rencontres formelles, etc.)
- Références particulières (s’il y a lieu).

Notez que les éléments non documentés (dont le champ Notes est vide) et les éléments dont le nom est vide ne sont pas inclus lors de la génération du bien livrable par Enterprise Architect. Ceci est une configuration spécifique du gabarit "MTQ - Bien livrable générique". Cependant, ces options peuvent être changées au moment de lancer la génération du rapport en choisissant les options voulues dans l'onglet "Advanced" de la fenêtre de dialogue "Generate Documentation".

Remarque : Ce bien livrable étant généré par le RAM (Référentiel applicatif ministériel), la structure de ce document ne peut pas être modifiée.

## 1 Axe Traitements

Diagramme SI\_APV Analyse structurale des ponts pour les permis

<!-- image -->

Nom du diagramme :  SI\_APV Analyse structurale des ponts pour les permis

Numéro de figure : 1

### 1.1 «Sous-système information» APV1 Analyse structurale des ponts pour les permis

Champs Notes du sous-système Z1.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV1 Analyse structurale des ponts pour les permis

<!-- image -->

Nom du diagramme :  APV1 Analyse structurale des ponts pour les permis

Numéro de figure : 2

#### 1.1.1 «Fonction» APV11 Gestion des demandes d'expertise

Cette fonction permet de traiter et consulter des demandes d'expertise.  Ces dernières proviennent en général du système GPM, mais peuvent aussi être saisie manuellement par les ingénieurs.  Sur réception des demandes provenant de GPM, plusieurs traitements sont faits automatiquement sur chaque demande, dont le calcul des efforts de flexion et de cisaillement, ainsi que les calculs des ratios et la comparaison du véhicule à l'étude avec les véhicules types.

Lorsqu’une demande est prise en charge par un ingénieur, la fonction permet à l'ingénieur de produire le parcours sur une carte géographique, d'exécuter les calculs, de gérer différents scénarios, de joindre des courriels et des documents à la demande.

Elle permet aussi à l'ingénieur de consulter les demandes d'expertises similaires.

| Critères de découpage   | Default: &lt;memo&gt;*  Description: Le ou les critères de découpage permettent de préciser sur quelles bases la fonction regroupe les unités de tâche. En général, ça devrait être en selon les entités à traiter.   |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Diagramme APV11 Gestion des demandes d'expertise

<!-- image -->

Nom du diagramme : «Fonction» APV11 Gestion des demandes d'expertise

Numéro de figure : 3

Diagramme APV11 Gestion des demandes d'expertise \_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV11 Gestion des demandes d'expertise \_Arrimage axe Processus

Numéro de figure : 4

Ce diagramme établit le lien entre les unités de tâche de cette fonction et les unités de travail prises en charge dans l'axe des processus.

##### 1.1.1.1 «Unité de tâche»  APV111  Rechercher une demande d'expertise

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

À l’affichage de la page, l’unité de tâche affiche toutes les demandes en cours qui sont assignées à l’utilisateur et toutes celles qui ne sont pas assignées. À ce moment, l’utilisateur peut raffiner sa recherche à l’aide de différents critères tels que numéro demande, transporteur, no structure, date de production de l'expertise, gestionnaires externes, masse totale en charge (MTC), nombres d’essieux, charges axiales, espacements, etc., dont notamment une recherche textuelle.

À partir du résultat de la recherche, l'ingénieur peut consulter, modifier, dupliquer ou supprimer une demande à l'aide des différents boutons affichés pour chaque demande.  Il peut aussi exporter le résultat de sa recherche dans un fichier Excel.

La duplication d'une demande consiste à copier la demande seulement.  Aucun résultat du calcul des efforts, ni de l'analyse structurale, ni du rapport d'expertise.  Elle est utilisée lorsque l'ingénieur veut créer une demande qui ne provient pas de GPM à partir d'une demande similaire.

L'unité de tâche permet aussi d'ajouter une demande manuellement.  Pour ce faire, l'UT doit appeler APV112 Gérer une demande d'expertise.

L’unité de tâche permet à l'ingénieur de prendre en charge une nouvelle demande d'expertise à réaliser ou encore de se dé-assigner une demande qu'il avait prise en charge ou encore de s'assigner une demande qui est assignée à un autre ingénieur, même si la demande est en traitement. Lorsque la demande est assignée, le statut de la demande devient « En cours ».  De même que si la demande n’est plus assignée à un ingénieur, le statut doit redevenir à « Non assignée ».

Dès qu'une demande est assignée ou ré-assignée, l'unité de tâche doit appeler le service fonctionnel "" pour envoyer les informations concernant la personne qui a pris en charge la demande, le statut de la demande et la date de prise en charge.

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

L’unité de tâche joue le rôle de page d’accueil, donc sera exécutée à chaque ouverture du système et également lorsque l’utilisateur aura besoin d’effectuer une recherche de dossier.

**Modalités d’accès :**

Cette unité de tâche est accessible à partir du menu "demande" .

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de trois secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Élevée

**Fréquence d’activation :**

Élevée, plusieurs fois par jour

**Volume traité :**

Environ 3000 demandes d'expertise sont traitées par année

**Préconditions :**

**SO**

**Postconditions :**

- Les résultats de la recherche sont affichés.

- À partir des résultats de recherche, l’utilisateur peut:

- consulter une demande
- modifier une demande
- supprimer une demande
- dupliquer une demande
- exporter le résultat de sa recherche dans un fichier Excel.

###### 1.1.1.1.1 Diagramme APV111 Rechercher une demande d'expertise - Scénario

<!-- image -->

Nom du diagramme :  APV111  Rechercher une demande d'expertise - Scénario

Numéro de figure : 5

###### 1.1.1.1.2 Diagramme APV111  Rechercher une demande d'expertise-Contexte

<!-- image -->

Nom du diagramme :  APV111  Rechercher une demande d'expertise-Contexte

Numéro de figure : 6

##### 1.1.1.2 «Unité de tâche»  APV112 Gérer une demande d'expertise

| Niveau complexité   | TC   |
|---------------------|------|

**Description :**

Cette unité de tâche permet de créer ou de modifier une demande d'expertise (dossier numérique).

Une demande d'expertise contient :

- La demande originale provenant de GPM (ou la demande saisie manuellement) + toutes les versions modifiées (historique);
- Les résultats pour les travées de 1m à 50m des efforts en flexion et cisaillement, les ratios, le nombre d'essieux critiques et le premier essieu critique pour chaque version de la demande;
- Toutes les structures du parcours et/ou les structures demandées pour l'analyse structurale;
- Tous les résultats d'analyse structurale (comprend les restrictions, évaluations, inspections), les résultats des hauteurs libres et les entraves retrouvées sur le parcours, de chaque version de la demande;
- Les rapports d’expertise produits par un ingénieur de la DGS, pour chaque version (s’il y a eu des modifications à la demande);
- Un lien vers la GID pour tous les documents/courriels qui ont été produits pour faire l’analyse de la demande;
- Un ou plusieurs scénarios pour chaque version.

L'utilisateur doit être en mesure de consulter plusieurs fenêtres d'informations d'une demande en même temps, par exemple, voir la demande, ainsi que les résultats d'analyse d'une structure.

**Demande**

Les demandes proviennent du système GPM.  Il existe 3 types de demandes: sans parcours, avec parcours ou Super-lourd.

Le service "APV Recevoir les demandes d'expertise de GPM" a déjà déterminé si une demande est sans parcours.  Si la demande est avec parcours, c'est l'ingénieur qui doit spécifier le type de la demande (avec parcours (DAP) ou super-lourd (DSL)).

Dès l'ouverture de la demande, les résultats des calculs des efforts et des ratios de flexion et de cisaillement sont affichés pour les longueurs de travées types, définies dans le tableau des seuils (ex: 10m, 20m, 30m, 40m et 50m), ainsi que les informations pertinentes de la demande provenant de GPM.

Les ratios sont ensuite comparés aux seuils établis par la DGS (équivalence aux charges légales et équivalence aux classes 5, correspondant au tableau 1 du fichier "Seuils\_limites(2019-12)").  Si un ratio est supérieur au seuil d'équivalence, alors l'UT doit avoir recours aux couleurs, afin de permettre une interprétation rapide de la sévérité de la configuration.

En tout temps, l'utilisateur peut refaire calculer les efforts de flexion et de cisaillement.  Pour ce faire, l'UT doit appeler le service externe "GPM\_3\_ Calculer les efforts de flexion et de cisaillement d'un véhicule et leurs ratios".

L'utilisateur doit pouvoir faire afficher les résultats de toutes les travées, soit de 1m à 50m, par incrément de 1 m, dans une fenêtre de type pop-up.  Dans ces résultats, l'utilisateur doit pouvoir consulter les résultats des flexions et cisaillement du véhicule à l'étude, ceux du véhicule de référence actif, les ratios (Mc véhicule à l'étude par rapport au Mc véhicule de référence actif et idem pour Vc) et les seuils de la classe 5 (table de pilotage pour la réglementation, non modifiable par le pilote).

De plus, l'utilisateur doit pouvoir faire afficher les résultats d'une travée spécifique autre que les travées types (Ex: 10m, 20m, 30m, 40m et 50m), à partir des travées de 1m à 50m.

**Demande manuelle**

L'utilisateur peut aussi créer une demande manuellement à partir d'une page vierge.  () types de demandes peuvent être saisies manuellement: sans parcours, avec parcours, super-lourd .  Une demande saisie manuellement doit avoir une numérotation différente de celle provenant de GPM et le numéro de version sera toujours 1.0.

Une fois enregistrée, la demande demeure modifiable.

Si une demande est créée sans parcours, le rapport d'expertise n'est jamais créé automatiquement. C'est l'ingénieur qui doit le créer à partir de l'UT APV132 Gérer le rapport d'expertise.

Dans le cas d'une demande de réglementation, l'ingénieur n'a pas à créer de rapport d'expertise.

**Demandes d'expertises similaires**

Afin de consulter la liste des demandes d'expertise similaires, l'UT doit appeler l'UT "APV115 Consulter les demandes d'expertises similaires".  À partir de cette UT, l'ingénieur peut consulter les demandes d'expertises similaires ou encore refaire une recherche avec des critères plus spécifiques.

**Parcours**

Pour une demande avec parcours ou pour un "super-lourd", l'utilisateur doit tracer le parcours en utilisant la carte géographique de l'outil SIGO.  Pour ce faire, l'UT doit appeler l'unité de tâche "APV113 Gérer un parcours sur une carte géographique" en lui passant en paramètre le numéro de la demande, le numéro de version et la hauteur du véhicule à analyser.

Pour chaque version de demande, un seul parcours est conservé.  Si l'ingénieur modifie le parcours sans modification de la demande, l'ancien parcours n'est pas conservé.  L'identifiant du parcours doit avoir le même no de version que celui de la demande.

**Consultation d'une demande**

Pour obtenir les informations des structures, des hauteurs libres, des entraves et du parcours associées à la demande, à partir de leurs identifiants, l'UT doit appeler leToutes les autres informations reliées à la demande, telle que la configuration du véhicule, les résultats d'analyse, les scénarios et les rapports d'expertise sont conservées dans APV.

**Historique d'une demande**

L'utilisateur peut consulter les anciennes versions de la demande qui correspondent aux différentes modifications qui ont été apportées dans GPM, et s'il y a lieu, consulter à partir de chaque version, le parcours sur la carte, les scénarios, les résultats des analyses et le rapport d'expertise.  Pour une version de demande, il existe un seul parcours, un ou plusieurs scénarios, un seul résultat d'analyse et un seul rapport d'expertise.

**Analyse structurale**

À partir de la demande avec parcours ou pour un "super-lourd", l'ingénieur peut en tout temps refaire l'analyse structurale. L’analyse s’effectue avec les charges axiales et les espacements du véhicule. Ainsi, la demande doit contenir la configuration du véhicule pour qu’une analyse puisse être exécutée.  Pour procéder à l'analyse structurale, l'UT doit appeler le service fonctionnel "APV128 Produire une analyse structurale des ponts".  Cependant, si l'ingénieur refait l'analyse structurale sans qu'il y ait eu de modification de la demande, l'ancienne analyse n'est pas conservée.  L'historique des analyses structurales est conservé seulement lorsqu'il y a eu une modification de la demande provenant de GPM, donc avec une nouvelle version de la demande.

S’il s’agit d’une demande manuelle, le système conserve seulement la dernière analyse.

**Résultats d'analyse**

À partir de la demande avec parcours ou pour un "super-lourd", l'utilisateur peut consulter les résultats d'analyse (détail des résultats d'analyse des structures, les résultats des évaluations et le détail des résultats des hauteurs libres) de toutes les structures impliquées dans l'analyse en passant par l'UT "APV121 Consulter les structures et leurs résultats d'analyse" et peut consulter les entraves sur le parcours en accédant à l'UT "APV124 Consulter les entraves du parcours".

**Scénarios**

À partir d'une version d'une demande, l'utilisateur peut créer un ou des scénarios.  Un scénario peut être nécessaire pour l'ingénieur afin de modifier les valeurs des charges axiales ou les espacements ou encore pour tracer un nouveau parcours.

Pour créer un scénario, l'UT doit accéder à l'UT "APV119 Gérer les scénarios".

Tous les scénarios avec les résultats d'analyse doivent être conservés en lien avec la demande.

La demande originale ne peut pas être modifiée.

**Impression d'une demande**

L'utilisateur doit pouvoir imprimer la demande sous forme de rapport PDF.  Il doit pouvoir sélectionner la sec ou les sections qu’il désire imprimer, soit la demande avec la configuration du véhicule, les calculs des efforts, les résultats des analyses de chaque structure, le rapport d’expertise, etc.

**Documents/courriels/lettres**

L'unité de tâche doit faire appel à l'UT "APV114 Joindre les documents/courriels/lettres à la demande d'expertise" pour permettre à l'utilisateur de joindre un document/courriel/lettre à la demande ou encore de consulter les documents déjà joints ou de supprimer un document.

L'unité de tâche doit faire appel à l'UT "APV134 Gérer les courriels " pour permettre à l'utilisateur de créer ou modifier un courriel qui est en lien avec la demande et de l'envoyer.

L'unité de tâche doit faire appel à l'UT "APV139 Gérer les lettres" pour permettre à l'utilisateur de modifier le contenu d'une lettre qui est en lien avec la demande.

**Rapport d'expertise**

L'unité de tâche doit faire appel à l'UT "APV132 Gérer le rapport d'expertise" pour permettre à l'utilisateur de modifier ce dernier avant de le signer et de l'envoyer à GPM ou encore, pour consulter les différentes versions

**Journalisation**

Tout changements aux demandes doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Complexe

**Paramètres :**

Numéro de la demande

**Circonstances d’utilisation :**

Un ingénieur doit procéder à l'analyse d'une demande d'expertise.

**Modalités d’accès :**

L'unité de tâche est accessible à partir de l'écran de recherche "APV111 Rechercher une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de trois secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance élevée.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Environ 3000 demandes d'expertise sont traitées par année

**Préconditions :**

Une demande d'expertise doit être sélectionnée

**Postconditions :**

- Une demande a été créée (par l’utilisateur ou par l’importation de GPM)

- Une demande a été modifiée (par GPM pour celles d’origine GPM ou par l’utilisateur pour celles créées par un utilisateur)

- Des scénarios ont été créés par l’utilisateur, si nécessaire

- Le ou les parcours ont été tracés, ou une sélection a été faite par l’utilisateur

- Les calculs des efforts ont été effectués, si la demande comporte une configuration avec des masses et les espacements d’essieux

- Les analyses structurales ont été effectuées pour une demande avec parcours ou avec une option de sélection de structures

- Des documents ont été joints à la demande

- Des courriels ont été envoyés, si nécessaire.

###### 1.1.1.2.1 Diagramme APV112 Gérer une demande d'expertise - contexte

<!-- image -->

Nom du diagramme :  APV112 Gérer une demande d'expertise - contexte

Numéro de figure : 7

###### 1.1.1.2.2 Diagramme APV112 Gérer une demande d'expertise - Scénario

<!-- image -->

Nom du diagramme :  APV112 Gérer une demande d'expertise - Scénario

Numéro de figure : 8

##### 1.1.1.3 «Unité de tâche»  APV113 Gérer un parcours sur une carte géographique

| Niveau complexité   | C   |
|---------------------|-----|

**Description :**

Elle permet de définir un parcours pour une demande avec parcours ou pour un "super-lourd" à partir de l'outil SIGO qui affiche une carte géographique interactive du Québec.

La carte doit être affichée dans une fenêtre de type "pop-up" afin que l'utilisateur puisse voir sa demande et la carte en même temps.

***Analyse du parcours***

Lorsque le parcours est affiché, saisi ou modifié, l'utilisateur doit procéder à l'analyse du parcours.

Lorsque l'analyse est terminée, l'outil affiche les résultats de l'analyse sur la carte géographique, tels que les structures et des indicateurs visuels selon les couches que l'utilisateur a sélectionnées.

L’analyse des hauteurs libres est effectuée à partir de cette carte puisque le tracé est en mesure de trouver quels points sont à vérifier et permet à l’ingénieur de facilement voir si le passage sous une structure est compromis par sa hauteur.

Dès que le parcours a été saisi et analysé sur la carte,doit appeler en lui passant en paramètres les résultats d'analyse du parcours, afin qu puisse les conserver.

Les résultats d'analyse sont:

- une liste chronologique des structures rencontrées et le passage soit en dessous, soit par-dessus la structure

- les municipalités où le parcours passe et pour lesquelles le transporteur devra obtenir un permis de circulation directement auprès d'elles

- les routes relevant de ces municipalités

- les traversiers qui sont utilisés

- les entraves sur le parcours

- les résultats d’analyse des hauteurs libres (identifiant du schéma, identifiant de passage, la direction et condition, si applicable), ainsi que si le véhicule doit passer par-dessus ou sous la structure

- le nombre de voies dans la même direction

**Mode d’automatisation :**

Interactif

**Complexité :**

**Paramètres d'entrée :**

Numéro de la demande d'expertise

**Paramètres de sortie :**

SO

**Circonstances d’utilisation :**

L'ingénieur doit tracer un parcours lors d'une demande d'expertise avec parcours ou pour une demande "Super-lourd"

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "APV112 Gérer une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance élevée.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Environ 2500 demandes avec parcours et super-lourd

**Préconditions :**

Une demande d'expertise a été sélectionnée

**Postconditions :**

Le parcours a été tracé

Toutes les couches sélectionnées sont affichées sur la carte géographique

Le détail de chaque élément affiché sur la carte peut être consulté

Les résultats d'analyse sont envoyés à APV.

###### 1.1.1.3.1 Diagramme APV113 Gérer un parcours sur une carte géographique - contexte

<!-- image -->

Nom du diagramme :  APV113 Gérer un parcours sur une carte géographique - contexte

Numéro de figure : 9

###### 1.1.1.3.2 Diagramme APV113 Gérer un parcours sur une carte géographique - Scénario

<!-- image -->

Nom du diagramme :  APV113 Gérer un parcours sur une carte géographique - Scénario

Numéro de figure : 10

##### 1.1.1.4 «Unité de tâche»  APV114 Joindre des documents/courriels/lettres à la demande d'expertise

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

Cette unité de tâche permet de consulter les documents/courriels/lettres d'une demande (pas seulement pour une version de la demande) et d'en joindre des nouveaux.  La technique "glisser et déposer" doit pouvoir être utilisée ou encore de sélectionner dans Explorer un document.  Chaque document/courriel/lettre joint est déposé dans la GID.

Un document/courriel/lettre déjà joint peut être retiré de la demande ou peut être remplacé.

Dès qu'un document/courriel/lettre est joint ou retiré à une demande, le service fonctionnel APV118 Gérer les documents officiels dans la GID est appelé.

**Journalisation**

Tout dépôt ou retrait de documents/courriels/lettres doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Lorsque l'utilisateur veut joindre des documents/courriels/lettres à une demande

**Modalités d’accès :**

Appelée par l'unité de tâche APV112 - Gérer une demande d'expertise ou à partir du menu

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de trois secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Moins de 10 documents/courriels/lettres par demande

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

L'utilisateur a joint, remplacé ou retiré des documents/courriels/lettres et ces derniers sont reliés à la demande dans la BD.

Les documents/courriels/lettres ont été consultés

###### 1.1.1.4.1 Diagramme APV114 Joindre des documents/courriels/lettres à la demande d'expertise - contexte

<!-- image -->

Nom du diagramme :  APV114 Joindre des documents/courriels/lettres à la demande d'expertise - contexte

Numéro de figure : 11

###### 1.1.1.4.2 Diagramme APV114 Joindre des documents/courriels/lettres à la demande d'expertise - Scénario

<!-- image -->

Nom du diagramme :  APV114 Joindre des documents/courriels/lettres à la demande d'expertise - Scénario

Numéro de figure : 12

##### 1.1.1.5 «Unité de tâche»  APV115 Consulter les demandes d'expertise similaires

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de rechercher et consulter les demandes d'expertise similaires à la demande à l'étude qui ont été obtenues lors de la réception de la demande.  Elle affiche la liste des numéros de demandes similaires et permet de consulter une demande à la fois.  La demande doit s'afficher dans une nouvelle fenêtre d'APV en utilisant l'UT "APV112 Gérer une demande d'expertise", afin de permettre de consulter toutes les informations de la demande similaire, y compris les résultats d'analyse et le rapport d'expertise et de pouvoir comparer avec la demande à l'étude.  Cependant, en aucun temps, il ne sera possible de modifier la demande similaire.

L'utilisateur doit pouvoir cliquer sur le bouton "Suivant" et "Précédent" pour consulter la prochaine ou la précédente demande similaire.

L'utilisateur peut exécuter la recherche à nouveau, en utilisant d'autres critères tels que le nom du transporteur, la période (autre que celle des paramètres du système), les numéros de structures et autres à définir.  Cependant, les critères de base (configuration, ville d'origine et ville de destination) ne sont pas modifiables.  Pour exécuter la recherche, l'UT doit appeler le APV11 Rechercher demande d'expertise.

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut consulter les demandes d'expertise similaires trouvées automatiquement par le système

L'ingénieur veut raffiner les critères de recherche des demandes d'expertise similaires et pouvoir les consulter.

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "APV112 Gérer une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de cinq secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Environ 3000 demandes d'expertise sont traitées par année, donc la recherche doit se faire parmi des milliers de demandes.

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

La liste des demandes similaires peut être consultée

Une recherche peut être exécutée avec de nouveaux critères.

###### 1.1.1.5.1 Diagramme APV115 Consulter les demandes d'expertise similaires

<!-- image -->

Nom du diagramme :  APV115 Consulter les demandes d'expertise similaires

Numéro de figure : 13

###### 1.1.1.5.2 Diagramme APV115 Consulter les demandes d'expertise similaires - Scénario

<!-- image -->

Nom du diagramme :  APV115 Consulter les demandes d'expertise similaires - Scénario

Numéro de figure : 14

##### 1.1.1.6 

##### 1.1.1.7 

|    |    |
|----|----|

##### 1.1.1.8 

##### 1.1.1.9 

##### 1.1.1.10 

##### 1.1.1.11 

##### 1.1.1.12 

##### 1.1.1.13 

##### 1.1.1.14 

##### 1.1.1.15 

##### 1.1.1.16 

##### 1.1.1.17 

##### 1.1.1.18 

##### 1.1.1.19 

##### 1.1.1.20 

##### 1.1.1.21 

##### 1.1.1.22 

##### 1.1.1.23 

##### 1.1.1.24 

##### 1.1.1.25 

##### 1.1.1.26 

##### 1.1.1.27 

##### 1.1.1.28 

##### 1.1.1.29 

##### 1.1.1.30 

##### 1.1.1.31 

##### 1.1.1.32 

##### 1.1.1.33 

##### 1.1.1.34 

##### 1.1.1.35 

|    |    |
|----|----|

###### 1.1.1.35.1 

<!-- image -->

##### 1.1.1.36 «Service fonctionnel»  APV118 Gérer les documents/courriels/lettres dans la GID

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Ce service fonctionnel permet d'appeler les services du système GID afin de déposer, modifier ou retirer les documents/courriels/lettres reliés à la demande.

Le service doit obtenir le nom du répertoire pour les demandes dans les paramètres de système et y ajouter le numéro de la demande, pour avoir le nom complet du répertoire où déposer les documents/courriels/lettres.  Si le répertoire n'a jamais été créé, il doit être créé et ensuite, le service doit ajouter le document/courriel/lettre.

Le service de la GID doit retourner les métadonnées du document/courriel/lettre, qui doivent être conservées dans la BD, afin de retrouver le document à partir de la demande.

**Complexité :**

Simple

**Paramètres :**

- Numéro de la demande

- La liste des documents/courriels/lettres à être déposés dans la GID, avec les métadonnées du document

- La liste des documents/courriels/lettres à être retirée de la GID, , avec les métadonnées du document.

**Conditions de réutilisation** *:*

Lorsqu'un document/courriel/lettre a été déposé, modifié ou retiré d'une demande.

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de trois secondes.

**Préconditions :**

**SO**

**Postconditions :**

Les métadonnées des documents/courriels/lettres sont enregistrées dans la BD.

###### 1.1.1.36.1 Diagramme APV118 Gérer les documents/courriels/lettres dans la GID

<!-- image -->

Nom du diagramme :  APV118 Gérer les documents/courriels/lettres dans la GID

Numéro de figure : 16

##### 1.1.1.37 «Unité de tâche»  APV119 Gérer les scénarios

| Niveau complexité   | C   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de créer, modifier et supprimer un scénario.  Pour créer un scénario, l'UT copie toutes les informations de la demande originale ainsi que le parcours dans le cas d'une demande avec parcours, en excluant tous les résultats d'analyse.  Chaque scénario est identifié par une lettre, le premier commençant par A, le deuxième par B, etc.  À ce moment, l'ingénieur peut modifier les informations de la demande ou le parcours et déclencher le calcul des efforts de flexion et de cisaillement et l'analyse structurale des ponts.

Pour être en mesure de modifier le parcours, l'UT doit appeler l'UT "APV113 - Gérer un parcours sur une carte géographique"

Si dans le scénario, le parcours a été modifié, et que c'est ce scénario qui a été retenu, l’ingénieur devra refaire la modification du parcours dans la demande.  Le parcours modifié ne sera pas copié automatiquement.

Pour effectuer les calculs, l'UT doit faire appel aux UTs et services suivants:

- GPM\_3\_Calculer les efforts de flexion et de cisaillement d'un véhicule et leurs ratios

- APV128 Produire une analyse structurale des ponts

Les résultats du calcul des efforts et cisaillement sont affichés automatiquement dans l'interface du scénario.  Pour consulter les résultats d'analyse structurale, l'UT doit appeler l'UT "APV121 Consulter les résultats d'analyse", pour consulter les entraves, l'UT doit appeler l'UT "APV124 Consulter les entraves du parcours" et pour consulter le rapport d'expertise, l'UT doit appeler l'UT "APV132 Gérer le rapport d'expertise".

Tous les scénarios et leurs résultats d'analyse doivent être conservés et peuvent être consultés.  Ils sont reliés à la demande.  L'identifiant de l'historique doit être en lien avec le même no de version que celui de la demande.   Si un scénario est modifié, l'historique des modifications et des analyses n'est pas conservée.  Si l'ingénieur veut le conserver, il doit créer un nouveau scénario.

Le rapport d'expertise doit toujours être produit et conservé avec le scénario de la demande.

**Conservation des données d'un scénario**

Seuls les identifiants des structures, des hauteurs libres et des entraves sont conservés dans APV.  Pour obtenir les informations associées.

**Mode d’automatisation :**

Interactif

**Complexité :**

Complexe

**Paramètres :**

SO

**Circonstances d’utilisation :**

Lorsque l'ingénieur veut créer différents scénarios lors de l'analyse de la demande

**Modalités d’accès :**

Appelée par l'unité de tâche APV112 - Gérer une demande d'expertise

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 5 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Moyenne de 2 scénarios par demande

**Préconditions :**

**SO**

**Postconditions :**

Un scénario a été créé, modifié ou supprimé.

###### 1.1.1.37.1 Diagramme APV119 Gérer les scénarios - contexte

<!-- image -->

Nom du diagramme :  APV119 Gérer les scénarios - contexte

Numéro de figure : 17

###### 1.1.1.37.2 Diagramme APV119 Gérer les scénarios - Scénarios

<!-- image -->

Nom du diagramme :  APV119 Gérer les scénarios - Scénarios

Numéro de figure : 18

##### 1.1.1.38 

|    |    |
|----|----|

#### 1.1.2 «Fonction» APV12 Analyse des demandes

Cette fonction permet de procéder aux analyses structurales des ponts qui se situent sur le parcours.

Par la suite, elle permet à l'ingénieur de consulter les résultats des analyses, les hauteurs libres et les entraves.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV12 Analyse des demandes

<!-- image -->

Nom du diagramme :  APV12 Analyse des demandes

Numéro de figure : 19

Diagramme APV12 Analyse des demandes \_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV12 Analyse des demandes \_Arrimage axe Processus

Numéro de figure : 20

##### 1.1.2.1 «Unité de tâche»  APV121 Consulter les résultats d'analyse

| Niveau complexité   |    |
|---------------------|----|

**Description :**

Cette unité de tâche permet d'afficher la liste des structures impliquées dans l'analyse de la demandees informationsl structure

L'utilisateur peut accéder pour chaque structure, à

- du détail des résultats d'analyse via l'UT "APV123 Consulter le détail des résultats d'analyse d'une structure"
- 'interface des résultats d'évaluation via l'UT "APV125 Consulter les résultats d'évaluation d'une structure"
- des restrictions via l'UT "APV143 Gérer les restrictions"

À partir de cette unité de tâche, l'ingénieur peut

**Mode d’automatisation :**

Interactif

**Complexité :**

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut consulter la liste des structures impliquées dans l'analyse de la demande.

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "APV112 Gérer une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de cinq secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Jusqu'à environ 11 000 structures possibles

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

La liste des structures reliées à la demande peut être consultée

###### 1.1.2.1.1 Diagramme APV121 Consulter les structures et leurs résultats d'analyse - contexte

<!-- image -->

Nom du diagramme :  APV121 Consulter les structures et leurs résultats d'analyse - contexte

Numéro de figure : 21

###### 1.1.2.1.2 Diagramme APV121 Consulter les structures et leurs résultats d'analyse - Scénario

<!-- image -->

Nom du diagramme :  APV121 Consulter les structures et leurs résultats d'analyse - Scénario

Numéro de figure : 22

##### 1.1.2.2 «Étape de tâche réutilisable»  APV122 Consulter le détail des hauteurs libres d'une structure

**Description :**

Cette étape de tâche réutilisable permet d'afficher le détail des hauteurs libres pour chaque structure concernée dans l'analyse de la demande.

Lhauteurs libres st composé de:

- le schéma

- le détail schéma

- la localisation

- l

- les repères relativement au passage en-dessous utilisés pour générer les conditions dans le rapport d’expertise

es informations ont obtenues via le service d système.

qui sont en dessous de la hauteur requise (hauteur du véhicule à l'étude + 10 cm (paramètre de système)).

L'utilisateur doit pouvoir cliquer sur le bouton "Suivant" et "Précédent" pour consulter les hauteurs libres de la prochaine ou de la précédente structure ou il peut retourner à la liste des structures.

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

**Conditions de réutilisation :**

Cette étape de tâche est utilisée pour consulter les résultats d'analyses d'une structure ou lors de la des hauteurs libres par l'UT APV148 Rechercher hauteur libre.

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Préconditions :**

Une structure doit être sélectionnée

**Postconditions :**

Les hauteurs libres de la structure sélectionnée peuvent être consultées, ainsi que les précédentes et les suivantes.

###### 1.1.2.2.1 Diagramme APV122 Consulter le détail des hauteurs libres d'une structure - contexte

<!-- image -->

Nom du diagramme :  APV122 Consulter le détail des hauteurs libres d'une structure - contexte

Numéro de figure : 23

###### 1.1.2.2.2 Diagramme APV122 Consulter le détail des hauteurs libres d'une structure - scénario

<!-- image -->

Nom du diagramme :  APV122 Consulter le détail des hauteurs libres d'une structure - scénario

Numéro de figure : 24

##### 1.1.2.3 «Unité de tâche»  APV123 Consulter le détail des résultats d'analyse d'une structure

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet d'afficher les résultats d'analyse, et ce pour chaque structure impliquée dans l'analyse de la demande.

Le détail de l'analyse d'une structure est composé de:

- la localisation de la structure (provient de GSQ)

- les caractéristiques de la structure (provient de GSQ ou déterminées par le système APV (travées types, no de tableau))

- les conditions de circulation de la structure (par défaut, de la restriction et de l'évaluation)

- Note concernant l'entrave (qui provient de APV142)

De plus, s'il y a une restriction et que la programmation n'a pas été validée par un autre ingénieur, un message d'avertissement doit s'afficher pour l'indiquer à l'ingénieur.

Un autre message d'avertissement doit aussi s'afficher, s'il y a une non-concordance de l'affichage (DLP vs GSQ) (C'est le traitement d'analyse structurale APV128 qui a fait la comparaison)

Les informations de la structure ont été obtenues via le service externe  système.

L'utilisateur doit pouvoir cliquer sur le bouton "Suivant" et "Précédent" pour consulter les résultats d'analyse structurale de la prochaine ou de la précédente structure.

L'utilisateur doit pouvoir accéder à l'écran des évaluations de la structure consultée via l'UT APV125 Consulter les résultats d'évaluation d'une structure", de consulter la programmation de la restriction via l'UT APV143 Gérer les restrictions" ou de retourner à la liste des structures.

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut consulter les résultats d'analyse d'une structure à l’égard des charges (sur laquelle passe le véhicule étudié).

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "Consulter les structures 'analyse"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de trois secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Jusqu'à environ 11 000 structures possibles

**Préconditions :**

Une structure doit être sélectionnée

**Postconditions :**

Les résultats d'analyse de la structure sélectionnée peuvent être consultés

###### 1.1.2.3.1 Diagramme APV123 Consulter le détail des résultats d'analyse d'une structure - contexte

<!-- image -->

Nom du diagramme :  APV123 Consulter le détail des résultats d'analyse d'une structure - contexte

Numéro de figure : 25

###### 1.1.2.3.2 Diagramme APV123 Consulter le détail des résultats d'analyse d'une structure - scénario

<!-- image -->

Nom du diagramme :  APV123 Consulter le détail des résultats d'analyse d'une structure - scénario

Numéro de figure : 26

##### 1.1.2.4 «Unité de tâche»  APV124 Consulter les entraves du parcours

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

Cette unité de tâche permet d'afficher le détail deimpliquée dans l'analyse de la demande.

L'affichage d'une entrave correspond au même contenu qui apparaît sur Québec511, dont le système TRR produit pour l'interne.  Les informations de l'entrave ont été obtenues via le service externe

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut consulter les entraves sur le parcours de la demande

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "APV112 Gérer une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de trois secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Selon la longueur du parcours, il peut y avoir plusieurs entraves, jusqu'à une centaine.

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

Les entraves reliées au parcours de la demande peuvent être consultées

###### 1.1.2.4.1 Diagramme APV124 Consulter les entraves du parcours

<!-- image -->

Nom du diagramme :  APV124 Consulter les entraves du parcours

Numéro de figure : 27

###### 1.1.2.4.2 

<!-- image -->

##### 1.1.2.5 «Unité de tâche»  APV125 Consulter les résultats d'évaluation d'une structure

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet d'afficher l'évaluation active du véhicule de référence (provient de GSQ) ayant servi à l'analyse structurale, et ce, pour une structure à la fois.  Chaque évaluation peut contenir plusieurs résultats d'évaluation (capacité des différents éléments de la structure, selon leur longueur et le type d’effort).

Pour chaque résultat d’évaluation, l'UT affiche le Mc (flexion) ou le Vc (cisaillement) du véhicule à l'étude du véhicule de référence ayant servi à l’évaluation, et ce, pour la longueur de travée spécifique.  De plus, elle doit afficher les résultats pour la flexion le cisaillement.

Les informations de l'évaluation du véhicule de référence (GSQ) ont été obtenues via le service externes

Chaque structure contient indicateur pour indiquer si lévaluation doit être considéré ou non pour déterminer les conditions de circulation, soit "Utiliser l'évaluation du véhicule de référence" (Se référer à l'UT APV144 - Gérer les évaluations).  L'affichage des résultats d'évaluation est fait en tenant compte de  indicateur:

- Si l'indicateur "Utiliser l'évaluation " est sélectionné, l'UT doit afficher les résultats d'évaluation du véhicule de référence.

L'UT doit permettre à l'utilisateur de consulter tous les résultats d'évaluation de la structure, une page après l'autre.

L'utilisateur doit pouvoir cliquer sur le bouton "Suivant" et "Précédent" pour consulter les résultats d'évaluation de la prochaine structure ou de la précédente.

L'utilisateur doit pouvoir accéder à l'écran des résultats d'analyse de la structure consultée via l'UT APV123 Consulter le détail des résultats d'analyse d'une structure ou de retourner à la liste des structures.

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut consulter les résultats d'évaluation d'une structure

**Modalités d’accès :**

L'unité de tâche est accédée à partir de l'UT "APV121 Consulter les structures et leurs résultats d'analyse"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Variable de 1 à 100 évaluations par demande qui est consultées

**Préconditions :**

Une structure doit être sélectionnée

**Postconditions :**

Les résultats d'évaluation de la structure sélectionnée peuvent être consultées

###### 1.1.2.5.1 Diagramme APV125 Consulter les résultats d'évaluation d'une structure

<!-- image -->

Nom du diagramme :  APV125 Consulter les résultats d'évaluation d'une structure

Numéro de figure : 28

##### 1.1.2.6 

|    |    |
|----|----|

###### 1.1.2.6.1 

<!-- image -->

###### 1.1.2.6.2 

<!-- image -->

##### 1.1.2.7 «Service 128 Produire une analyse structurale des ponts

| Niveau complexité   |    |
|---------------------|----|

**Description :**

Ce service permet de produire une analyse structurale pour tous les .

Il doit tenir compte des charges axiales et des espacements du véhicule à l'étude.

i une structure a un statut "À traiter", il doit assigner la condition "À traiter" et passer à l'analyse de la prochaine structure.

Pour :

**Condition de circulation par défaut (méthode simplifiée):**

**estriction:**

**valuation:**

**Conditions à inscrire sur le rapport d'expertise:**

Le système doit la condition appropriée entre "méthode simplifiée", "évaluation" et "restriction".

del'évaluationest atteinte ou dépassée indiquer au rapport la mention "Évaluation à revoir"

**Historique des analyses structurales :**

Pour chaque modification de la demande, l'ingénieur doit produire une nouvelle analyse structurale des ponts.  L'UT doit conserver un historique des analyses structurales.  L'identifiant de l'historique doit être le même no de version que celui de la demande.

**Complexité :**

Très très Complexe

**Paramètres :**

Liste de structures à analyser

**Conditions de réutilisation :**

À chaque fois qu'une analyse structurale est nécessaire, soit pour une nouvelle demande, pour une demande modifiée ou encore pour un scénario.

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de secondes.

**Préconditions :**

Le véhicule à l'étude doit avoir des charges axiales et des espacements.

**Postconditions :**

L'analyse structurale a été effectuée.

###### 1.1.2.7.1 Diagramme APV128 Produire une analyse structurale des ponts

<!-- image -->

Nom du diagramme :  APV128 Produire une analyse structurale des ponts

Numéro de figure : 29

##### 1.1.2.8 

|    |    |
|----|----|

##### 1.1.2.9 

|    |    |
|----|----|

##### 1.1.2.10 

|    |    |
|----|----|

#### 1.1.3 «Fonction» APV13 Production du rapport d'expertise/courriels/lettres

Cette fonction permet de produire automatiquement les rapports d'expertise et permet à l'ingénieur de les gérer et les signer.  Dans les cas où une expertise externe est nécessaire, cette fonction peut produire automatiquement des courriels et/ou des lettres et elle permet à l'ingénieur de les modifier et les envoyer.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV13 Production du rapport d'expertise/courriels/lettres

<!-- image -->

Nom du diagramme :  APV13 Production du rapport d'expertise/courriels/lettres

Numéro de figure : 30

Diagramme APV13 Production du rapport d'expertise/courriels/lettres\_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV13 Production du rapport d'expertise/courriels/lettres\_Arrimage axe Processus

Numéro de figure : 31

##### 1.1.3.1 «Unité de tâche»  APV131 Rechercher rapportd'expertise

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de rechercher des rapports d'expertise qui ont été produits pour d'anciennes demandes ou pour des demandes en cours d'analyse.

La recherche se fait à partir de différents critères tels que le numéro de la demande, le statut (acceptée et refusée), une plage de date, le nom de l'ingénieur et autres.  Il est aussi possible de faire une recherche textuelle.

À partir du résultat de la recherche, l'ingénieur peut consulter, modifier ou supprimer un rapport d'expertise à l'aide des différents boutons affichés pour chaque rapport.  Il peut aussi exporter le résultat de sa recherche dans un fichier Excel.  Pour consulter ou modifier un rapport d'expertise, l'UT doit appeler l'UT "APV132 Gérer le rapport d'expertise".

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Lorsque l'ingénieur a besoin de rechercher un rapport d'expertise

**Modalités d’accès :**

À partir du menu

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Environ 3000 rapports d'expertise par année

**Préconditions :**

**SO**

**Postconditions :**

Le résultat de la recherche est affiché et peut être exporté

###### 1.1.3.1.1 Diagramme APV131 Rechercher les rapports d'expertise

<!-- image -->

Nom du diagramme :  APV131 Rechercher les rapports d'expertise

Numéro de figure : 32

##### 1.1.3.2 «Unité de tâche»  APV132 Gérer le rapport d'expertise

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de consulter, créer, modifier le rapport d'expertise.  Ce dernier a été créé automatiquement par le service fonctionnel APV133 Produire le rapport d'expertise dans le cas d'une demande provenant de GPM et des demandes avec parcours et super-lourd qui ont été saisies manuellement.

Dans le cas d'une demande saisie manuellement sans parcours, l'ingénieur doit avoir la possibilité de créer le rapport  de saisir les informations manuellement.

Le rapport doit être affiché à l'interface et l'ingénieur peut modifier le contenu.

Si l'ingénieur doit refuser la demande, la section pour un refus s'affiche et l'utilisateur peut sélectionner la raison du refus.  Cependant, même si c'est un refus, les sections « Restrictions », "Réseau municipal", « Remarques additionnelles » et "Autre gestionnaire" doivent quand même être conservées.

Lorsqu'il est prêt, l'ingénieur peut faire produire le rapport en format PDF. L'UT nommera automatiquement le rapport avec le numéro de la demande et autres informations à définir lors du dossier fonctionnel.

Lors de la génération du rapport d'expertise en format PDF, seule la section appropriée doit être produite, soit les sections « Restrictions », "Réseau municipal", « Remarques additionnelles » et "Autre gestionnaire" pour une acceptation ou les sections « Raison du refus » et « Remarques additionnelles » pour un refus.  Toutes les sections doivent apparaître, même si elles sont vides.

Le rapport inclura également en annexe la demande (celle provenant de GPM en format PDF). Ainsi, les données de la demande analysée seront consultables à même ce rapport d’expertise.

Le rapport contient aussi une section pour la signature.  Elle doit être créée après les sections d’acceptation ou de refus et doit contenir le nom et le titre de l'ingénieur qui fait l'analyse de la demande (en appelant le service Web "GIA\_12\_Obtenir Information employé par code utilisateur" et la date du jour.

À partir de cette unité de tâche l'ingénieur pourra signer électroniquement le rapport d'expertise produit en format PDF via le service fonctionnel "APV136 Signer le rapport d'expertise" en lui passant en paramètres les coordonnées de la zone de signature et le document en format PDF.

Lorsque le rapport est signé, c'est l'ingénieur qui doit décider du moment où il veut le transmettre à GPM.  Au moment de la transmission, l'ingénieur doit pouvoir sélectionner des documents à joindre au rapport d'expertise, à partir des documents joints à la demande. Pour transférer le rapport et les documents joints, l'UT doit appeler le service fonctionnel "11.  L'UT devra aussi déposer le rapport dans la GID en appelant le service fonctionnel "APV118 Gérer les documents officiels dans la GID".

**Journalisation**

Tout changements apportés aux rapports d’expertise doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur veut accepter ou refuser le rapport d'expertise.

L'ingénieur veut créer, consulter ou modifier le rapport d'expertise.

**Modalités d’accès :**

À partir de l'UT de recherche des rapports d'expertise "APV131 Rechercher les rapports d'expertise" ou de la demande "APV112 Gérer une demande d'expertise"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance élevée.

**Fréquence d’activation :**

Pour chaque demande d'expertise

**Volume traité :**

Un seul rapport d'expertise à la fois.

**Préconditions :**

**SO**

**Postconditions :**

Le rapport d'expertise est produit, signé et envoyé à GPM.

###### 1.1.3.2.1 Diagramme APV132 Gérer le rapport d'expertise - Contexte

<!-- image -->

Nom du diagramme :  APV132 Gérer le rapport d'expertise - Contexte

Numéro de figure : 33

###### 1.1.3.2.2 Diagramme APV132 Gérer le rapport d'expertise-Scénario

<!-- image -->

Nom du diagramme :  APV132 Gérer le rapport d'expertise-Scénario

Numéro de figure : 34

##### 1.1.3.3 «Service fonctionnel»  APV133 Produire le rapport d'expertise

| Niveau complexité   |    |
|---------------------|----|

**Description :**

Ce service permet de produire les différentes sections du rapport d'expertise.  Il est appelé par les services d'analyses.

Pour une demande sans parcours:

- si l'état de la demande, reçu en paramètre, est "refusée", alors le rapport contiendra seulement la section pour un refus et la raison qui sera cochée est "Masse axiale trop élevée/Mauvaise configuration"

- si l'état de la demande, reçu en paramètre, est "nul", alors le rapport contiendra seulement la section»avec les conditions de circulation que le service a reçu en paramètre.

C'est à l'ingénieur que revient la décision finale d'accepter ou de refuser la demande.

**Historique des rapports d'expertise:**

Pour chaque modification de la demande, le système produit un nouveau rapport d'expertise.  L'UT doit conserver un historique des rapports d'expertise.  Donc si une analyse structurale est refaite sans que la demande ait eu une modification, les informations du rapport d'expertise ne seront pas conservées.

**Complexité :**

**Paramètres :**

-

**Conditions de réutilisation** :

Appelé par :

- le service externe APVRecevoir les demandes d'expertise de GPM

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de trois secondes.

**Préconditions :**

L paramètre obligatoire doit être reçu en entrée

**Postconditions :**

Le rapport d'expertise est créé.

###### 1.1.3.3.1 

<!-- image -->

##### 1.1.3.4 «Unité de tâche»  APV134 Gérer les courriels

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de produire ou de modifier un courriel qui est en relation avec une demande, et de l'envoyer au bon destinataire.  C'est pourquoi l'UT est accessible à partir d'une demande seulement.

Le courriel peut avoir été produit automatiquement dans le cas d'une demande qui implique des ponts qui appartiennent à des intervenants externes via le service fonctionnel "APV138 Produire les courriels".  Dans ce cas, l'ingénieur peut modifier le courriel avant de l'envoyer.  Lorsque le courriel est prêt, l'UT envoie le courriel à l'intervenant externe et l'accompagne de la demande provenant de GPM en format PDF.

L'utilisateur peut aussi créer un courriel à partir d'un gabarit.  Pour ce faire, l'unité de tâche permet à l'utilisateur de sélectionner le gabarit de courriel à utiliser et de modifier le contenu de ce dernier à sa guise.  L'adresse du destinataire et le sujet affichés sont ceux correspondant au gabarit, mais l'utilisateur peut les modifier.

Les courriels seront automatiquement déposés dans la GID.

**Journalisation**

Tout changements apportés aux courriels doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

Lorsque l'ingénieur veut envoyer un courriel qui est en relation avec une demande

**Modalités d’accès :**

Appelée par l'unité de tâche APV112 - Gérer une demande d'expertise

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 3 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Environ 500 fois par année

**Volume traité :**

Une seule demande à la fois est envoyée par courriel.

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

Le courriel est produit et envoyé.

###### 1.1.3.4.1 Diagramme APV134 Gérer les courriels

<!-- image -->

Nom du diagramme :  APV134 Gérer les courriels

Numéro de figure : 36

##### 1.1.3.5 «Unité de tâche»  APV135 Produire le bilan des analyses

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

Cette unité de tâche permet de produire le bilan des demandes d'expertise structurales pour le passage de véhicule hors norme sur les ponts.  L'utilisateur peut sélectionner pour quelle période il veut produire le rapport et pour  de demande.

Le rapport contient par jour le nombre de demandes acceptées et refusées avec les informations des demandes, tel que le numéro de la demande, le transporteur, la date de réception à la DGS, la date à laquelle la demande a été assignée à un ingénieur, le délai de traitement, à quelle date le permis a été délivré et le type de demande.

Le résultat est affiché à l'écran et peut être exporté dans un fichier Excel ou PDF.

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Pour fin de reddition de compte

**Modalités d’accès :**

À partir du menu

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Aux deux semaines

**Volume traité :**

Entre 50 à 100 demandes par semaine

**Préconditions :**

**SO**

**Postconditions :**

Le rapport est produit et peut être exporté.

##### 1.1.3.6 «Service fonctionnel»  APV136 Signer un document

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Ce service fonctionnel permet à l'ingénieur de signer le rapport d'expertise ou une lettre qui nécessite une signature numérique.

L'ingénieur doit être capable de saisir les paramètres nécessaires pour la signature, tel que le type de signature et autres.

, le service doit faire appel au service applicatif "Signer un document" de la couche d'intégration du MTMD

**Complexité :**

Simple

**Paramètres :**

Document en format PDF

Coordonnées de la zone de signature

**Conditions de réutilisation** *:*

À chaque fois qu'un ingénieur veut signer un document numériquement

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de trois secondes.

**Préconditions :**

Un document en format PDF doit être reçu en paramètre

**Postconditions :**

Le document PDF est signé numériquement.

###### 1.1.3.6.1 Diagramme APV136 Signer un document

<!-- image -->

Nom du diagramme :  APV136 Signer un document

Numéro de figure : 37

##### 1.1.3.7 «Service fonctionnel»  APV137 Produire les lettres

| Niveau complexité   | C   |
|---------------------|-----|

**Description :**

Ce service fonctionnel est appelé par différentes unités de tâche ou services fonctionnels pour produire des lettres.

Afin de produire la lettre, le service doit obtenir le gabarit correspondant au nom du gabarit reçu en paramètre et intégrer les informations reçues en paramètres, dans les sections à remplir.

La lettre doit être conservée avec la demande afin que l'ingénieur puisse la modifier et l'envoyer via l'UT "APV139 Gérer les lettres".

Pour le moment, le seul gabarit de lettre utilisé pour APV est pour la "lettre de demande d'évaluation des structures". Cette lettre est produite pour une demande de type "super-lourd", afin d'informer la firme externe des différentes structures rencontrées sur le parcours qui a été soumis par le transporteur.

Le service devra :

- remplir toutes les sections indiquées dans le gabarit

- inscrire toutes les routes du parcours dans le titre du tableau des structures

- lister la liste des structures rencontrées sur le parcours avec la localisation (nom de la route, l’obstacle et la municipalité). Les particularités et les remarques

- produire la section de la signature avec le nom et le titre de l'ingénieur qui fait l'analyse de la demande (en appelant le service Web "GIA\_12\_Obtenir Information employé par code utilisateur" et la date du jour.

Ce service doit pouvoir produire d'autres types de lettres dans l'avenir.

**Complexité :**

Complexe

**Paramètres :**

abarit de lettre à utiliser

de la demande

**Conditions de réutilisation** *:*

- Pour la production de différentes lettres

- Appelé par le service fonctionnel APV128 produire une analyse structurale des ponts

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de trois secondes.

**Préconditions :**

Selon le gabarit reçu en paramètre, les valeurs à inscrire dans les lettres doivent être reçues en paramètres

**Postconditions :**

La lettre est produite.

###### 1.1.3.7.1 

<!-- image -->

##### 1.1.3.8 «Service fonctionnel»  APV138 Produire les courriels

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Ce service fonctionnel est appelé par différentes unités de tâche ou services fonctionnels pour produire des courriels.

Afin de produire le courriel, le service doit obtenir le gabarit correspondant au nom du gabarit reçu en paramètre et intégrer les informations reçues en paramètres, dans les sections à remplir.

Le courriel doit être conservé avec la demande, afin que l'ingénieur puisse le modifier et l'envoyer via l'UT "APV134 Gérer les courriels".

Pour le moment, le seul gabarit de courriel utilisé pour APV est celui pour informer les intervenants externes qu'ils doivent analyser les structures leur appartenant pour le passage d'un véhicule hors norme, tel que spécifié dans la demande qui sera jointe au courriel.

Les étapes pour produire ce courriel sont:

- Un courriel être produit pour chaque structure d’un intervenant externe, dont le véhicule passe  la structure

- Un seul courriel par gestionnaire qui gère plusieurs structures rencontrées dans le parcours de la demande

- Obtenir l'adresse courriel des intervenants externes dans la table de pilotage (gestionnaire de la structure)

- Obtenir l'adresse courriel du technicien qui s'occupe de la demande et la mettre en CC

- Remplir la section indiquée dans le gabarit avec le numéro de la demande.

Ce service doit pouvoir produire d'autres types de courriels dans l'avenir.

**Complexité :**

Moyenne

**Paramètres :**

Numéro de la demande

**Conditions de réutilisation** *:*

Pour la production de différents courriels

**Critères de qualité (exigences) :**

Cette unité de tâche doit répondre dans un délai de moins de trois secondes.

**Préconditions :**

Selon le gabarit reçu en paramètre, les valeurs à inscrire dans les courriels doivent être reçues en paramètres

**Postconditions :**

Le courriel est produit.

##### 1.1.3.9 «Unité de tâche» APV139 Gérer les lettres

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de produire de modifier une lettre qui est en relation avec une demande, et de l'envoyer au bon destinataire.  C'est pourquoi l'UT est accessible à partir d'une demande seulement.

La lettre peut avoir été produite automatiquement dans le cas d'une demande "Super-lourd" via le service fonctionnel "APV137 Produire les lettres" pour créer la lettre de demande d'évaluation des structures.  Dans ce cas, l'ingénieur peut modifier la lettre, la produire en format PDF (l'UT nommera automatiquement la lettre avec le numéro de la demande et autres informations à définir lors du dossier fonctionnel) et la signer via le service fonctionnel "APV136 Signer un document".

Lorsque la lettre est signée, c'est l'ingénieur qui doit décider du moment où il veut la transmettre à GPM.  doit la lettre, le mandat d'évaluation l'UT doit appeler le service fonctionnel "".

L'utilisateur peut aussi créer une lettre à partir d'un gabarit.  Pour ce faire, l'unité de tâche permet à l'utilisateur de sélectionner le gabarit de lettres à utiliser et de modifier le contenu de ce dernier à sa guise.  L'adresse du destinataire et le sujet affichés sont ceux correspondant au gabarit, mais l'utilisateur peut les modifier.

Les lettres produites seront déposées dans la GID

**Journalisation**

Tout changements apportés aux lettres doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

Lettre en format Word

**Circonstances d’utilisation :**

Lorsque l'ingénieur veut envoyer une lettre qui est en relation avec une demande.

**Modalités d’accès :**

Appelée par l'unité de tâche APV112 - Gérer une demande d'expertise

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 3 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

Environ 50 lettres par année

**Volume traité :**

Une seule lettre à la fois

**Préconditions :**

Une demande doit être sélectionnée

**Postconditions :**

La lettre est produite, signée, si nécessaire et envoyée par courriel

###### 1.1.3.9.1 

<!-- image -->

###### 1.1.3.9.2 Diagramme APV139 Gérer les lettres

<!-- image -->

Nom du diagramme :  APV139 Gérer les lettres

Numéro de figure : 38

##### 1.1.3.10 

|    |    |
|----|----|

#### 1.1.4 «Fonction» APV14 Gestion technique des structures

Cette fonction permet à l'ingénieur de gérer les structures, c'est-à-dire de gérer les restrictions, les évaluations, l'état des structures et les repères.  Elle permet d'importer les structures, à une fréquence régulière, du système GSQ.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV14 Gestion technique des structures

<!-- image -->

Nom du diagramme :  APV14 Gestion technique des structures

Numéro de figure : 39

Diagramme APV14 Gestion technique des structures\_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV14 Gestion technique des structures\_Arrimage axe Processus

Numéro de figure : 40

##### 1.1.4.1 «Unité de tâche»  APV141 Rechercher les structures

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

L'unité de tâche permet de rechercher les structures.  Elle permet à l’utilisateur de saisir les critères de recherche tel que numéro de la structure, etc.), dont notamment une recherche textuelle.

À partir du résultat de la recherche, l'ingénieur peut consulter, modifier une structure à l'aide des différents boutons affichés pour chaque structure.  Il peut aussi exporter le résultat de sa recherche dans un fichier Excel.

Cette unité de tâche servira aussi pour rechercher toutes les structures qui ont été modifiées dans GSQ et qui doivent être prise en charge (indicateur "à traiter") par un ingénieur.

**Mode d’automatisation :**

Interactif

**Complexité :**

Très simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut rechercher une ou plusieurs structures

**Modalités d’accès :**

Cette unité de tâche est accessible à partir du menu "Structure".

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Moyenne

**Fréquence d’activation :**

À la demande

**Volume traité :**

Environ 11 000 structures

**Préconditions :**

**SO**

**Postconditions :**

· les résultats de la recherche sont affichés

- À partir des résultats de recherche, l’utilisateur peut

- consulter une structure
- modifier une structure
- exporter le résultat de sa recherche dans un fichier Excel.

###### 1.1.4.1.1 

<!-- image -->

###### 1.1.4.1.2 Diagramme APV141 Rechercher les structures

<!-- image -->

Nom du diagramme :  APV141 Rechercher les structures

Numéro de figure : 41

##### 1.1.4.2 «Unité de tâche»  APV142 Gérer les structures

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

L'historique des modifications concernant le statut GSQ, les données de localisation et les caractéristiques doivent être consultables à partir de cette UT.  Les données doivent êtreobtenues service en passant en paramètres le numéro de la structure, et de la BD de APV concernant le no de tableau de seuils et la distribution des travées.

**Journalisation**

Tout changements apportés aux structures doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

Numéro de la structure

**Circonstances d’utilisation :**

Lorsqu'il y a un sur une structure au niveau du système GSQ, les ingénieurs doivent vérifier et analyser la structure.

**Modalités d’accès :**

À partir de l'écran de recherche des structures "APV141 Rechercher les structures"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance élevée.

**Fréquence d’activation :**

À chaque fois qu'une structure a été modifiée

**Volume traité :**

Il existe environ 11000 structures

**Préconditions :**

Une structure doit avoir été sélectionnée

**Postconditions :**

Les données des structures (restrictions, évaluation, inspection et repères) ont été mises à jour

###### 1.1.4.2.1 Diagramme APV142 Gérer les structures - Contexte

<!-- image -->

Nom du diagramme :  APV142 Gérer les structures - Contexte

Numéro de figure : 42

###### 1.1.4.2.2 Diagramme APV142 Gérer les structures - scénario

<!-- image -->

Nom du diagramme :  APV142 Gérer les structures - scénario

Numéro de figure : 43

##### 1.1.4.3 «Unité de tâche»  APV143 Gérer les restrictions

| Niveau complexité   | M   |
|---------------------|-----|

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

Numéro de la structure

**Circonstances d’utilisation :**

L'ingénieur veut consulter une restriction

L'ingénieur doit modifier une restriction suite à une modification de la restriction dans GSQ.

**Modalités d’accès :**

À partir de l'UT "APV142 Gérer les structures"

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Une seule restriction active par structure

**Préconditions :**

Une structure doit être sélectionnée **.**

**Postconditions :**

Les restrictions sont consultées

La programmation est mise à jour et l'ancienne est conservée en historique.

###### 1.1.4.3.1 Diagramme APV143 Gérer les restrictions

<!-- image -->

Nom du diagramme :  APV143 Gérer les restrictions

Numéro de figure : 44

##### 1.1.4.4 «Unité de tâche»  APV144 Gérer les évaluations

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de consulter les évaluation () structure  Une structure peut avoir plusieurs évaluations, De plus, une évaluation peut contenir plusieurs résultats.

.

.

L'ingénieur doit pouvoir saisir des notes pour chaque résultat d'évaluation.

Lorsque l'utilisateur a terminé les modifications à effectuer sur les évaluations, il doit être en mesure de le spécifier afin que l'indicateur de modification soit remis à nul et que l'onglet deviennent grisé.

**Journalisation**

Tout changements apportés aux évaluations doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

Numéro de la structure

**Circonstances d’utilisation :**

L'ingénieur veut consulter l'évaluation du véhicule de référence pour une structure.

L'ingénieur veut ajouter, modifier ou consulter l'évaluation des véhicules types pour une structure

**Modalités d’accès :**

À partir de l'UT "APV142 Gérer les structures"

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Environ 10 000 résultats d’évaluation

**Préconditions :**

Une structure doit être sélectionnée.

**Postconditions :**

Les évaluations provenant de GSQ sont consultées.

Les évaluations des véhicules types sont mises à jour.

Les indicateurs de prise en compte sont mis à jour.

###### 1.1.4.4.1 Diagramme APV144 Gérer les évaluations - contexte

<!-- image -->

Nom du diagramme :  APV144 Gérer les évaluations - contexte

Numéro de figure : 45

###### 1.1.4.4.2 Diagramme APV144 Gérer les évaluations - Scénario

<!-- image -->

Nom du diagramme :  APV144 Gérer les évaluations - Scénario

Numéro de figure : 46

##### 1.1.4.5 «Unité de tâche»  APV145 l'état des structures (inspections)

| Niveau complexité   | S   |
|---------------------|-----|

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

Numéro de la structure

**Circonstances d’utilisation :**

L'ingénieur doit consulter l'état de la structure suite à une nouvelle inspection dans GSQ.

**Modalités d’accès :**

À partir de l'UT "APV142 Gérer les structures"

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 3 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance moyenne.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Entre 0 et 30 éléments modifiés et à prendre en compte pour une structure par année

**Préconditions :**

Une structure doit être sélectionnée.

**Postconditions :**

Les données d'inspection peuvent être consultées.

###### 1.1.4.5.1 Diagramme APV145 Gérer l'état des structures (inspections) - Contexte

<!-- image -->

Nom du diagramme :  APV145 Gérer l'état des structures (inspections) - Contexte

Numéro de figure : 47

###### 1.1.4.5.2 Diagramme APV145 Gérer l'état des structures (inspections) - Scénario

<!-- image -->

Nom du diagramme :  APV145 Gérer l'état des structures (inspections) - Scénario

Numéro de figure : 48

##### 1.1.4.6 «Unité de tâche»  APV146 Gérer les repères

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

**Journalisation**

Tout changements apportés aux repères doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

simple

**Paramètres :**

Numéro de la structure

**Circonstances d’utilisation :**

**Modalités d’accès :**

À partir de l'UT "APV142 Gérer les structures"

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 3 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

À la demande

**Volume traité :**

1 à 4 repères par structure

**Préconditions :**

**Une structure doit être sélectionnée.**

**Postconditions :**

Les repères ont été créés ou modifiés.

###### 1.1.4.6.1 Diagramme APV146 Gérer les repères

<!-- image -->

Nom du diagramme :  APV146 Gérer les repères

Numéro de figure : 49

##### 1.1.4.7 «» APV147 Obtenir les des structures de GSQ

| Niveau complexité   |    |
|---------------------|----|

**Description :**

permet d'obtenir les  sur les structures de GSQ, afin d'avoir les informations des structures à jour pour procéder aux analyses structurales et d'informer les ingénieurs.

Le traitement complet compare les données , des restrictions, des évaluations et des inspections.

partiel compare seulement les données de .

Les données à sont

les données d’inventaire : localisation, type de structure générale, type de structure par travée, chargement de conception, nombre de travées, longueur des travées, année de construction, les affichages, etc.;

**Mise à jour du statut d'une structure**

Pour chaque structure qui est modifiée (en tenant compte seulement des types de modification qui ont été spécifiés dans la table de pilotage et de l'indicateur ), le système doit modifier le statut de la structure pour "À traiter", afin que l'ingénieur puisse procéder à la vérification de la structure et modifier la programmation de la restriction, si nécessaire, et spécifier si l'évaluation doit être prise en compte ou non, si nécessaire.

Si pour un type de modification, l'indicateur "À traiter" est coché et  autre type de modification, il n'est pas coché et que les deux types de modification se produisent en même temps sur une structure, c'est le type de modification avec l'indicateur coché qui doit être pris en compte, donc la structure aura le statut "À traiter".

**Complexité :**

**Paramètres :**

SO

**Circonstances d’utilisation :**

Les ingénieurs doivent être informés rapidement des aux structures qui sont faites dans le système GSQ.

**Modalités d’accès :**

SO

**Critères de qualité (exigences) :**

Conforme aux normes d'un prod-lot

**Aspects critiques de la performance :**

Importance élevée.

**Fréquence d’activation :**

Le traitement complet doit s'exécuter une fois le matin et par la suite le traitement partiel aux deux heures

**Volume traité :**

Il existe environ 11 000 structures dans GSQ

**Préconditions :**

**SO**

**Postconditions :**

Les modifications aux structures ont été conservées et un historique a été conservé

###### 1.1.4.7.1 Diagramme APV147 Obtenir les modifications des structures de GSQ

<!-- image -->

Nom du diagramme :  APV147 Obtenir les modifications des structures de GSQ

Numéro de figure : 50

##### 1.1.4.8 «Unité de tâche»  APV148 Rechercher et consulter les hauteurs libres

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

L'unité de tâche permet de consulter les hauteurs libres.  Pour ce faire,

l'étape de tâche réutilisable "APV122 Consulter le détail des hauteurs libres d'une structure".   la localisation de la structure, schéma représentant les points de mesure, les repères, les données de hauteurs ainsi que des remarques et commentaires.

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'ingénieur doit pouvoir consulter les hauteurs libres lorsqu'il y a problème avec une structure

**Modalités d’accès :**

À partir du menu

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de 3 secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Il y a 1 500 hauteurs libres.

**Préconditions :**

**SO**

**Postconditions :**

Les hauteurs libres sont affichées et sont consultables.

###### 1.1.4.8.1 Diagramme APV148 Rechercher et consulter les hauteurs libres

<!-- image -->

Nom du diagramme :  APV148 Rechercher et consulter les hauteurs libres

Numéro de figure : 51

##### 1.1.4.9 

|    |    |
|----|----|

###### 1.1.4.9.1 

##### 1.1.4.10 

|    |    |
|----|----|

##### 1.1.4.11 

|    |    |
|----|----|

###### 1.1.4.11.1 

##### 1.1.4.12 

|    |    |
|----|----|

###### 1.1.4.12.1 

##### 1.1.4.13 

|    |    |
|----|----|

##### 1.1.4.14 

|    |    |
|----|----|

##### 1.1.4.15 

|    |    |
|----|----|

#### 1.1.5 «Fonction» APV15 Gestion du pilotage et de l'administration du système

Cette fonction regroupe toutes les fonctionnalités qui permettent de gérer les données de pilotage et d'administrer le système, soit les paramètres de système, les domaines de valeur, la gestion du menu et différentes données de pilotage utilisés par le système.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV15 Gestion du pilotage et de l'administration du système

<!-- image -->

Nom du diagramme :  APV15 Gestion du pilotage et de l'administration du système

Numéro de figure : 52

Diagramme APV15 Gestion du pilotage et de l'administration du système\_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV15 Gestion du pilotage et de l'administration du système\_Arrimage axe Processus

Numéro de figure : 53

##### 1.1.5.1 «Unité de tâche»  APV151 Gérer les domaines de valeur

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet au pilote de gérer les différents domaines de valeur utilisés par l’application APV.

Elle permet de modifier ou de mettre fin à un domaine de valeurs.  Et pour chaque domaine, elle permet de modifier ou de mettre fin à une valeur d'un domaine.

Pour chaque valeur, il doit y avoir une date de début et s'il y a lieu, une date de fin d'effectivité.

**Journalisation**

Tout changements apportés aux domaines de valeurs et à leurs valeurs doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut ajouter, modifier ou mettre fin à une valeur d'un domaine ou à un domaine de valeur.

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ une quinzaine de domaines de valeurs.  Et pour chaque domaine, le nombre de valeur peut varier de quelques-unes à une centaine.

**Préconditions :**

Le pilote a les droits d'accès pour gérer les domaines de valeurs.

**Postconditions :**

Un nouveau domaine ou une nouvelle valeur à un domaine a été ajouté

Un domaine ou une valeur à un domaine a été modifié

##### 1.1.5.2 «Unité de tâche»  APV152 Gérer les paramètres du système

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

Cette unité de tâche permet de modifier ou de mettre fin à un paramètre de système.

Pour chaque paramètre, l'utilisateur doit saisir une date de début et lorsque la valeur du paramètre change, une date de fin d'effectivité.

Les paramètres de système peuvent correspondre par exemple à :

- une adresse URL nécessaire pour un hyperlien dans l'application

- l'adresse courriel du pilote dans le cas où une notification ou un rapport doit lui être envoyée

- etc.

Ces paramètres seront définis lors du développement de l'application APV, mais les paramètres suivants doivent être pris en compte :

- Valeur Alpha L\_PS et Alpha\_L\_NP

- écart entre les cotes de comportement et de matériaux

- autres à venir

De plus, certains paramètres peuvent seulement être consultés.

**Journalisation :**

Tout changements apportés aux paramètres de systèmes doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut ajouter, modifier ou mettre fin à un paramètre de système.

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Volume très faible

**Préconditions :**

SO

**Postconditions :**

Un paramètre a été créé, modifié ou consulté.

##### 1.1.5.3 «Unité de tâche»  APV153 Gérer les gabarits de communication

| Niveau complexité   | TS   |
|---------------------|------|

**Description :**

Cette unité de tâche permet au pilote de créer, modifier et mettre fin à des gabarits de communication.  Ces gabarits seront utilisés pour les différents courriels, lettres et notifications à produire par le système.  Le gabarit pour le rapport d'expertise est aussi géré par cette UT.

Les gabarits doivent être en format Word et peuvent contenir des champs ou sections que le système peut remplir automatiquement.  Pour chaque gabarit, le pilote devra spécifier de quel type est le gabarit (lettre, courriel, notification, rapport), le sujet du courriel ou de la lettre

Chaque gabarit doit avoir une date de début d'effectivité et s'il y a lieu une date de fin d'effectivité.

**Journalisation**

Tout changements apportés aux gabarits de communication doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut ajouter, modifier ou mettre fin à  de communication

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ une 6 gabarits de communication.

**Préconditions :**

Le pilote a les droits d'accès pour gérer les gabarits de communication

**Postconditions :**

Un nouveau gabarit de communication a été ajouté

Un gabarit de communication a été modifié.

##### 1.1.5.4 «Unité de tâche»  APV154 Gérer les intervenants externes

| Niveau complexité   | TTS   |
|---------------------|-------|

**Description :**

Cette unité de tâche permet de créer, modifier et mettre fin à des intervenants externes.  Ces intervenants sont ceux à qui l'ingénieur doit envoyer un courriel lorsqu'un parcours passe sur une structure appartenant à ces intervenants (Ex: Hydro Québec, Fédéral, etc.).  Les informations sur l'organisation, les coordonnées, les adresses courriel, les personnes à contacter doivent être saisies.

De plus, le pilote doit pouvoir saisir la liste des numéros de structures qui appartiennent à l'intervenant.

Chaque intervenant doit avoir une date de début d'effectivité et s'il y a lieu une date de fin d'effectivité.

**Journalisation :**

Tout changements apportés aux intervenants externes doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très très simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut ajouter, modifier ou mettre fin à un intervenant externe

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ une quinzaine d'intervenants externes.

**Préconditions :**

Le pilote a les droits d'accès pour gérer les intervenants externes.

**Postconditions :**

Un nouvel intervenant externe a été ajouté

Un intervenant externe a été modifié.

##### 1.1.5.5 «Unité de tâche»  APV155 Gérer les conditions de circulation

| Niveau complexité   | TTS   |
|---------------------|-------|

**Description :**

Cette unité de tâche permet de créer, modifier et supprimer (inscrire une date de fin) les conditions de circulation qui seront utilisées pour établir les différents tableaux de seuils.

Le pilote doit pouvoir saisir la condition à inscrire sur le permis, le code associé, une description de la condition et l'ordonnancement de sévérité. De plus, le pilote doit choisir avec quel type d'analyse la condition doit être associée.  Elle peut être associée à plus d'un type d'analyse.

Par exemple, la condition sur le permis "Circulation à 40 km/h", le code "A-I", la description "Le véhicule doit circuler à 40 km/h" et l'ordre de sévérité "2".

Chaque condition de circulation doit avoir une date de début et de fin d'effectivité.

**Journalisation :**

Tout changements apportés aux conditions de circulation doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très très simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Le pilote veut ajouter, modifier ou supprimer une condition de circulation

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ 10 conditions de circulation.

**Préconditions :**

L'utilisateur a les droits d'accès pour gérer les conditions de circulation

**Postconditions :**

Les conditions de circulation ont été mises à jour.

##### 1.1.5.6 «Étape de tâche réutilisable»  APV156 Afficher le menu du système

**Description :**

Cette étape de tâche réutilisable sera utilisée par chaque unité de tâche interactive.  Elle permet d'afficher les menus du système, ainsi que l'aide en ligne.

Elle affiche aussi les liens URL vers le système SIT (511), le site internet SIGO, la page intranet du MTQ pour les permis spéciaux et la visionneuse.  Ces URL sont paramétrables.

La visionneuse permet aux utilisateurs de produire des rapports ad hoc à partir des services d'entités et de facettes (P171U Services - APV).

Elle doit aussi contenir une section pour afficher différents messages, tel que le nombre de structures dont le statut est "à traiter", le nombre de demandes non assignées, le nombre de nouveaux messages dans la boîte commune de la DGeS, etc.

Ces différents nombres doivent être calculés par l’étape de tâche à chaque ouverture de session.

Cette interface doit utiliser le Programme d'identification visuel (PIV) du MTQ.

**Mode d’automatisation :**

Interactif

**Complexité :**

Très simple

**Paramètres :**

SO

**Conditions de réutilisation :**

Cette étape de tâche est utilisée lors de l'affichage de toutes les interfaces du système

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Préconditions :**

**SO**

**Postconditions :**

Le menu du système est affiché

##### 1.1.5.7 «Unité de tâche»  APV157 Gérer les véhicules types et de référence

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de créer, modifier, dupliquer ou mettre fin aux véhicules de référence et aux véhicules types.

Pour chaque véhicule, le pilote doit saisir le nom, le type de véhicule (référence ou type), les caractéristiques du véhicule, tel que le nombre d'essieux, ainsi que les charges axiales et les espacements.  Pour les véhicules types seulement, en plus de saisir les mêmes caractéristiques, il doit aussi saisir des plages de valeur pour chacun des essieux et espacement.  Les plages de valeur serviront à déterminer à quel véhicule type le véhicule à l'étude d'une demande sera associé, s'il y a lieu.

Le pilote doit aussi associer le véhicule de référence aux différents camions d'évaluation provenant de GSQ (ex: S6-14-CL625 et S6-00-CL625, devraient être associés au véhicule de référence CL625 de APV).

À partir de ces données, le système calcule les efforts de flexion (MC) et les efforts de cisaillement (VC).  Pour ce faire, le traitement doit appeler le service "GPM\_3\_Calculer les efforts de flexion et de cisaillement d'un véhicule et leurs ratios" (à déterminer au DF si on doit le calculer et le conserver selon la décision du service GPM\_3).  Aucun ratio n'est calculé pour les véhicules de référence et type.

Le calcul doit être effectué pour les travées de 1 à 50 m et les résultats des calculs doivent être affichés de la même manière que dans l'interface d'une demande d'expertise.

Il ne peut y avoir qu'un seul véhicule de référence actif en tout temps, pour le calcul des ratios. Les autres véhicules de références serviront dans les calculs des évaluations.

L'interface doit avoir une case à cocher afin que le pilote puisse indiquer quel véhicule de référence sert pour analyser les ratios d'une demande d'expertise.

Chaque type de véhicule doit avoir une date de début d'effectivité et s'il y a lieu une date de fin d'effectivité.

Toutes modifications au véhicule de référence actif devront être transférées au système GPM.  Elles seront utilisées pour le calcul des efforts de flexion et de cisaillement.

**Journalisation**

Tout changements apportés aux véhicules types et de référence doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Le pilote doit mettre à jour les véhicules types et de référence.

**Modalités d’accès :**

À partir du menu "Pilotage"

**Critères de qualité (exigences) :**

L'interface doit s'afficher dans un délai maximal de secondes. Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance Faible.

**Fréquence d’activation :**

À la demande

**Volume traité :**

Il peut avoir xxxx type de véhicules

**Préconditions :**

**SO**

**Postconditions :**

Les véhicules de référence et les véhicules types sont mis à jour.

###### 1.1.5.7.1 Diagramme APV157 Gérer les véhicules types et de référence

<!-- image -->

Nom du diagramme :  APV157 Gérer les véhicules types et de référence

Numéro de figure : 54

##### 1.1.5.8 «Unité de tâche»  APV158 Gérer les seuils

| Niveau complexité   | M   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de créer, modifier, dupliquer et mettre fin à un tableau de seuils d'équivalence en flexion et cisaillement, pour des véhicules de référence (ex: CL625) et d'équivalence à la classe 5, pour différentes longueurs de travée Exemple: 10, 20, 30, 40 et 50 mètres.

Se référer au fichier "Seuils\_limites(2019-12)" pour comprendre les tableaux 1 à 5.

Pour créer un tableau, l'unité de tâche doit demander les critères suivants:

- Type d'affichage: liste déroulante correspondant au domaine de valeur: pont non affiché, ponts interdits aux surcharges, limitation de poids (Choix de 2 types d'affichage maximum)

- Charge de conception: liste déroulante correspondant aux charges de conception (domaine de valeur) (il peut y en avoir plus d'une par tableau)

- Année de construction du pont (inférieure à, supérieure à ou égale à)

- Type de structure : liste déroulante correspondant au domaine de valeur: type bois-acier, autres

- Avec ou sans évaluation

- Évaluation du véhicule de référence prise en compte ou non

Par la suite, le pilote doit saisir le tableau qui va servir à déterminer le niveau de sévérité du véhicule à l'étude. Pour ce faire, il doit saisir une description et les valeurs de ratio pour la flexion et le cisaillement de l'équivalence aux charges légales et de l'équivalence à la classe 5.

Pour les tableaux 2, 3 et 4, le pilote peut modifier la description de la formule et sélectionner la condition de circulation liée à chaque ligne du tableau, à partir d'une liste déroulante dont les valeurs ont été définies dans la table de pilotage des conditions de circulation (APV155).

Cependant, les formules utilisées pour le calcul de la flexion et du cisaillement pour les différentes longueurs de travées (10, 20, 30, 40 et 50m) seront "hard codées".  Les formules doivent tenir compte des facteurs liés à la vitesse, au groupe de structure et type de structure (dalle ou poutre).

Si l'utilisateur veut créer un nouveau tableau, les valeurs de flexion et de cisaillement ne seront pas calculées automatiquement, c'est le pilote qui devra les saisir pour chaque condition.

Ces tableaux servent à déterminer les conditions de circulation par défaut, selon les caractéristiques des structures.

Si les longueurs de travées sont modifiées, un message doit être affiché afin d'informer le pilote qu'il doit revoir les étendues de travées.  Et même de pouvoir accéder aux étendues directement via cette unité de tâche.

Chaque tableau doit avoir une date de début d'effectivité et s'il y a lieu une date de fin d'effectivité.

Les valeurs du tableau "1" correspondant au calcul des efforts de flexion et de cisaillement devront être transférées au système GPM lorsqu'elles sont modifiées.  Pour ce faire, l'UT doit appeler le service GPM\_5\_Recevoir les valeurs des seuils.

**Journalisation**

Tout changements apportés aux tableaux des seuils doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Moyenne

**Paramètres :**

SO

**Circonstances d’utilisation :**

Le pilote veut ajouter, modifier ou mettre fin à tableau de seuils

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ 5 tableaux

**Préconditions :**

Le pilote a les droits d'accès pour gérer les tableaux de seuils.

**Postconditions :**

Un nouveau tableau de seuils a été ajouté

Un tableau de seuils a été modifié

##### 1.1.5.9 «Unité de tâche»  APV159 Gérer les types  des structures à notifier

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de gérer les différents types  reliés aux structures du système GSQ, qui ont un impact sur les demandes de permis et pour lesquels les ingénieurs doivent être informés.

Les types  ne sont pas pilotables.  Cependant, pour chaque type , le pilote doit sélectionner le statut à apposer sur la structure (à traiter ou non), si doit être notifiée à l'ingénieur dont la demande est impactée et en cours et si  doit être notifiée au pilote de APV.

Ces types  sont utilisés lors du traitement "APV147 Obtenir les des structures de GSQ".

Les types  sont par exemple:

- Modification des travées;
- Nouvelle évaluation;
- Nouveau résultat d’évaluation;
- Modification d'un résultat d'évaluation;
- Nouvelle restriction;
- Modification d’une restriction;
- Changement d’état (cote de comportement et de matériaux), selon les écarts définis par le pilote;

Les valeurs des écarts entre les cotes de comportement et de matériaux doivent être paramétrables via l'UT "APV152 Gérer les paramètres".  Par exemple, si l'écart entre les cotes doit être plus grand que "10" pour que la modification soit significative pour les ingénieurs, la valeur "10" est paramétrable.  Il se peut qu'il y ait d'autres valeurs paramétrables et seront définies lorsque les types de modification seront déterminés par le pilote.

**Journalisation**

Tout changements apportés doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

Le pilote veut modifier les indicateurs associés aux types .

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

Environ 15 types

**Préconditions :**

Le pilote a les droits d'accès pour gérer les types .

**Postconditions :**

Les indicateurs associés aux types ont été mis à jour.

##### 1.1.5.10 «Unité de tâche»  APV15A Gérer les facteurs liés à la vitesse et au groupe de structure

| Niveau complexité   | TTS   |
|---------------------|-------|

**Description :**

Cette unité de tâche permet de définir et modifier les facteurs liés à la vitesse et au groupe de structure.  Ces facteurs seront ensuite utilisés avec les tableaux de seuils définis via l'UT "APV158 Gérer les seuils".  Ils peuvent aussi être utilisés dans les différents calculs d'évaluation et de restrictions.

Les groupes de structure et les vitesses ont été définis dans les domaines de valeurs.  Ex: pont à voie unique, à poutres, etc.

Pour chaque groupe de structure et chaque vitesse, le pilote doit saisir le facteur correspondant et la date d'effectivité de début.  Lorsque la valeur du facteur est modifiée, une date de fin d'effectivité doit être saisie et ajouter la nouvelle valeur.

Pour référence, consulter le fichier "Seuils\_limite (2019)", les deux premiers tableaux.

Toutes modifications devront être transférées au système GPM lorsqu'elles sont modifiées.  Elles seront utilisées pour le calcul des efforts de flexion et de cisaillement.

**Journalisation :**

Tout changements apportés aux facteurs doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très très Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut ajouter ou modifier les facteurs liés à la vitesse et/ou au groupede structure.

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

4 facteurs liés au type de structure, mais il peut y en avoir plus, si des types de structures sont ajoutés aux domaines de valeurs

2 facteurs liés à la vitesse, mais il peut y en avoir plus, si des vitesses sont ajoutées aux domaines de valeurs

**Préconditions :**

Le pilote a les droits d'accès pour gérer les facteurs

**Postconditions :**

Un nouveau facteur a été ajouté à un groupe de structure ou à la vitesse

Les valeurs des facteurs ont été modifiées

##### 1.1.5.11 «Unité de tâche»  APV15B Gérer les étendues de travées

| Niveau complexité   | TTS   |
|---------------------|-------|

**Description :**

Cette unité de tâche permet au pilote de créer modifier un intervalle de longueur Par exemple, pour la travée de 10m, la longueur de travée doit être située entre 0 et 15m. **Note** : à définir au dossier fonctionnel, si les valeurs sont en mètre ou en millimètre.

Ces intervalles servent à déterminer le nombre de travées qui se retrouvent dans chaque travée type (Ex: 10m, 20m, etc.) pour chaque structure.

Pour chaque travée, l'utilisateur doit saisir une date de début et lorsque l'intervalle de longueur change, une date de fin d'effectivité doit s'inscrire automatiquement, mais peut aussi être saisie par le pilote.

**Journalisation**

Tout changements apportés aux étendues de travées doivent être journalisés via le service fonctionnel « APV15C Journaliser les actions (Qui, quoi, quand) ».

**Mode d’automatisation :**

Interactif

**Complexité :**

Très très simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut modifier ou mettre fin à un intervalle de longueur de travée.

**Modalités d’accès :**

À partir menu "Pilotage"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de 3 secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Peu fréquent

**Volume traité :**

5 travées.

**Préconditions :**

Le pilote a les droits d'accès pour gérer les distances de travées.

**Postconditions :**

L'intervalle de longueur d'une travée a été modifié.

##### 1.1.5.12 «Service fonctionnel»  APV15C Journaliser les actions (Qui, quoi, quand)

| Niveau complexité   | TTS   |
|---------------------|-------|

**Description :**

Ce service permet de journaliser toutes les actions faites dans le système APV.  Il est appelé par toutes les unités de tâche qui nécessitent une journalisation.

L'unité appelante doit passer en paramètres les informations de l'action, soit la date à laquelle elle s'est produite, l'utilisateur ayant déclenché l'action, le code de l'unité de tâche et sa description, l'identifiant de la demande, de la structure ou autre identifiant.

Les paramètres reçus pour chaque appel sont enregistrés dans la BD du système APV.

**Mode d’automatisation :**

Service

**Complexité :**

Très très Simple

**Paramètres :**

- Le numéro d’utilisateur

- La date et heure

- Le code de l'unité de traitement appelante et sa description

- L'identifiant de l'élément en cours

**Conditions de réutilisation :**

Ce service est utilisé pour la journalisation des actions effectuées dans chaque unité de tâches du système APV.

**Critères de qualité (exigences) :**

Elle doit respecter les règles du cadre d'application en vigueur.

**Préconditions :**

SO

**Postconditions :**

Les actions sont enregistrées dans la BD du système APV.

#### 1.1.6 «Fonction» APV16 Gestion de la messagerie interne

Cette fonction permet de gérer la messagerie interne, donc de produire et envoyer automatiquement des notifications dans la messagerie interne afin d'informer les ingénieurs.

Elle permet à l'ingénieur de consulter et supprimer les notifications.

| Critères de découpage   | <memo>*   |
|-------------------------|-----------|

Diagramme APV16 Gestion de la messagerie interne

<!-- image -->

Nom du diagramme :  APV16 Gestion de la messagerie interne

Numéro de figure : 55

Diagramme APV16 Gestion de la messagerie interne\_Arrimage axe Processus

<!-- image -->

Nom du diagramme :  APV16 Gestion de la messagerie interne\_Arrimage axe Processus

Numéro de figure : 56

##### 1.1.6.1 «Unité de tâche»  APV161 Rechercher et consulter les notifications

| Niveau complexité   | S   |
|---------------------|-----|

**Description :**

Cette unité de tâche permet de rechercher les notifications à partir de différents critères tels que le code utilisateur, la date, le type de notification, etc.

Elle permet aussi de consulter le contenu des notifications et pour chaque utilisateur, inscrire "comme lu" ou encore de la supprimer (on entend par supprimer que l'utilisateur ne veut plus voir cette notification, mais elle n'est pas détruite et les autres utilisateurs peuvent encore la consulter).  Les notifications supprimées pourront quand même être consultables, un peu comme dans Outlook.

**Mode d’automatisation :**

Interactif

**Complexité :**

Simple

**Paramètres :**

SO

**Circonstances d’utilisation :**

L'utilisateur veut rechercher ou consulter des notifications de la messagerie interne.

**Modalités d’accès :**

à partir du menu "Messagerie interne"

**Critères de qualité (exigences) :**

Cette interface doit s'afficher dans un délai de moins de cinq secondes.  Elle doit respecter les règles du cadre d'application en vigueur.

**Aspects critiques de la performance :**

Importance faible.

**Fréquence d’activation :**

Plusieurs fois par jour

**Volume traité :**

Environ 10 notifications par jour

**Préconditions :**

**SO**

**Postconditions :**

La recherche a été effectuée et les notifications peuvent être consultées et supprimées (suppression pour chaque utilisateur)

###### 1.1.6.1.1 Diagramme APV161 Rechercher et consulter les notifications

<!-- image -->

Nom du diagramme :  APV161 Rechercher et consulter les notifications

Numéro de figure : 57

##### 1.1.6.2 «Service fonctionnel»  APV162 Produire et envoyer une notification

| Niveau complexité   |    |
|---------------------|----|

**Description :**

Ce service permet de créer une notification à partir d'un gabarit et des valeurs à remplacer dans le gabarit (spécifié dans les paramètres d'entrées).

Il permet de spécifier pour quelle la notification est produite

ne fois la notification crée, elle est automatiquement envoyée dans la messagerie interne.

**Mode d’automatisation :**

Service

**Complexité :**

**Paramètres :**

-

**Circonstances d’utilisation :**

- notifié l'ingénieur assigné à la demande lorsque celle-ci est modifiée dans GPM;

**Modalités d’accès :**

Appelé par différentes unités de tâches de APV qui doivent produire et envoyer une notification dans la messagerie interne.

**Critères de qualité (exigences) :**

Conforme aux normes d'un service

**Aspects critiques de la performance :**

Importance Faible.

**Fréquence d’activation :**

Plusieurs fois par jour.

**Volume traité :**

Environ 10 notifications par jour

**Préconditions :**

Un événement arrive sur une demande.

**Postconditions :**

La notification est produite et envoyée dans la messagerie interne.

##### 1.1.6.3 

|    |    |
|----|----|

###### 1.1.6.3.1 

<!-- image -->
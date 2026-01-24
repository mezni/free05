from transformers import pipeline

text1 = """
Le gouvernement français a annoncé aujourd'hui un nouveau plan économique visant à soutenir les petites entreprises.
Ce plan comprend des réductions d'impôts, des aides financières et des investissements dans l'innovation technologique.
Les experts estiment que ces mesures pourraient stimuler la croissance et réduire le chômage au cours des prochaines années.
"""

text = """
Cette unité de tâche permet de créer, modifier et supprimer un scénario.  Pour créer un scénario, l'UT copie toutes les informations de la demande originale ainsi que le parcours dans le cas d'une demande avec parcours, en excluant tous les résultats d'analyse.  Chaque scénario est identifié par une lettre, le premier commençant par A, le deuxième par B, etc.  À ce moment, l'ingénieur peut modifier les informations de la demande ou le parcours et déclencher le calcul des efforts de flexion et de cisaillement et l'analyse structurale des ponts.
Pour être en mesure de modifier le parcours, l'UT doit appeler l'UT "APV113 - Gérer un parcours sur une carte géographique"
Si dans le scénario, le parcours a été modifié, et que c'est ce scénario qui a été retenu, l’ingénieur devra refaire la modification du parcours dans la demande.  Le parcours modifié ne sera pas copié automatiquement.
Pour effectuer les calculs, l'UT doit faire appel aux UTs et services suivants:
- GPM_3_Calculer les efforts de flexion et de cisaillement d'un véhicule et leurs ratios
- APV128 Produire une analyse structurale des ponts
Les résultats du calcul des efforts et cisaillement sont affichés automatiquement dans l'interface du scénario.  Pour consulter les résultats d'analyse structurale, l'UT doit appeler l'UT "APV121 Consulter les résultats d'analyse", pour consulter les entraves, l'UT doit appeler l'UT "APV124 Consulter les entraves du parcours" et pour consulter le rapport d'expertise, l'UT doit appeler l'UT "APV132 Gérer le rapport d'expertise".
Tous les scénarios et leurs résultats d'analyse doivent être conservés et peuvent être consultés.  Ils sont reliés à la demande.  L'identifiant de l'historique doit être en lien avec le même no de version que celui de la demande.   Si un scénario est modifié, l'historique des modifications et des analyses n'est pas conservée.  Si l'ingénieur veut le conserver, il doit créer un nouveau scénario.
Le rapport d'expertise doit toujours être produit et conservé avec le scénario de la demande.
"""

# Use a model specifically fine-tuned for multilingual summarization
model_name = "csebuetnlp/mT5_multilingual_XLSum"

summarizer = pipeline(
    "summarization",
    model=model_name,
    tokenizer=model_name
)

# XL-Sum doesn't strictly require the "summarize: " prefix, 
# but it doesn't hurt to include it.
summary = summarizer(
    text, 
    max_length=60, 
    min_length=20, 
    do_sample=False
)

print(summary[0]["summary_text"])
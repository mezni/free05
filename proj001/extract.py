import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 1. Setup Model and Tokenizer with the fix
model_id = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

# Force 'eager' implementation to avoid the DynamicCache bug
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="auto", 
    torch_dtype="auto", 
    trust_remote_code=True,
    attn_implementation="eager" 
)

# 2. Create the pipeline using the loaded model
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

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

# Phi-3 works best with a chat-style prompt format
messages = [
    {"role": "user", "content": f"Extract the logical business rules from this French text as a Markdown list: {text}"},
]

# 3. Generate
# Note: For Phi-3, passing the message list to the pipeline is the modern way
output = pipe(messages, max_new_tokens=500, temperature=0.1)

print(output[0]['generated_text'])
# Table des Capacités de l'Agent IA

## Agent : first-responder

### Permissions (Actions Autorisées)

| Permission | Description |
|------------|-------------|
| `read_logs` | Lire les logs applicatifs depuis Loki |
| `read_metrics` | Lire les métriques depuis Prometheus |
| `propose_fix` | Proposer des correctifs pour résoudre les incidents |

### Actions Interdites

| Action | Raison |
|--------|--------|
| `delete_database` | Action destructive irréversible |
| `restart_production_server` | Impact production, nécessite validation humaine |
| `modify_credentials` | Sécurité critique, risque de compromission |

### Seuil d'Automatisation

- **Confiance requise** : ≥ 0.95 pour exécuter automatiquement
- **En dessous de 0.95** : approbation humaine obligatoire

### Workflow de Décision

```
1. Incident détecté (alerte Prometheus)
   ↓
2. Collecte de preuves (collect-evidence.sh)
   ↓
3. Analyse IA → réponse structurée (response.schema.json)
   ↓
4. Vérification du seuil de confiance
   ├─ confidence_score ≥ 0.95 → Action automatique (si dans permissions)
   └─ confidence_score < 0.95 → Approbation humaine requise
```

### Exemples d'Actions Autorisées

✅ **Autorisé** (confidence ≥ 0.95) :
- Analyser les logs d'erreur
- Identifier la cause racine
- Proposer un correctif (ex: redémarrer un service non-critique)

❌ **Interdit** (même avec confidence = 1.0) :
- Supprimer la base de données
- Redémarrer le serveur de production
- Modifier les credentials

### Format de Réponse Requis

L'agent doit toujours répondre selon le schéma JSON défini dans `incident-response/response.schema.json` :

```json
{
  "root_cause": "Description de la cause racine",
  "proposed_action": "Action corrective proposée",
  "confidence_score": 0.85,
  "requires_human_approval": true
}
```

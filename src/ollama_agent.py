import requests
import json
import pandas as pd
from typing import Dict, Any

class OllamaAgent:
    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        
    def _generate_response(self, prompt: str) -> str:
        """Sendet Anfrage an Ollama API"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()['response']
    
    def analyze_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Führt Datenanalyse mit Ollama durch"""
        # Basis-Statistiken erstellen
        basic_stats = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': df.columns.tolist(),
            'dtypes': {str(k): str(v) for k, v in df.dtypes.to_dict().items()},
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_summary': {
                col: df[col].describe().to_dict() 
                for col in df.select_dtypes(include=['int64', 'float64']).columns
            } if not df.empty else {}
        }
        
        # Analyse-Prompt erstellen
        # Analyse-Prompt für detaillierte Textanalyse
        analysis_prompt = f"""Als Data Science Experte, analysiere folgende Daten und antworte auf Deutsch:

Basis-Statistiken:
{json.dumps(basic_stats, indent=2)}

Bitte führe eine detaillierte Analyse durch und strukturiere deine Antwort in folgende Abschnitte:

1. Datenübersicht: Beschreibe die grundlegende Struktur und den Inhalt der Daten
2. Statistische Analyse: Erkläre wichtige statistische Merkmale und Auffälligkeiten
3. Datenqualität: Bewerte die Qualität und Vollständigkeit der Daten
4. Muster und Trends: Beschreibe erkennbare Muster oder Trends in den Daten

Gib eine ausführliche, gut strukturierte Analyse in natürlicher Sprache."""

        # Zusätzlicher Prompt für Empfehlungen im JSON-Format
        recommendations_prompt = f"""Basierend auf der vorherigen Analyse, erstelle konkrete Empfehlungen.

Antworte in folgendem JSON-Format:
{{
    'datenverarbeitung': [Liste von Empfehlungen zur Datenverarbeitung],
    'weitere_analysen': [Liste von vorgeschlagenen weiterführenden Analysen],
    'visualisierungen': [Liste von empfohlenen Visualisierungen],
    'actionable_insights': [Liste von konkreten Handlungsempfehlungen]
}}"""

        # Analyse durchführen
        analysis_result = self._generate_response(analysis_prompt)
        
        # Empfehlungen generieren
        recommendations_result = self._generate_response(recommendations_prompt)
        
        try:
            recommendations_dict = json.loads(recommendations_result)
        except json.JSONDecodeError:
            recommendations_dict = {
                'datenverarbeitung': ['Fehler beim Parsen der Empfehlungen'],
                'weitere_analysen': [],
                'visualisierungen': [],
                'actionable_insights': []
            }
            
        return {
            'basic_stats': basic_stats,
            'textanalyse': analysis_result,
            'empfehlungen': recommendations_dict
        }
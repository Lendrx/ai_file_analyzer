"""
Sammlung von Prompt-Templates für verschiedene Analysetypen.
"""

ANALYSIS_PROMPT = """
Analysiere den folgenden Text und erstelle eine strukturierte Zusammenfassung.
Berücksichtige dabei:
1. Hauptthemen
2. Wichtigste Aussagen
3. Schlüsselwörter
4. Ton und Stil

Text:
{content}

Strukurierte Analyse:
"""

CODE_REVIEW_PROMPT = """
Führe ein Code-Review für den folgenden Code durch.
Achte besonders auf:
1. Code-Qualität
2. Best Practices
3. Mögliche Verbesserungen
4. Potenzielle Bugs oder Sicherheitsprobleme

Code:
```python
{code}
```

Code-Review Ergebnis:
"""

SUMMARIZATION_PROMPT = """
Fasse den folgenden Text kurz und prägnant zusammen.
Behalte die wichtigsten Informationen bei und
strukturiere die Zusammenfassung klar.

Text:
{text}

Zusammenfassung:
"""

COMPARISON_PROMPT = """
Vergleiche die folgenden zwei Texte und
identifiziere Gemeinsamkeiten und Unterschiede.

Text 1:
{text1}

Text 2:
{text2}

Vergleichsanalyse:
"""
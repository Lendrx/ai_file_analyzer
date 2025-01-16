# Simple LLM File Analyzer with Ollama

Ein einfaches Python-Projekt, das zeigt, wie man lokale LLMs (Large Language Models) mit Ollama nutzt, um Dateien zu analysieren und zu verstehen.

## 🎯 Über das Projekt

Dieses Projekt demonstriert, wie man:
- Lokale LLMs mit Ollama einrichtet und verwendet
- Textdateien analysiert und zusammenfasst
- Mit verschiedenen Modellen interagiert
- Prompt Engineering in der Praxis anwendet

## 🚀 Schnellstart

1. Ollama installieren:
```bash
# macOS oder Linux
curl https://ollama.ai/install.sh | sh

# Für Windows, besuche:
# https://ollama.ai/download
```

2. Repository klonen:
```bash
git clone https://github.com/yourusername/simple-llm-analyzer.git
cd simple-llm-analyzer
```

3. Virtuelle Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Für Windows: venv\Scripts\activate
```

4. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

5. Modell herunterladen:
```bash
ollama pull mistral
```

## 📦 Projektstruktur

```
simple-llm-analyzer/
│
├── src/
│   ├── analyzer.py       # Hauptanalyseklasse
│   ├── prompts.py        # Prompt-Templates
│   └── utils.py          # Hilfsfunktionen
│
├── examples/
│   ├── text_analysis.py  # Beispiel für Textanalyse
│   └── code_review.py    # Beispiel für Code-Review
│
├── config/
│   └── config.yaml       # Konfigurationsdatei
│
└── README.md
```

## 💡 Beispiele

### Textanalyse
```python
from src.analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
result = analyzer.analyze_file("mein_dokument.txt")
print(result.summary)
```

### Code-Review
```python
from src.analyzer import CodeAnalyzer

analyzer = CodeAnalyzer(model="codellama")
feedback = analyzer.review_code("main.py")
print(feedback.suggestions)
```

## 🔧 Konfiguration

Die `config.yaml` erlaubt das Anpassen von:
- Verwendet LLM-Modell
- Maximale Tokenlänge
- Temperatur für Antworten
- Standardprompts

## 📚 Weiterführende Ressourcen

- [Ollama Dokumentation](https://ollama.ai/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai)
- [LangChain Dokumentation](https://python.langchain.com/docs/get_started/introduction.html)

## 🤝 Beitragen

Fühlen Sie sich frei, Issues zu erstellen oder Pull Requests einzureichen. Jeder Beitrag ist willkommen!

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE)
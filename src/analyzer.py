from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from .prompts import ANALYSIS_PROMPT, CODE_REVIEW_PROMPT

class BaseAnalyzer:
    """Basisklasse für verschiedene Analysetypen"""
    
    def __init__(self, model: str = "mistral", config_path: Optional[str] = None):
        """
        Initialisiert den Analyzer.
        
        Args:
            model: Name des Ollama-Modells
            config_path: Pfad zur Konfigurationsdatei
        """
        self.model = Ollama(model=model)
        self.config = self._load_config(config_path) if config_path else {}
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Lädt die Konfigurationsdatei"""
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

class DocumentAnalyzer(BaseAnalyzer):
    """Analyzer für Textdokumente"""
    
    def analyze_file(self, file_path: str) -> Dict[str, str]:
        """
        Analysiert eine Textdatei mit dem LLM.
        
        Args:
            file_path: Pfad zur Textdatei
            
        Returns:
            Dict mit Analyseergebnissen
        """
        # Datei einlesen
        content = Path(file_path).read_text(encoding='utf-8')
        
        # Prompt vorbereiten
        prompt = PromptTemplate(
            template=ANALYSIS_PROMPT,
            input_variables=["content"]
        )
        
        # Analyse durchführen
        result = self.model(prompt.format(content=content))
        
        return {
            "summary": result,
            "file_path": file_path,
            "model_used": self.model.model
        }

class CodeAnalyzer(BaseAnalyzer):
    """Analyzer für Code-Review"""
    
    def review_code(self, file_path: str) -> Dict[str, Any]:
        """
        Führt ein Code-Review mit dem LLM durch.
        
        Args:
            file_path: Pfad zur Code-Datei
            
        Returns:
            Dict mit Review-Ergebnissen
        """
        # Code einlesen
        code = Path(file_path).read_text(encoding='utf-8')
        
        # Prompt vorbereiten
        prompt = PromptTemplate(
            template=CODE_REVIEW_PROMPT,
            input_variables=["code"]
        )
        
        # Review durchführen
        result = self.model(prompt.format(code=code))
        
        return {
            "suggestions": result,
            "file_analyzed": file_path,
            "model_used": self.model.model
        }

    def suggest_improvements(self, code_snippet: str) -> str:
        """
        Schlägt Verbesserungen für ein Code-Snippet vor.
        
        Args:
            code_snippet: Der zu analysierende Code
            
        Returns:
            Verbesserungsvorschläge als String
        """
        prompt = """
        Analysiere den folgenden Code und schlage Verbesserungen vor:
        
        ```python
        {code}
        ```
        
        Fokussiere dich auf:
        1. Best Practices
        2. Performance
        3. Lesbarkeit
        4. Potenzielle Bugs
        """
        
        return self.model(prompt.format(code=code_snippet))
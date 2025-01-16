import os
import logging
from typing import Union, List, Dict, Any
import pandas as pd
import numpy as np
from pathlib import Path
import spacy
from spacy_langdetect import LanguageDetector

class FileUtils:
    """Hilfsfunktionen für Dateioperationen und Vorverarbeitung"""
    
    @staticmethod
    def detect_file_type(file_path: Union[str, Path]) -> str:
        """Erkennt den Dateityp und Encoding"""
        import magic
        
        file_type = magic.Magic(mime=True)
        return file_type.from_file(str(file_path))

    @staticmethod
    def get_file_metadata(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrahiert Metadaten aus der Datei"""
        file_stats = os.stat(file_path)
        return {
            "size": file_stats.st_size,
            "created": file_stats.st_ctime,
            "modified": file_stats.st_mtime,
            "accessed": file_stats.st_atime,
            "path": str(file_path),
            "extension": Path(file_path).suffix
        }

class TextPreprocessor:
    """Klasse für die Textvorverarbeitung"""
    
    def __init__(self):
        self.nlp = spacy.load("de_core_news_sm")
        self.nlp.add_pipe("language_detector")
        
    def preprocess_text(self, text: str, config: Dict) -> str:
        """Führt die Textvorverarbeitung durch"""
        if config.get("lowercase", True):
            text = text.lower()
            
        doc = self.nlp(text)
        
        if config.get("lemmatization", True):
            text = " ".join([token.lemma_ for token in doc])
            
        if config.get("remove_special_chars", True):
            text = "".join(char for char in text if char.isalnum() or char.isspace())
            
        return text
    
    def detect_language(self, text: str) -> str:
        """Erkennt die Sprache des Textes"""
        doc = self.nlp(text)
        return doc._.language["language"]

class DataFrameAnalyzer:
    """Erweiterte Analysefunktionen für DataFrames"""
    
    @staticmethod
    def analyze_correlations(df: pd.DataFrame, 
                           method: str = 'pearson',
                           threshold: float = 0.5) -> pd.DataFrame:
        """Analysiert Korrelationen zwischen numerischen Spalten"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr(method=method)
        
        # Filtere signifikante Korrelationen
        significant_corr = corr_matrix[abs(corr_matrix) > threshold]
        return significant_corr
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame,
                       columns: List[str] = None,
                       method: str = 'iqr') -> Dict[str, List[int]]:
        """Erkennt Ausreißer in numerischen Spalten"""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
            
        outliers = {}
        
        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outlier_indices = df[
                    (df[col] < (Q1 - 1.5 * IQR)) |
                    (df[col] > (Q3 + 1.5 * IQR))
                ].index.tolist()
            else:
                # Z-Score Methode
                z_scores = abs((df[col] - df[col].mean()) / df[col].std())
                outlier_indices = df[z_scores > 3].index.tolist()
                
            outliers[col] = outlier_indices
            
        return outliers

class VisualizationHelper:
    """Hilfsklasse für Datenvisualisierung"""
    
    @staticmethod
    def create_distribution_plot(data: pd.Series,
                               title: str = None,
                               bins: int = 30):
        """Erstellt einen Verteilungsplot"""
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        sns.histplot(data, bins=bins, kde=True)
        
        if title:
            plt.title(title)
        
        return plt
    
    @staticmethod
    def create_correlation_heatmap(corr_matrix: pd.DataFrame):
        """Erstellt eine Korrelations-Heatmap"""
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   fmt='.2f')
        
        return plt
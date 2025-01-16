from pathlib import Path
import pandas as pd
from typing import Union, Dict
from .ollama_agent import OllamaAgent

class FileProcessor:
    def __init__(self, agent: OllamaAgent):
        self.agent = agent
        
    def process_file(self, file_path: Union[str, Path]) -> Dict:
        """Verarbeitet eine einzelne Datei"""
        file_path = Path(file_path)
        
        # Datei einlesen
        try:
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Nicht unterstütztes Dateiformat: {file_path.suffix}")
        except Exception as e:
            return {
                'file_name': file_path.name,
                'error': f"Fehler beim Einlesen der Datei: {str(e)}"
            }
            
        # Analyse durchführen
        try:
            analysis_results = self.agent.analyze_data(df)
            
            # Textanalyse in .txt Datei speichern
            output_dir = Path('output')
            txt_output = output_dir / f"analyse_{file_path.stem}.txt"
            
            with open(txt_output, 'w', encoding='utf-8') as f:
                f.write(f"Analyse für: {file_path.name}\n")
                f.write(f"Zeitpunkt: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("=" * 80 + "\n\n")
                f.write("DATENANALYSE\n\n")
                f.write(analysis_results['textanalyse'])
            
            # JSON mit Empfehlungen und Basis-Statistiken zurückgeben
            return {
                'file_name': file_path.name,
                'status': 'success',
                'timestamp': pd.Timestamp.now().isoformat(),
                'basic_stats': analysis_results['basic_stats'],
                'empfehlungen': analysis_results['empfehlungen']
            }
        except Exception as e:
            return {
                'file_name': file_path.name,
                'status': 'error',
                'error': f"Fehler bei der Analyse: {str(e)}"
            }
import os
import json
import time
from pathlib import Path
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.ollama_agent import OllamaAgent
from src.file_processor import FileProcessor

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, processor: FileProcessor, output_dir: Path):
        self.processor = processor
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.processed_files = set()
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path in self.processed_files:
            return
            
        print(f"Neue Datei erkannt: {file_path}")
        
        try:
            # Datei verarbeiten
            results = self.processor.process_file(file_path)
            
            # Empfehlungen als JSON speichern
            recommendations_file = self.output_dir / f"empfehlungen_{file_path.stem}.json"
            with open(recommendations_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                
            # Pfade der erstellten Dateien anzeigen
            txt_file = self.output_dir / f"analyse_{file_path.stem}.txt"
            print(f"\nAnalyse gespeichert in:")
            print(f"- Textanalyse: {txt_file}")
            print(f"- Empfehlungen: {recommendations_file}")
            self.processed_files.add(file_path)
            
        except Exception as e:
            print(f"Fehler bei der Verarbeitung von {file_path}: {str(e)}")

def main():
    # Aktuelles Verzeichnis zum Projektverzeichnis machen
    os.chdir(Path(__file__).parent)
    
    # Konfiguration laden
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Ollama Agent initialisieren
    agent = OllamaAgent(
        model=config['model_settings']['model_name'],
        base_url=config['model_settings']['base_url']
    )
    processor = FileProcessor(agent)
    
    # Verzeichnisse erstellen
    watch_dir = Path(config['watch_directory'])
    output_dir = Path(config['output_directory'])
    watch_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Dateiwatcher einrichten
    event_handler = NewFileHandler(processor, output_dir)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()
    
    print(f"Überwache Verzeichnis: {watch_dir}")
    print(f"Ausgabeverzeichnis: {output_dir}")
    print(f"Drücken Sie Ctrl+C zum Beenden")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nBeende Überwachung...")
    observer.join()

if __name__ == "__main__":
    main()
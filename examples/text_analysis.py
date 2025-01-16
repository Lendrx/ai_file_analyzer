"""
Beispiel für die Verwendung des DocumentAnalyzer.
"""
from src.analyzer import DocumentAnalyzer

def main():
    # Analyzer initialisieren
    analyzer = DocumentAnalyzer(model="mistral")
    
    # Beispieltext in Datei schreiben
    with open("beispiel.txt", "w", encoding="utf-8") as f:
        f.write("""
        Machine Learning (ML) ist ein Teilgebiet der künstlichen Intelligenz. 
        Es bezeichnet das künstliche Generieren von Wissen aus Erfahrung: 
        Ein künstliches System lernt aus Beispielen und kann diese nach 
        Beendigung der Lernphase verallgemeinern.
        """)
    
    # Analyse durchführen
    result = analyzer.analyze_file("beispiel.txt")
    
    # Ergebnisse ausgeben
    print("\n=== Analyseergebnisse ===")
    print(f"\nZusammenfassung:\n{result['summary']}")
    print(f"\nVerwendetes Modell: {result['model_used']}")

if __name__ == "__main__":
    main()
"""
Beispiel für die Verwendung des CodeAnalyzer.
"""
from src.analyzer import CodeAnalyzer

def main():
    # Analyzer mit CodeLlama initialisieren
    analyzer = CodeAnalyzer(model="codellama")
    
    # Beispiel-Code für die Analyse
    code_snippet = """
def calculate_average(numbers):
    sum = 0
    for i in range(len(numbers)):
        sum += numbers[i]
    return sum / len(numbers)

# Liste mit Testwerten
test_numbers = [1, 2, 3, 4, 5]
average = calculate_average(test_numbers)
print(f"Der Durchschnitt ist: {average}")
    """
    
    # Code-Review durchführen
    suggestions = analyzer.suggest_improvements(code_snippet)
    
    # Ergebnisse ausgeben
    print("\n=== Code Review Ergebnisse ===")
    print(suggestions)

if __name__ == "__main__":
    main()
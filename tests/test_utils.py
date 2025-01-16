import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils import FileUtils, TextPreprocessor, DataFrameAnalyzer

@pytest.fixture
def sample_dataframe():
    """Erstellt einen Test-DataFrame"""
    return pd.DataFrame({
        'numeric': [1, 2, 3, 100, 4, 5],  # mit Ausreißer
        'text': ['Hello', 'World', 'Test', 'Sample', 'Data', 'Analysis'],
        'category': ['A', 'B', 'A', 'B', 'C', 'A']
    })

@pytest.fixture
def text_preprocessor():
    """Erstellt eine Instanz des TextPreprocessors"""
    return TextPreprocessor()

def test_file_utils_metadata():
    """Testet die Metadatenextraktion"""
    # Erstelle temporäre Testdatei
    test_file = Path('test_file.txt')
    test_file.write_text('Test content')
    
    metadata = FileUtils.get_file_metadata(test_file)
    
    assert isinstance(metadata, dict)
    assert 'size' in metadata
    assert 'created' in metadata
    assert metadata['extension'] == '.txt'
    
    # Cleanup
    test_file.unlink()

def test_text_preprocessing(text_preprocessor):
    """Testet die Textvorverarbeitung"""
    test_text = "Hello World! This is a Test."
    config = {
        "lowercase": True,
        "remove_special_chars": True
    }
    
    processed_text = text_preprocessor.preprocess_text(test_text, config)
    
    assert processed_text.islower()
    assert "!" not in processed_text
    assert "." not in processed_text

def test_outlier_detection(sample_dataframe):
    """Testet die Ausreißererkennung"""
    outliers = DataFrameAnalyzer.detect_outliers(
        sample_dataframe,
        columns=['numeric']
    )
    
    assert 'numeric' in outliers
    assert len(outliers['numeric']) > 0  # Sollte den Ausreißer (100) finden

def test_correlation_analysis(sample_dataframe):
    """Testet die Korrelationsanalyse"""
    # Füge eine korrelierte Spalte hinzu
    sample_dataframe['correlated'] = sample_dataframe['numeric'] * 2 + np.random.normal(0, 0.1, 6)
    
    correlations = DataFrameAnalyzer.analyze_correlations(
        sample_dataframe,
        threshold=0.5
    )
    
    assert isinstance(correlations, pd.DataFrame)
    assert correlations.loc['numeric', 'correlated'] > 0.9  # Sollte stark korreliert sein

if __name__ == '__main__':
    pytest.main([__file__])
import pytest
from src.calculator import calculate_tax_old_regime, calculate_tax_new_regime
from src.config import SYSTEM_PROMPT, GUARDRAIL_ERROR_MESSAGE
from src.styles import CUSTOM_CSS

def test_system_prompt_declaration():
    """
    Verifies system prompt is correctly declared and contains critical guardrail sentences.
    """
    assert "FinanceGuru" in SYSTEM_PROMPT
    assert "I apologize, but my expertise is strictly limited to Indian income tax, investments, and personal finance." in SYSTEM_PROMPT

def test_guardrail_error_message():
    """
    Ensures the guardrail error message matches requirements.
    """
    assert GUARDRAIL_ERROR_MESSAGE == "I apologize, but my expertise is strictly limited to Indian income tax, investments, and personal finance. I cannot assist with out-of-scope topics."

def test_tax_calculation_zero_income():
    """
    Verifies that zero income results in zero tax under both regimes.
    """
    assert calculate_tax_old_regime(0.0) == 0.0
    assert calculate_tax_new_regime(0.0) == 0.0

def test_tax_calculation_new_regime_rebate():
    """
    Verifies that taxable income under ₹7 Lakhs has 0 tax due to rebate under Section 87A (New Regime).
    Standard deduction is ₹75,000, so gross income up to ₹7.75 Lakhs should result in 0 tax.
    """
    assert calculate_tax_new_regime(700000.0) == 0.0
    assert calculate_tax_new_regime(775000.0) == 0.0

def test_tax_calculation_old_regime_rebate():
    """
    Verifies that taxable income under ₹5 Lakhs has 0 tax due to rebate (Old Regime).
    Standard deduction is ₹50,000, and standard 80C is ₹150,000, so gross income of ₹4.5 Lakhs should result in 0 tax.
    """
    assert calculate_tax_old_regime(450000.0) == 0.0

def test_tax_calculation_new_regime_slabs():
    """
    Test New Regime slab rates:
    Income = 15,000,000 (1.5 Crore)
    Check that calculations return correct values for large incomes.
    """
    tax_15l = calculate_tax_new_regime(1575000.0) # Taxable = 15L. Slabs: 3L-7L (20k), 7L-10L (30k), 10L-12L (30k), 12L-15L (60k) -> 140k + 4% cess = 145,600
    assert abs(tax_15l - 145600.0) < 0.01

def test_styles_sheet_contains_css():
    """
    Verifies that custom styling CSS sheet contains key design classes to prevent regressions.
    """
    assert ".stApp" in CUSTOM_CSS
    assert ".shimmer-text" in CUSTOM_CSS
    assert ".logo-container" in CUSTOM_CSS

def test_sanitize_csv_value():
    """
    Verifies that sanitize_csv_value properly escapes formula characters to mitigate CSV injection.
    """
    from src.gcp_services import sanitize_csv_value
    assert sanitize_csv_value("normal value") == "normal value"
    assert sanitize_csv_value("=SUM(A1:A5)") == "'=SUM(A1:A5)"
    assert sanitize_csv_value("+value") == "'+value"
    assert sanitize_csv_value("-value") == "'-value"
    assert sanitize_csv_value("@value") == "'@value"
    assert sanitize_csv_value("") == ""
    assert sanitize_csv_value(None) is None

def test_tax_calculation_negative_values():
    """
    Verifies that negative income results in zero tax under both regimes.
    """
    assert calculate_tax_old_regime(-1000.0) == 0.0
    assert calculate_tax_new_regime(-1000.0) == 0.0

def test_tax_calculation_old_regime_large_income():
    """
    Tests old regime calculation slabs for high incomes.
    For standard deductions (80C=150k, 80D=25k, Std=50k, total 225k ded),
    Income = 1,225,000 => Taxable = 1,000,000.
    Slabs: 2.5L-5L (12.5k), 5L-10L (100k) => 112.5k + 4% = 117,000
    """
    tax = calculate_tax_old_regime(1225000.0)
    assert abs(tax - 117000.0) < 0.01

def test_record_feedback_local_write(tmp_path, monkeypatch):
    """
    Tests that record_feedback writes logs securely to the CSV file.
    """
    import csv
    import os
    import src.gcp_services
    
    # Use monkeypatch to redirect feedback_log.csv to tmp_path
    test_csv = tmp_path / "feedback_log.csv"
    monkeypatch.setattr(src.gcp_services, "FEEDBACK_FILE_PATH", str(test_csv))
    
    src.gcp_services.record_feedback("=SUM(1,2)", "Check response", 5)
    
    assert test_csv.exists()
    with open(test_csv, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        # Header + 1 data row
        assert len(reader) == 2
        # Verify sanitization prefix is written
        assert reader[1][1] == "'=SUM(1,2)"




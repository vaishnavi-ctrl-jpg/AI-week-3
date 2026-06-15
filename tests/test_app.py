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

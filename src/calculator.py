def calculate_tax_old_regime(gross_salary: float, deductions_80c: float = 150000.0, deductions_80d: float = 25000.0) -> float:
    """
    Computes tax under the Old Regime for FY 2024-25.
    Standard deduction: ₹50,000
    """
    taxable_income = max(0.0, gross_salary - 50000.0 - deductions_80c - deductions_80d)
    
    tax = 0.0
    if taxable_income <= 250000:
        return 0.0
    
    # 5% Slab
    taxable_5 = min(250000.0, taxable_income - 250000.0)
    tax += taxable_5 * 0.05
    
    # 20% Slab
    if taxable_income > 500000:
        taxable_20 = min(500000.0, taxable_income - 500000.0)
        tax += taxable_20 * 0.20
        
    # 30% Slab
    if taxable_income > 1000000:
        taxable_30 = taxable_income - 1000000.0
        tax += taxable_30 * 0.30
        
    # Rebate under Section 87A (income up to ₹5 Lakhs)
    if taxable_income <= 500000:
        tax = 0.0
        
    # Health and Education Cess at 4%
    return tax * 1.04

def calculate_tax_new_regime(gross_salary: float) -> float:
    """
    Computes tax under the New Regime for FY 2024-25.
    Standard deduction: ₹75,000
    Slabs:
    Up to ₹3,000,000: Nil
    ₹3L to ₹7L: 5%
    ₹7L to ₹10L: 10%
    ₹10L to ₹12L: 15%
    ₹12L to ₹15L: 20%
    Above ₹15L: 30%
    Rebate under Section 87A for income up to ₹7 Lakhs
    """
    taxable_income = max(0.0, gross_salary - 75000.0)
    
    if taxable_income <= 300000:
        return 0.0
    
    tax = 0.0
    
    # 5% slab (300k - 700k)
    if taxable_income > 300000:
        slab_val = min(400000.0, taxable_income - 300000.0)
        tax += slab_val * 0.05
        
    # 10% slab (700k - 1000k)
    if taxable_income > 700000:
        slab_val = min(300000.0, taxable_income - 700000.0)
        tax += slab_val * 0.10
        
    # 15% slab (1000k - 1200k)
    if taxable_income > 1000000:
        slab_val = min(200000.0, taxable_income - 1000000.0)
        tax += slab_val * 0.15
        
    # 20% slab (1200k - 1500k)
    if taxable_income > 1200000:
        slab_val = min(300000.0, taxable_income - 1200000.0)
        tax += slab_val * 0.20
        
    # 30% slab (Above 1500k)
    if taxable_income > 1500000:
        slab_val = taxable_income - 1500000.0
        tax += slab_val * 0.30
        
    # Rebate under Section 87A (taxable income up to ₹7 Lakhs)
    if taxable_income <= 700000:
        tax = 0.0
        
    # Health and Education Cess at 4%
    return tax * 1.04

"""
Investment Risk Analysis using Apache Arrow
Analyzes portfolio risk metrics, VaR calculations, and risk exposure
"""
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as feather
from datetime import datetime, timedelta
import time


def generate_risk_data(num_positions=300_000):
    """Generate realistic risk analysis data"""
    print(f"Generating {num_positions:,} risk positions...")
    
    # Generate positions with risk characteristics
    data = {
        'position_id': range(1, num_positions + 1),
        'portfolio_id': np.random.randint(1, 5000, size=num_positions),
        'asset_type': np.random.choice(['Stock', 'Bond', 'Option', 'Future', 'Swap'], size=num_positions, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
        'region': np.random.choice(['US', 'EU', 'Asia', 'EM', 'Other'], size=num_positions, p=[0.4, 0.25, 0.2, 0.1, 0.05]),
        'currency': np.random.choice(['USD', 'EUR', 'GBP', 'JPY', 'CNY'], size=num_positions, p=[0.5, 0.2, 0.1, 0.1, 0.1]),
        'notional_value': np.random.uniform(10000, 10_000_000, size=num_positions).round(2),
        'market_value': np.random.uniform(10000, 10_000_000, size=num_positions).round(2),
    }
    
    # Calculate risk metrics
    # VaR (Value at Risk) - 95% confidence, 1-day
    data['var_1d_95'] = np.random.uniform(0.01, 0.05, size=num_positions) * data['market_value']
    
    # Expected Shortfall (Conditional VaR)
    data['expected_shortfall'] = data['var_1d_95'] * np.random.uniform(1.2, 1.5, size=num_positions)
    
    # Beta (market sensitivity)
    data['beta'] = np.random.uniform(0.3, 2.0, size=num_positions).round(2)
    
    # Volatility (annualized)
    data['volatility'] = np.random.uniform(0.10, 0.50, size=num_positions).round(4)
    
    # Credit rating
    credit_ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'D']
    data['credit_rating'] = np.random.choice(credit_ratings, size=num_positions, p=[0.1, 0.15, 0.2, 0.25, 0.15, 0.1, 0.04, 0.01])
    
    # Risk category
    data['risk_category'] = np.where(
        data['var_1d_95'] / data['market_value'] < 0.02, 'Low',
        np.where(data['var_1d_95'] / data['market_value'] < 0.04, 'Medium', 'High')
    )
    
    # Concentration risk (sector exposure)
    sectors = ['Tech', 'Finance', 'Energy', 'Healthcare', 'Consumer', 'Industrial']
    data['sector'] = np.random.choice(sectors, size=num_positions)
    
    # Liquidity score (1-10, higher = more liquid)
    data['liquidity_score'] = np.random.randint(1, 11, size=num_positions)
    
    return pd.DataFrame(data)


def calculate_portfolio_var(arrow_table):
    """Calculate portfolio-level VaR using Arrow compute"""
    # Simple VaR aggregation (assuming normal distribution)
    # In practice, you'd use more sophisticated methods
    
    # Get all VaR values
    var_values = arrow_table['var_1d_95'].to_numpy()
    
    # Portfolio VaR (square root of sum of squares for diversification effect)
    # Simplified calculation
    total_var = np.sqrt(np.sum(var_values ** 2))
    
    return total_var


def analyze_risk_with_arrow(df):
    """Perform comprehensive risk analysis using Apache Arrow"""
    print("\n" + "="*60)
    print("INVESTMENT RISK ANALYSIS")
    print("="*60)
    
    # Convert to Arrow Table
    start = time.time()
    arrow_table = pa.Table.from_pandas(df)
    conversion_time = time.time() - start
    print(f"\n✓ Converted to Arrow Table: {conversion_time:.4f} seconds")
    print(f"  Positions: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    
    # Convert to pandas for complex aggregations
    df_arrow = arrow_table.to_pandas()
    
    # 1. Portfolio Risk Overview
    print("\n1. PORTFOLIO RISK OVERVIEW")
    print("-" * 60)
    start = time.time()
    
    total_market_value = pc.sum(arrow_table['market_value']).as_py()
    total_var = calculate_portfolio_var(arrow_table)
    total_expected_shortfall = pc.sum(arrow_table['expected_shortfall']).as_py()
    avg_volatility = pc.mean(arrow_table['volatility']).as_py()
    avg_beta = pc.mean(arrow_table['beta']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Total Market Value: ${total_market_value:,.2f}")
    print(f"  Portfolio VaR (1-day, 95%): ${total_var:,.2f}")
    print(f"  VaR as % of Portfolio: {total_var/total_market_value*100:.2f}%")
    print(f"  Total Expected Shortfall: ${total_expected_shortfall:,.2f}")
    print(f"  Average Volatility: {avg_volatility*100:.2f}%")
    print(f"  Average Beta: {avg_beta:.2f}")
    
    # 2. Risk by Asset Type
    print("\n2. RISK EXPOSURE BY ASSET TYPE")
    print("-" * 60)
    start = time.time()
    
    asset_risk = df_arrow.groupby('asset_type').agg({
        'market_value': 'sum',
        'var_1d_95': 'sum',
        'volatility': 'mean',
        'beta': 'mean',
        'position_id': 'count'
    }).sort_values('var_1d_95', ascending=False)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Asset Type':<12} {'Market Value':>15} {'Total VaR':>12} {'Avg Vol':>10} {'Avg Beta':>10} {'Count':>8}")
    print("-" * 80)
    for asset_type, row in asset_risk.iterrows():
        var_pct = (row['var_1d_95'] / row['market_value'] * 100) if row['market_value'] > 0 else 0
        print(f"{asset_type:<12} ${row['market_value']:>14,.2f} ${row['var_1d_95']:>11,.2f} {row['volatility']*100:>9.2f}% {row['beta']:>9.2f} {row['position_id']:>8,}")
    
    # 3. Risk by Region
    print("\n3. RISK EXPOSURE BY REGION")
    print("-" * 60)
    start = time.time()
    
    region_risk = df_arrow.groupby('region').agg({
        'market_value': 'sum',
        'var_1d_95': 'sum',
        'volatility': 'mean',
        'position_id': 'count'
    }).sort_values('var_1d_95', ascending=False)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Region':<10} {'Market Value':>15} {'Total VaR':>12} {'Avg Vol':>10} {'Count':>8}")
    print("-" * 60)
    for region, row in region_risk.iterrows():
        var_pct = (row['var_1d_95'] / row['market_value'] * 100) if row['market_value'] > 0 else 0
        print(f"{region:<10} ${row['market_value']:>14,.2f} ${row['var_1d_95']:>11,.2f} {row['volatility']*100:>9.2f}% {row['position_id']:>8,}")
    
    # 4. Risk Category Distribution
    print("\n4. RISK CATEGORY DISTRIBUTION")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for filtering
    low_risk_mask = pc.equal(arrow_table['risk_category'], pa.scalar('Low'))
    medium_risk_mask = pc.equal(arrow_table['risk_category'], pa.scalar('Medium'))
    high_risk_mask = pc.equal(arrow_table['risk_category'], pa.scalar('High'))
    
    low_risk_table = pc.filter(arrow_table, low_risk_mask)
    medium_risk_table = pc.filter(arrow_table, medium_risk_mask)
    high_risk_table = pc.filter(arrow_table, high_risk_mask)
    
    low_risk_value = pc.sum(low_risk_table['market_value']).as_py()
    medium_risk_value = pc.sum(medium_risk_table['market_value']).as_py()
    high_risk_value = pc.sum(high_risk_table['market_value']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Low Risk:    ${low_risk_value:>15,.2f} ({low_risk_value/total_market_value*100:>5.2f}%) - {low_risk_table.num_rows:,} positions")
    print(f"  Medium Risk: ${medium_risk_value:>15,.2f} ({medium_risk_value/total_market_value*100:>5.2f}%) - {medium_risk_table.num_rows:,} positions")
    print(f"  High Risk:   ${high_risk_value:>15,.2f} ({high_risk_value/total_market_value*100:>5.2f}%) - {high_risk_table.num_rows:,} positions")
    
    # 5. Credit Risk Analysis
    print("\n5. CREDIT RISK BY RATING")
    print("-" * 60)
    start = time.time()
    
    credit_risk = df_arrow.groupby('credit_rating').agg({
        'market_value': 'sum',
        'var_1d_95': 'sum',
        'position_id': 'count'
    }).sort_values('market_value', ascending=False)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Rating':<10} {'Market Value':>15} {'Total VaR':>12} {'Count':>8}")
    print("-" * 50)
    for rating, row in credit_risk.iterrows():
        print(f"{rating:<10} ${row['market_value']:>14,.2f} ${row['var_1d_95']:>11,.2f} {row['position_id']:>8,}")
    
    # 6. High Risk Positions
    print("\n6. TOP 10 HIGHEST RISK POSITIONS")
    print("-" * 60)
    start = time.time()
    
    # Filter high risk positions
    high_risk_df = df_arrow[df_arrow['risk_category'] == 'High'].nlargest(10, 'var_1d_95')[
        ['position_id', 'asset_type', 'region', 'market_value', 'var_1d_95', 'volatility', 'beta']
    ]
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Pos ID':<10} {'Asset Type':<12} {'Region':<8} {'Value':>12} {'VaR':>12} {'Vol':>8} {'Beta':>8}")
    print("-" * 80)
    for _, row in high_risk_df.iterrows():
        print(f"{row['position_id']:<10} {row['asset_type']:<12} {row['region']:<8} ${row['market_value']:>11,.2f} ${row['var_1d_95']:>11,.2f} {row['volatility']*100:>7.2f}% {row['beta']:>7.2f}")
    
    # 7. Liquidity Risk Analysis
    print("\n7. LIQUIDITY RISK ANALYSIS")
    print("-" * 60)
    start = time.time()
    
    # Categorize by liquidity (using pandas for complex filtering)
    low_liq_df = df_arrow[df_arrow['liquidity_score'] < 5]
    medium_liq_df = df_arrow[(df_arrow['liquidity_score'] >= 5) & (df_arrow['liquidity_score'] < 8)]
    high_liq_df = df_arrow[df_arrow['liquidity_score'] >= 8]
    
    low_liq_value = low_liq_df['market_value'].sum()
    medium_liq_value = medium_liq_df['market_value'].sum()
    high_liq_value = high_liq_df['market_value'].sum()
    
    low_liq_count = len(low_liq_df)
    medium_liq_count = len(medium_liq_df)
    high_liq_count = len(high_liq_df)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Low Liquidity (<5):    ${low_liq_value:>15,.2f} ({low_liq_value/total_market_value*100:>5.2f}%) - {low_liq_count:,} positions")
    print(f"  Medium Liquidity (5-7): ${medium_liq_value:>15,.2f} ({medium_liq_value/total_market_value*100:>5.2f}%) - {medium_liq_count:,} positions")
    print(f"  High Liquidity (8+):   ${high_liq_value:>15,.2f} ({high_liq_value/total_market_value*100:>5.2f}%) - {high_liq_count:,} positions")
    
    # 8. Sector Concentration Risk
    print("\n8. SECTOR CONCENTRATION RISK")
    print("-" * 60)
    start = time.time()
    
    sector_concentration = df_arrow.groupby('sector').agg({
        'market_value': 'sum',
        'position_id': 'count'
    }).sort_values('market_value', ascending=False)
    sector_concentration['percentage'] = (sector_concentration['market_value'] / total_market_value * 100).round(2)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Sector':<12} {'Market Value':>15} {'Percentage':>12} {'Count':>8}")
    print("-" * 50)
    for sector, row in sector_concentration.iterrows():
        print(f"{sector:<12} ${row['market_value']:>14,.2f} {row['percentage']:>11.2f}% {row['position_id']:>8,}")
    
    # 9. Risk Statistics
    print("\n9. RISK STATISTICS")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for statistics
    var_mean = pc.mean(arrow_table['var_1d_95']).as_py()
    var_max = pc.max(arrow_table['var_1d_95']).as_py()
    var_min = pc.min(arrow_table['var_1d_95']).as_py()
    var_std = pc.stddev(arrow_table['var_1d_95']).as_py()
    
    vol_mean = pc.mean(arrow_table['volatility']).as_py()
    vol_max = pc.max(arrow_table['volatility']).as_py()
    
    beta_mean = pc.mean(arrow_table['beta']).as_py()
    beta_max = pc.max(arrow_table['beta']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  VaR Statistics:")
    print(f"    Mean: ${var_mean:,.2f}")
    print(f"    Max:  ${var_max:,.2f}")
    print(f"    Min:  ${var_min:,.2f}")
    print(f"    Std:  ${var_std:,.2f}")
    print(f"  Volatility Statistics:")
    print(f"    Mean: {vol_mean*100:.2f}%")
    print(f"    Max:  {vol_max*100:.2f}%")
    print(f"  Beta Statistics:")
    print(f"    Mean: {beta_mean:.2f}")
    print(f"    Max:  {beta_max:.2f}")
    
    # 10. Save to Feather
    print("\n10. SAVING TO FEATHER FORMAT")
    print("-" * 60)
    start = time.time()
    
    feather.write_feather(arrow_table, 'risk_data.feather')
    
    save_time = time.time() - start
    print(f"Saved to Feather: {save_time:.4f} seconds")
    print("  File: risk_data.feather")
    
    return arrow_table


if __name__ == "__main__":
    print("="*60)
    print("INVESTMENT RISK ANALYSIS")
    print("="*60)
    
    # Generate risk data
    df = generate_risk_data(num_positions=300_000)
    
    # Perform analysis
    arrow_table = analyze_risk_with_arrow(df)
    
    print("\n" + "="*60)
    print("RISK ANALYSIS COMPLETE")
    print("="*60)
    print("\nKey Benefits of Using Apache Arrow for Risk Analysis:")
    print("  ✓ Fast VaR calculations")
    print("  ✓ Efficient risk aggregation")
    print("  ✓ Real-time risk monitoring")
    print("  ✓ Scalable to millions of positions")
    print("  ✓ Zero-copy data sharing between systems")


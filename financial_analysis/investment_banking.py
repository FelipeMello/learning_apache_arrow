"""
Investment Banking Analysis using Apache Arrow
Analyzes portfolio performance, asset allocation, and investment metrics
"""
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as feather
from datetime import datetime, timedelta
import time


def generate_portfolio_data(num_holdings=500_000):
    """Generate realistic investment portfolio data"""
    print(f"Generating {num_holdings:,} portfolio holdings...")
    
    # Asset classes
    asset_classes = ['Equity', 'Bond', 'Commodity', 'Real Estate', 'Cash', 'Derivative']
    
    # Sectors
    sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer', 'Industrial', 'Utilities']
    
    # Generate portfolio data
    data = {
        'holding_id': range(1, num_holdings + 1),
        'client_id': np.random.randint(1, 10000, size=num_holdings),
        'asset_class': np.random.choice(asset_classes, size=num_holdings, p=[0.4, 0.25, 0.1, 0.1, 0.1, 0.05]),
        'sector': np.random.choice(sectors, size=num_holdings),
        'symbol': [f"STK{np.random.randint(1000, 9999)}" for _ in range(num_holdings)],
        'purchase_price': np.random.uniform(10, 500, size=num_holdings).round(2),
        'current_price': np.random.uniform(10, 500, size=num_holdings).round(2),
        'quantity': np.random.randint(10, 10000, size=num_holdings),
        'purchase_date': [
            datetime.now() - timedelta(days=np.random.randint(1, 3650))
            for _ in range(num_holdings)
        ],
    }
    
    # Calculate metrics
    data['cost_basis'] = data['purchase_price'] * data['quantity']
    data['current_value'] = data['current_price'] * data['quantity']
    data['unrealized_pnl'] = data['current_value'] - data['cost_basis']
    data['unrealized_pnl_percent'] = ((data['current_price'] - data['purchase_price']) / data['purchase_price'] * 100).round(2)
    
    # Add risk rating
    data['risk_rating'] = np.random.choice(['Low', 'Medium', 'High'], size=num_holdings, p=[0.3, 0.5, 0.2])
    
    return pd.DataFrame(data)


def analyze_portfolio_with_arrow(df):
    """Perform comprehensive portfolio analysis using Apache Arrow"""
    print("\n" + "="*60)
    print("INVESTMENT BANKING PORTFOLIO ANALYSIS")
    print("="*60)
    
    # Convert to Arrow Table
    start = time.time()
    arrow_table = pa.Table.from_pandas(df)
    conversion_time = time.time() - start
    print(f"\n✓ Converted to Arrow Table: {conversion_time:.4f} seconds")
    print(f"  Holdings: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    
    # Convert to pandas for complex aggregations
    df_arrow = arrow_table.to_pandas()
    
    # 1. Portfolio Overview
    print("\n1. PORTFOLIO OVERVIEW")
    print("-" * 60)
    start = time.time()
    
    total_cost_basis = pc.sum(arrow_table['cost_basis']).as_py()
    total_current_value = pc.sum(arrow_table['current_value']).as_py()
    total_unrealized_pnl = pc.sum(arrow_table['unrealized_pnl']).as_py()
    total_unrealized_pnl_percent = (total_unrealized_pnl / total_cost_basis * 100)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Total Cost Basis: ${total_cost_basis:,.2f}")
    print(f"  Total Current Value: ${total_current_value:,.2f}")
    print(f"  Total Unrealized P&L: ${total_unrealized_pnl:,.2f}")
    print(f"  Total Return: {total_unrealized_pnl_percent:.2f}%")
    
    # 2. Asset Class Allocation
    print("\n2. ASSET CLASS ALLOCATION")
    print("-" * 60)
    start = time.time()
    
    asset_allocation = df_arrow.groupby('asset_class').agg({
        'current_value': 'sum',
        'holding_id': 'count'
    }).sort_values('current_value', ascending=False)
    asset_allocation['percentage'] = (asset_allocation['current_value'] / total_current_value * 100).round(2)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    for asset_class, row in asset_allocation.iterrows():
        print(f"  {asset_class:15s}: ${row['current_value']:>15,.2f} ({row['percentage']:>5.2f}%) - {row['holding_id']:,} holdings")
    
    # 3. Sector Performance
    print("\n3. SECTOR PERFORMANCE")
    print("-" * 60)
    start = time.time()
    
    sector_performance = df_arrow.groupby('sector').agg({
        'unrealized_pnl': 'sum',
        'unrealized_pnl_percent': 'mean',
        'current_value': 'sum'
    }).sort_values('unrealized_pnl', ascending=False)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    for sector, row in sector_performance.iterrows():
        print(f"  {sector:15s}: P&L ${row['unrealized_pnl']:>12,.2f} | Avg Return {row['unrealized_pnl_percent']:>6.2f}% | Value ${row['current_value']:>12,.2f}")
    
    # 4. Top Performing Holdings
    print("\n4. TOP 10 PERFORMING HOLDINGS")
    print("-" * 60)
    start = time.time()
    
    top_performers = df_arrow.nlargest(10, 'unrealized_pnl')[['symbol', 'asset_class', 'sector', 'unrealized_pnl', 'unrealized_pnl_percent', 'current_value']]
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Symbol':<10} {'Asset Class':<15} {'Sector':<12} {'P&L':>12} {'Return %':>10} {'Value':>12}")
    print("-" * 80)
    for _, row in top_performers.iterrows():
        print(f"{row['symbol']:<10} {row['asset_class']:<15} {row['sector']:<12} ${row['unrealized_pnl']:>11,.2f} {row['unrealized_pnl_percent']:>9.2f}% ${row['current_value']:>11,.2f}")
    
    # 5. Worst Performing Holdings
    print("\n5. BOTTOM 10 PERFORMING HOLDINGS")
    print("-" * 60)
    start = time.time()
    
    worst_performers = df_arrow.nsmallest(10, 'unrealized_pnl')[['symbol', 'asset_class', 'sector', 'unrealized_pnl', 'unrealized_pnl_percent', 'current_value']]
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Symbol':<10} {'Asset Class':<15} {'Sector':<12} {'P&L':>12} {'Return %':>10} {'Value':>12}")
    print("-" * 80)
    for _, row in worst_performers.iterrows():
        print(f"{row['symbol']:<10} {row['asset_class']:<15} {row['sector']:<12} ${row['unrealized_pnl']:>11,.2f} {row['unrealized_pnl_percent']:>9.2f}% ${row['current_value']:>11,.2f}")
    
    # 6. Risk Distribution
    print("\n6. RISK DISTRIBUTION")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for filtering
    low_risk_mask = pc.equal(arrow_table['risk_rating'], pa.scalar('Low'))
    medium_risk_mask = pc.equal(arrow_table['risk_rating'], pa.scalar('Medium'))
    high_risk_mask = pc.equal(arrow_table['risk_rating'], pa.scalar('High'))
    
    low_risk_table = pc.filter(arrow_table, low_risk_mask)
    medium_risk_table = pc.filter(arrow_table, medium_risk_mask)
    high_risk_table = pc.filter(arrow_table, high_risk_mask)
    
    low_risk_value = pc.sum(low_risk_table['current_value']).as_py()
    medium_risk_value = pc.sum(medium_risk_table['current_value']).as_py()
    high_risk_value = pc.sum(high_risk_table['current_value']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Low Risk:    ${low_risk_value:>15,.2f} ({low_risk_value/total_current_value*100:>5.2f}%) - {low_risk_table.num_rows:,} holdings")
    print(f"  Medium Risk: ${medium_risk_value:>15,.2f} ({medium_risk_value/total_current_value*100:>5.2f}%) - {medium_risk_table.num_rows:,} holdings")
    print(f"  High Risk:   ${high_risk_value:>15,.2f} ({high_risk_value/total_current_value*100:>5.2f}%) - {high_risk_table.num_rows:,} holdings")
    
    # 7. Client Portfolio Summary
    print("\n7. TOP 10 CLIENT PORTFOLIOS BY VALUE")
    print("-" * 60)
    start = time.time()
    
    client_summary = df_arrow.groupby('client_id').agg({
        'current_value': 'sum',
        'unrealized_pnl': 'sum',
        'holding_id': 'count'
    }).sort_values('current_value', ascending=False).head(10)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"{'Client ID':<12} {'Portfolio Value':>18} {'Total P&L':>15} {'Holdings':>10}")
    print("-" * 60)
    for client_id, row in client_summary.iterrows():
        print(f"{client_id:<12} ${row['current_value']:>17,.2f} ${row['unrealized_pnl']:>14,.2f} {row['holding_id']:>10,}")
    
    # 8. Performance Statistics
    print("\n8. PERFORMANCE STATISTICS")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for statistics
    mean_return = pc.mean(arrow_table['unrealized_pnl_percent']).as_py()
    median_return = pc.median(arrow_table['unrealized_pnl_percent']).as_py()
    std_return = pc.stddev(arrow_table['unrealized_pnl_percent']).as_py()
    min_return = pc.min(arrow_table['unrealized_pnl_percent']).as_py()
    max_return = pc.max(arrow_table['unrealized_pnl_percent']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Mean Return:   {mean_return:>8.2f}%")
    print(f"  Median Return: {median_return:>8.2f}%")
    print(f"  Std Deviation: {std_return:>8.2f}%")
    print(f"  Min Return:    {min_return:>8.2f}%")
    print(f"  Max Return:    {max_return:>8.2f}%")
    
    # 9. Save to Feather
    print("\n9. SAVING TO FEATHER FORMAT")
    print("-" * 60)
    start = time.time()
    
    feather.write_feather(arrow_table, 'portfolio_data.feather')
    
    save_time = time.time() - start
    print(f"Saved to Feather: {save_time:.4f} seconds")
    print("  File: portfolio_data.feather")
    
    return arrow_table


if __name__ == "__main__":
    print("="*60)
    print("INVESTMENT BANKING PORTFOLIO ANALYSIS")
    print("="*60)
    
    # Generate portfolio data
    df = generate_portfolio_data(num_holdings=500_000)
    
    # Perform analysis
    arrow_table = analyze_portfolio_with_arrow(df)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nKey Benefits of Using Apache Arrow for Investment Banking:")
    print("  ✓ Fast portfolio calculations")
    print("  ✓ Efficient risk analysis")
    print("  ✓ Real-time performance metrics")
    print("  ✓ Scalable to millions of holdings")


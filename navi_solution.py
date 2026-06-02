import pandas as pd
import matplotlib.pyplot as plt

# --- Variables ---
INITIAL_PRICE = 0.0089 
DAILY_EMISSION = 1175514 
FARMER_SELL_RATE = 0.85 
DAILY_SELL_PRESSURE_TOKENS = DAILY_EMISSION * FARMER_SELL_RATE

DAILY_REVENUE_BUYBACK_USD = 8794 # ($3.21M Annual Profit / 365)

LIQUIDITY_POOL_USDC = 400000 
LIQUIDITY_POOL_NAVX = LIQUIDITY_POOL_USDC / INITIAL_PRICE
AMM_K = LIQUIDITY_POOL_USDC * LIQUIDITY_POOL_NAVX

days = 365
price_history_original = []
price_history_solution = []

# --- Original State ---
navx_in_pool_orig = LIQUIDITY_POOL_NAVX
usdc_in_pool_orig = LIQUIDITY_POOL_USDC

# --- Solution State ---
navx_in_pool_sol = LIQUIDITY_POOL_NAVX
usdc_in_pool_sol = LIQUIDITY_POOL_USDC

# --- Run Simulations ---
for day in range(days):
    # 1. Original Death Spiral
    navx_in_pool_orig += DAILY_SELL_PRESSURE_TOKENS
    usdc_in_pool_orig = AMM_K / navx_in_pool_orig
    price_history_original.append(usdc_in_pool_orig / navx_in_pool_orig)

    # 2. Proposed Solution (Buyback)
    # Farmers Dump
    navx_in_pool_sol += DAILY_SELL_PRESSURE_TOKENS
    usdc_in_pool_sol = AMM_K / navx_in_pool_sol
    
    # Protocol Buys Back with Daily Revenue
    usdc_in_pool_sol += DAILY_REVENUE_BUYBACK_USD
    navx_in_pool_sol = AMM_K / usdc_in_pool_sol
    
    price_history_solution.append(usdc_in_pool_sol / navx_in_pool_sol)

# --- Plot the Comparison ---
plt.figure(figsize=(10, 6))
plt.plot(range(days), price_history_original, color='red', label='Current dLP Model (Death Spiral)', linewidth=2)
plt.plot(range(days), price_history_solution, color='green', label='Proposed Real-Yield Buyback Model', linewidth=2)
plt.title("NAVI Protocol - Economic Survival vs Collapse Simulation")
plt.xlabel("Days from Today")
plt.ylabel("NAVX Price (USD)")
plt.axhline(y=INITIAL_PRICE, color='grey', linestyle='--', label=f'Current Price (${INITIAL_PRICE})')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('navx_solution_comparison.png')
print(f"Original Model Final Price: ${price_history_original[-1]:.6f}")
print(f"Proposed Model Final Price: ${price_history_solution[-1]:.6f}")
print("Graph saved as 'navx_solution_comparison.png'.")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- NAVI Protocol Initial State ---
INITIAL_PRICE = 0.0089 # Current NAVX Price
DAILY_EMISSION = 1175514 # Total NAVX unlocked per day
FARMER_SELL_RATE = 0.85 # Assume 85% of emitted tokens are instantly sold
DAILY_SELL_PRESSURE_TOKENS = DAILY_EMISSION * FARMER_SELL_RATE

# Assume a constant Liquidity Pool (LP) Depth for NAVX/USDC on DEXs
# A typical $7.3M Market Cap token has roughly $300k - $500k in actual DEX liquidity
LIQUIDITY_POOL_USDC = 400000 
LIQUIDITY_POOL_NAVX = LIQUIDITY_POOL_USDC / INITIAL_PRICE

# Constant Product AMM Formula (x * y = k)
AMM_K = LIQUIDITY_POOL_USDC * LIQUIDITY_POOL_NAVX

days = 365
price_history = []
navx_in_pool = LIQUIDITY_POOL_NAVX
usdc_in_pool = LIQUIDITY_POOL_USDC

# --- Run Simulation ---
for day in range(days):
    # Daily dump hits the liquidity pool
    navx_in_pool += DAILY_SELL_PRESSURE_TOKENS
    
    # Recalculate USDC in pool based on x * y = k
    usdc_in_pool = AMM_K / navx_in_pool
    
    # Calculate new price
    current_price = usdc_in_pool / navx_in_pool
    price_history.append(current_price)

# --- Plot the Death Spiral ---
plt.figure(figsize=(10, 6))
plt.plot(range(days), price_history, color='red', linewidth=2)
plt.title("NAVI Protocol (NAVX) - 365 Day Price Simulation (dLP Sell Pressure)")
plt.xlabel("Days from Today")
plt.ylabel("NAVX Price (USD)")
plt.grid(True, alpha=0.3)
plt.axhline(y=INITIAL_PRICE, color='grey', linestyle='--', label=f'Current Price (${INITIAL_PRICE})')
plt.legend()
plt.tight_layout()

# Save the graph
plt.savefig('navx_death_spiral.png')
print(f"Simulation complete. Price drops from ${INITIAL_PRICE} to ${price_history[-1]:.6f} in 365 days.")
print("Graph saved as 'navx_death_spiral.png'.")
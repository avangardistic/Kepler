# Project Goals

## Primary Goal
Demonstrate that three-body gravitational dynamics on L2 tick data
provide a descriptive language for HFT microstructure — not a trading
system, not a prediction model.

## Constraints (Immutable)
- Only raw L2 tick data allowed as input
- No external parameters, filters, indicators, or risk management
- No execution, no real money, no profit claims
- Time quantized in ticks
- All parameters derived internally from geometry

## Success Criteria
1. Angular momentum ‖L‖ remains bounded
2. Virial ratio T/V → −1/2
3. Π > 0 in mathematical expectation
4. Zero max drawdown (self-freeze)

## Anti-Goals
- Trading bot
- Signal generator
- Price prediction model
- Sellable strategy

# PortfolioAllocation
I'm trying to find an algorithm to solve the following (real-life) problem:

A customer has M
M
 amount of money each month that he wants to invest according to her preferred asset allocation. Example

60% stocks
20% bonds
20% REITs
She has a list of "favourite" financial instruments and a preferred allocation in each of the asset classes, e.g.:

Stocks: C (60%) and AAPL (40%)
Bonds: AGG (70%) and LQD (30%)
REITs: VNQI (100%)
Now, the algorithm would provide an investment advice (how many units and what financial instruments to buy) according to the following constraints:

Total sum of purchases with fees cannot exceed M
M
 (amount of money).
Units are integer and indivisible, you can buy either one or two stocks but not 1.5. Since the customer ivests small(-ish) sums, this constraint becomes important. Example: M
M
 is $500 and AAPL is $173 per unit!
Main goal is fee minimisation (again, since the sum invested is not large, fees become relatively large). Instruments have different fees that not flat-rate. E.g.: fees for buying C are "$1 if transaction sum is <$100, 0.30% otherwise", but for VNQI they're "$10 if sum < $2000, 0.40% otherwise".
Second goal is allocation that is approximately close to the "model allocation" above. Note that the model is concerned with asset classes, not individual instruments. That means the customer can buy only C or only AAPLto attain the desired 60% in Stocks. However, remember that there's also a preferred allocation within an asset class; if we decide not to buy C this month, then we'll need buy more of it next time to keep the stocks in balance.
Fee minimisation can be attained by limiting the number of transactions. That means we can decide to buy, e.g., C, AGG and VNQI only, and think about buying AAPL and LQD next month. We can go even further and decide not to buy a whole asset class at all if the first solution has fees that are too high (above some pre-determined limit). In that case we'll remember that decision and buy more of it next month.

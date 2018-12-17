# Investment advisor.
# Copyright (C) 2018  Alexander Ivashkin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def calc_total_cost(assetsToBuy, assetsBuying):
    tot_sum = 0
    for ass, cnt in zip(assetsToBuy, assetsBuying):
        tot_sum += ass[1] * cnt
    return tot_sum

iterations = 0
isDebug = True

def buy_an_asset(assetsToBuy, moneyLeft):
    minAssetsBuying = []
    minMoneyLeft = moneyLeft
    global iterations
    iterations += 1

    global isDebug
    if isDebug: print("fun called with: ", assetsToBuy, moneyLeft)

    currAsset = assetsToBuy[0]
    if len(assetsToBuy) == 1:
        return [int(moneyLeft / currAsset[1])]
    leftAssetsToBuy = assetsToBuy[1:]
    if isDebug: print("leftAssetsToBuy: ", leftAssetsToBuy)

    for currAssetCount in range(0, int(moneyLeft / currAsset[1]) + 1):
        currMoneyLeft = moneyLeft - currAssetCount * currAsset[1]
        currAssetsBuying = buy_an_asset(leftAssetsToBuy, currMoneyLeft)
        if isDebug: print("   after recursion: currAssetsBuying:", currAssetsBuying)
        currMoneyLeft -= calc_total_cost(leftAssetsToBuy, currAssetsBuying)
        if isDebug: print("   currMoneyLeft: ", currMoneyLeft)
        if isDebug: print("   minMoneyLeft: ", minMoneyLeft)

        if currMoneyLeft < minMoneyLeft:
            minMoneyLeft = currMoneyLeft
            minAssetsBuying = [currAssetCount] + currAssetsBuying
            if isDebug: print("        Found local min: minMoneyLeft: ", minMoneyLeft)
            if isDebug: print("        minAssetsBuying: ", minAssetsBuying)

    returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + currAssetsBuying
    if isDebug: print("Exiting fun. Will return minAssetsBuying: ", returnValue)
    return returnValue


ass = [("LQD", 2.5, 0.02), ("SCHA", 2.15, 0.02), ("S&P", 2.77, 0.01), ("C", 3.95, 0.01), ("AAPL", 1.73, 0.01)]
cash = 10
buying = buy_an_asset(ass, cash)
cashUsed = calc_total_cost(ass, buying)
print("Will buy: ")
for a, c in zip(ass, buying):
    print("   ", c, " of ", a[0], "@", a[1])
print("Total cost: ", cashUsed)
print("Money left: ", cash - cashUsed)
print("Calculated in ", iterations, " iterations")

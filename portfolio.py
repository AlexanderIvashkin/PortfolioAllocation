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


def calc_sum_bought(assetsToBuy, assetsBuying):
    tot_sum = 0
    for ass, cnt in zip(assetsToBuy, assetsBuying):
        tot_sum += ass[1] * cnt
    return tot_sum

def calc_fee(asset, cnt):
    return max(asset[2] * cnt * asset[1], asset[3])

def calc_sum_fees(assetsToBuy, assetsBuying):
    fees = 0
    for ass, cnt in zip(assetsToBuy, assetsBuying):
        fees += calc_fee(ass, cnt)
    return fees

iterations = 0
isDebug = False
isUseCache = True
cacheHits = 0
cacheMisses = 0
memo = {}

def buy_an_asset(assetsToBuy, moneyLeft):
    global memo
    global cacheHits
    global cacheMisses
    if isUseCache:
        cacheLkp = ""
        for ass in assetsToBuy:
            cacheLkp += "{0},{1}/".format(ass[0], moneyLeft) 

        if cacheLkp in memo:
            cacheHits += 1
            return memo[cacheLkp]

        cacheMisses += 1

    minAssetsBuying = []
    minMoneyLeft = moneyLeft
    minFees = moneyLeft
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

        if isUseCache:
            cacheLkp = ""
            for ass in leftAssetsToBuy:
                cacheLkp += "{0},{1}/".format(ass[0], currMoneyLeft) 
            memo[cacheLkp] = currAssetsBuying

        if isDebug: print("   after recursion: currAssetsBuying:", currAssetsBuying)

        currMoneyLeft -= calc_sum_bought(leftAssetsToBuy, currAssetsBuying)
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


if __name__ == '__main__':
    ass = [("LQD", 2.5, 0.01, 1), ("SCHA", 2.01, 0.01, 1), ("S&P", 0.91, 0.01, 1), ("C", 9.9, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    print(ass)
    cash = 150
    buying = buy_an_asset(ass, cash)
    cashUsed = calc_sum_bought(ass, buying)
    print("Will buy: ")
    for a, c in zip(ass, buying):
        print("   ", c, " of ", a[0], "@", a[1])
    print("Total cost: ", cashUsed)
    print("Money left: ", cash - cashUsed)
    print("Total fees: ", calc_sum_fees(ass, buying))
    print("Calculated in ", iterations, " iterations")
    if isUseCache:
        print("Cache size ", len(memo))
        print("Cache hits ", cacheHits)
        print("Cache misses ", cacheMisses)

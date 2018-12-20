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

import timeit

def calc_sum_bought(assetsToBuy, assetsBuying):
    tot_sum = 0
    #print("Got: {0}, {1}".format(assetsToBuy, assetsBuying))
    for ass, cnt in zip(assetsToBuy, assetsBuying):
        #print("ass: {0}, cnt: {1}".format(ass, cnt))
        tot_sum += ass[1] * cnt
    return tot_sum

def calc_fee(asset, cnt):
    return 0 if cnt == 0 else max(asset[2] * cnt * asset[1], asset[3])

def calc_sum_fees(assetsToBuy, assetsBuying):
    fees = 0
    for ass, cnt in zip(assetsToBuy, assetsBuying):
        fees += calc_fee(ass, cnt)
    return fees

def calc_bought_w_fees(assetsToBuy, assetsBuying):
    return calc_sum_fees(assetsToBuy, assetsBuying) + calc_sum_bought(assetsToBuy, assetsBuying)

iterations = 0
iterSavedByBacktrack = 0
isDebug = False

def buy_an_asset(assetsToBuy, moneyLeft):
    minAssetsBuying = []
    minMoneyLeft = moneyLeft
    minFees = moneyLeft
    global iterations
    iterations += 1

    global isDebug
    if isDebug: print("fun called with: ", assetsToBuy, moneyLeft)

    currAsset = assetsToBuy[0]
    cnt = 0
    if len(assetsToBuy) == 1:
        maxCnt = int(moneyLeft / currAsset[1])
        cnt = maxCnt
        fee = calc_fee(currAsset, cnt)
        cost = calc_sum_bought([currAsset], [cnt]) 
        while cnt >= 0 and fee + cost > moneyLeft:
            cnt -= 1
            fee = calc_fee(currAsset, cnt)
            cost = calc_sum_bought([currAsset], [cnt]) 
            # print("Count: {4}, Fee: {0}, cost: {1}, fee+cost: {2}, money left: {3}".format(fee, cost, fee + cost, moneyLeft, cnt))
        # print(cnt)
        return [cnt]

    leftAssetsToBuy = assetsToBuy[1:]
    if isDebug: print("leftAssetsToBuy: ", leftAssetsToBuy)

    for currAssetCount in range(0, int(moneyLeft / currAsset[1]) + 1):
        currMoneyLeft = moneyLeft - calc_bought_w_fees([currAsset], [currAssetCount])
        if currMoneyLeft > 0:
            if leftAssetsToBuy[0][1] + leftAssetsToBuy[0][3] > currMoneyLeft:
                global iterSavedByBacktrack
                iterSavedByBacktrack += len(leftAssetsToBuy)
                currAssetsBuying = minAssetsBuying if minAssetsBuying != [] else [currAssetCount]
            else:
                currAssetsBuying = buy_an_asset(leftAssetsToBuy, currMoneyLeft)
                if isDebug: print("   after recursion: currAssetsBuying:", currAssetsBuying)
                currMoneyLeft -= calc_bought_w_fees(leftAssetsToBuy, currAssetsBuying)
                if isDebug: print("   currMoneyLeft: ", currMoneyLeft)
                if isDebug: print("   minMoneyLeft: ", minMoneyLeft)

                if currMoneyLeft >= 0 and currMoneyLeft < minMoneyLeft:
                    minMoneyLeft = currMoneyLeft
                    minAssetsBuying = [currAssetCount] + currAssetsBuying
                    if isDebug: print("        Found local min: minMoneyLeft: ", minMoneyLeft)
                    if isDebug: print("        minAssetsBuying: ", minAssetsBuying)

    returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + currAssetsBuying
    if isDebug: print("Exiting fun. Will return minAssetsBuying: ", returnValue)
    return returnValue


if __name__ == '__main__':
    #ass = [("LQD", 2.5, 0.01, 1), ("SCHA", 2.01, 0.01, 1), ("S&P", 0.91, 0.01, 1), ("C", 9.9, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    ass = [("LQD", 1, 0.01, 1), ("SCHA", 2, 0.01, 1), ("S&P", 1, 0.01, 1), ("C", 10, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    print(ass)
    cash = 150
    buying = buy_an_asset(ass, cash)
    cashUsed = calc_bought_w_fees(ass, buying)
    print("Will buy: ")
    for a, c in zip(ass, buying):
        print("   ", c, " of ", a[0], "@", a[1])
    print("Total cost: {0:2}".format(cashUsed))
    print("Money left: ", cash - cashUsed)
    print("Total fees: ", calc_sum_fees(ass, buying))
    print("Calculated in ", iterations, " iterations")
    print("Saved {0} iterations by backtracking!".format(iterSavedByBacktrack))

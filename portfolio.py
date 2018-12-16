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

minAssetsBuying = []
minMoneyLeft = -1

def buy_an_asset(assetsToBuy, moneyLeft):
    global minAssetsBuying
    global minMoneyLeft

    print("fun called with: ", assetsToBuy, moneyLeft)

    if minMoneyLeft < 0: minMoneyLeft = moneyLeft
    #print("Starting fun; minMoneyLeft: ", minMoneyLeft)

    currAsset = assetsToBuy[0]
    if len(assetsToBuy) == 1:
        return [int(moneyLeft / currAsset[1])]
    leftAssetsToBuy = assetsToBuy[1:]
    #print("leftAssetsToBuy: ", leftAssetsToBuy)

    isLocalMin = False

    for currAssetCount in range(0, int(moneyLeft / currAsset[1]) + 1):
        currMoneyLeft = moneyLeft - currAssetCount * currAsset[1]
        currAssetsBuying = buy_an_asset(leftAssetsToBuy, currMoneyLeft)
        print("   after recursion: currAssetsBuying:", currAssetsBuying)
        currMoneyLeft -= calc_total_cost(leftAssetsToBuy, currAssetsBuying)
        print("   currMoneyLeft: ", currMoneyLeft)
        print("   minMoneyLeft: ", minMoneyLeft)

        if currMoneyLeft < minMoneyLeft:
            minMoneyLeft = currMoneyLeft
            minAssetsBuying = [currAssetCount] + currAssetsBuying
            isLocalMin = True
            print("Found local min: minMoneyLeft: ", minMoneyLeft)
            print("minAssetsBuying: ", minAssetsBuying)

    print("Exiting fun. Will return minAssetsBuying: ", minAssetsBuying if isLocalMin else [])
    return minAssetsBuying if isLocalMin else []



#print("Before calling: ", minAssetsBuying)
buy_an_asset([("LQD", 2.5, 0.02), ("SCHA", 2, 0.02), ("S&P", 3, 0.01)], 10)
print("Min assets: ", minAssetsBuying)
#print("After fun: ", minAssetsBuying)
#print("Total sum: ", calc_total_cost([("LQD", 2.5, 0.02), ("SCHA", 2, 0.02), ("S&P", 3, 0.01)], [10, 0, 0]))

#print(buy_an_asset([("S&P", 3, 0.01)], 3.5))

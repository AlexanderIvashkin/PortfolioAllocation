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


def buy_an_asset(assetsToBuy, moneyLeft):
    currAsset = assetsToBuy[0]
    if len(assetsToBuy) == 1:
        return [int(moneyLeft/currAsset[1])]

    leftAssets = assetsToBuy[1:]
    minMoneyLeft = moneyLeft

    for currAssCount in range(0, int(moneyLeft/currAsset[1])):
        currMoneyLeft = moneyLeft - currAsset[1] * currAssCount
        assetsBuying = [currAssCount] + buy_an_asset(leftAssets, currMoneyLeft)
        if len(assetsBuying) == 0:
            return []
        currMoneyLeft = moneyLeft
        for i in range(len(assetsBuying)):
            currMoneyLeft = currMoneyLeft - assetsToBuy[i][1] * assetsBuying[i]
        if currMoneyLeft < minMoneyLeft:
            return assetsBuying
        else:
            return[]


        print("Buying ", currAssCount, " of ", currAsset[0], " at ", currAsset[1], " for ", currAsset[1] * currAssCount)
        print("Buying ", nextAssCount, " of ", nextAsset[0], " at ", nextAsset[1], " for ", nextAsset[1] * nextAssCount)
        print("Leftover money: ", currMoneyLeft)
        
        if currMoneyLeft < minMoneyLeft:
            minMoneyLeft = currMoneyLeft
            print("Found minMoneyLeft!")


print(buy_an_asset([("LQD", 2.5, 0.02), ("SCHA", 2, 0.02), ("S&P", 3, 0.01)], 10))

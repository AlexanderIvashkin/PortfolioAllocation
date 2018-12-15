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


def buy_an_asset(assetsToBuy, moneyLeft, assetID = 0):
    currAsset = assetsToBuy[assetID]
    if assetID + 1 == len(assetsToBuy):
        return moneyLeft//currAsset[1]

    nextAsset = assetsToBuy[-1]

    for currAssCount in range(0, moneyLeft//currAsset[1]):
        currMoneyLeft = moneyLeft - currAsset[1] * currAssCount
        nextAssCount = buy_an_asset(assetsToBuy, currMoneyLeft, assetID + 1)
        print("Buying ", currAssCount, " of ", currAsset[0], " at ", currAsset[1])
        print("Buying ", nextAssCount, " of ", nextAsset[0], " at ", nextAsset[1])
        print("Leftover money: ", currMoneyLeft - nextAsset[1] * nextAssCount)


buy_an_asset([("SCHA", 2, 0.02), ("S&P", 3, 0.01)], 10)

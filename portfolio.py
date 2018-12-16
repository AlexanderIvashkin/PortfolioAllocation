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


minAssetsBuying = []

def buy_an_asset(assetsToBuy, moneyLeft, minMoneyLeft = -1):
    global minAssetsBuying
    minAssetsBuying += assetsToBuy[0]
    print("Inside fun: ", minAssetsBuying)
    return minAssetsBuying


print("Before calling: ", minAssetsBuying)
print(buy_an_asset([("LQD", 2.5, 0.02), ("SCHA", 2, 0.02), ("S&P", 3, 0.01)], 10))
print("After fun: ", minAssetsBuying)

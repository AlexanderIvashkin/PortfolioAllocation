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
isDebug = False
_solutionsFound = 0
_wML = 1
_wMF = 1
_wPA = 1
_minFees = 0

def buy_an_asset(assetsToBuy, moneyLeft):
    minAssetsBuying = []
    minMoneyLeft = moneyLeft
    global iterations
    iterations += 1

    global isDebug
    if isDebug: print("fun called with: ", assetsToBuy, moneyLeft)

    currAsset = assetsToBuy[0]

    # The base case
    if len(assetsToBuy) == 1:# {{{
        maxCnt = int((moneyLeft - currAsset[3]) / currAsset[1])
        if maxCnt == 0:
            return [0]
        cnt = maxCnt
        fee = calc_fee(currAsset, cnt)
        cost = calc_sum_bought([currAsset], [cnt]) 
        while cnt > 0 and fee + cost > moneyLeft:
            cnt -= 1
            fee = calc_fee(currAsset, cnt)
            cost = calc_sum_bought([currAsset], [cnt]) 
            # print("Count: {4}, Fee: {0}, cost: {1}, fee+cost: {2}, money left: {3}".format(fee, cost, fee + cost, moneyLeft, cnt))
        # print(cnt)
        return [cnt]# }}}

    leftAssetsToBuy = assetsToBuy[1:]
    if isDebug: print("leftAssetsToBuy: ", leftAssetsToBuy)

    # Will add this to the minimums to relax the constraint
    addML = (1 - _wML) * moneyLeft
    addMF = (1 - _wMF) * moneyLeft

    timesToCycle = int((moneyLeft - currAsset[3]) / currAsset[1])
    timesToCycle = timesToCycle + 1 if timesToCycle >= 0 else 1
    for currAssetCount in range(0, timesToCycle):
        currMoneyLeft = moneyLeft - calc_bought_w_fees([currAsset], [currAssetCount])
        if currMoneyLeft >= 0:
            # import pdb; pdb.set_trace()
            currAssetsBuying = buy_an_asset(leftAssetsToBuy, currMoneyLeft)
            if isDebug: print("   after recursion: currAssetsBuying:", currAssetsBuying)
            currMoneyLeft -= calc_bought_w_fees(leftAssetsToBuy, currAssetsBuying)
            if isDebug: print("   currMoneyLeft: ", currMoneyLeft)
            if isDebug: print("   minMoneyLeft: ", minMoneyLeft)
            currFees = calc_sum_fees([currAsset] + leftAssetsToBuy, [currAssetCount] + currAssetsBuying)

            global _minFees
            if currMoneyLeft >= 0 and currMoneyLeft <= minMoneyLeft + addML and currFees <= _minFees + addMF:
                global _solutionsFound
                _solutionsFound += 1
                minMoneyLeft = currMoneyLeft
                _minFees = currFees
                minAssetsBuying = [currAssetCount] + currAssetsBuying
                if isDebug: print("        Found local min: minMoneyLeft: ", minMoneyLeft)
                if isDebug: print("        minAssetsBuying: ", minAssetsBuying)

            returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + currAssetsBuying
        else:
            returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + [0 for x in leftAssetsToBuy]

    if isDebug: print("Exiting fun. Will return minAssetsBuying: ", returnValue)
    return returnValue

def allocate_assets(assetsToBuy, moneyLeft, wML=1, wMF=1, wPA=1):
    """
    Find the best allocation of assets.
    assetsToBuy: a list of tuples with assets (format TBD)
    moneyLeft: a value of money we can use
    wML: weight of "Min money left" solution where 1 is "No leeway" and 0 is "I don't care about this"
    wMF: weight of "Min fees" solution
    wPA: weight of "Perfect Allocation" solution
    """
    
    global _wML
    global _wMF
    global _wPA
    _wML = wML
    _wMF = wMF
    _wPA = wPA

    global _minFees
    _minFees = moneyLeft

    ### Check for "no solutions found"
    result = buy_an_asset(assetsToBuy, moneyLeft)
    return result if _solutionsFound > 0 else []


if __name__ == '__main__':
    #ass = [("LQD", 2.5, 0.01, 1), ("SCHA", 2.01, 0.01, 1), ("S&P", 0.91, 0.01, 1), ("C", 9.9, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    ass = [("LQD", 2, 0.01, 1), ("SCHA", 2, 0.01, 1), ("S&P", 1, 0.01, 1), ("C", 10, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    #ass = [("A", 4, 0, 0), ("A", 4, 0, 0)]
    weights = [1, 1, 1]
    cash = 100
    print("Allocating: ", ass)
    print("Cash available: {:}".format(cash))
    print("Weights: MinMoneyLeft: {:5.3f}, MinFees: {:5.3f}, PerfectAllocation: {:5.3f}".format(*weights))
    buying = allocate_assets(ass, cash, *weights)
    cashUsed = calc_bought_w_fees(ass, buying)
    print("Will buy: ")
    for a, c in zip(ass, buying):
        print("   {0:4d} of {1:6} @ {2:8.2f} (total: {3:8.2f}, fees: {4:6.2f})".format(c, a[0], a[1], c * a[1], calc_fee(a, c)))
    print("Total cost: ", cashUsed)
    print("Money left: ", cash - cashUsed)
    print("Total fees: ", calc_sum_fees(ass, buying))
    print("Calculated in ", iterations, " iterations")
    print("Solutions found: {:}".format(_solutionsFound))

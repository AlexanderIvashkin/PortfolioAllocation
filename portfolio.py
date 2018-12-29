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

from math import sqrt

# Custom errors
class NonPositivePrices(ValueError):
    """All prices must be larger than zero"""

class NegativeFees(ValueError):
    """All fees must be positive"""

class TooLittleCash(ValueError):
    """Can't buy even one security"""

class DuplicateAssetTickers(ValueError):
    """Duplicate asset tickers found"""

class WrongConstraintWeights(ValueError):
    """Invalid weights for constraints"""

class NonPositiveCash(ValueError):
    """You can't buy anything with negative money!"""

class WrongModelAllocation(ValueError):
    """Assets allocations don't add up to 100%"""


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

def calc_sum_bought_w_fees(assetsToBuy, assetsBuying):
    return calc_sum_fees(assetsToBuy, assetsBuying) + calc_sum_bought(assetsToBuy, assetsBuying)

def calc_allocation_distance(assetsToBuy, assetsBuying):
    """
    Calculate distance from the ideal allocation where 0 is the best (min. distance).
    Distance is SQRT(sum-squares).
    """
    totSum = calc_sum_bought_w_fees(assetsToBuy, assetsBuying)
    alloDist = 0
    if totSum > 0:
        for ass, cnt in zip(assetsToBuy, assetsBuying):
            alloDist += (ass[4] - (calc_sum_bought_w_fees([ass], [cnt]) / totSum) ) ** 2
    else:
        for ass, cnt in zip(assetsToBuy, assetsBuying):
            alloDist += ass[4] ** 2
    
    return sqrt(alloDist / len(assetsToBuy))



def calc_sol_distance(assetsToBuy, sol, moneyLeft, wML = 1, wMF = 1, wPA = 1):
    """
    Calculate distance (from the ideal solution)
    """
    # Max ML is moneyLeft (i.e. we don't buy anything)
    # Min ML is zero
    # distML is in range of 0-1
    if wML == 0:
        distML = 0
    else:
        distML = (moneyLeft - calc_sum_bought_w_fees(assetsToBuy, sol)) / moneyLeft * wML
    # Max MF is moneyLeft (i.e. we pay the max amount of fees)
    # Min MF is zero
    # distMF is in range of 0-1
    if wMF == 0:
        distMF = 0
    else:
        distMF = calc_sum_fees(assetsToBuy, sol) / moneyLeft * wMF

    if wPA == 0:
        distPA = 0
    else:
        distPA = calc_allocation_distance(assetsToBuy, sol) * wPA

    return sqrt(distMF ** 2 + distML ** 2 + distPA ** 2)


iterations = 0
isDebug = False
_solutionsFound = 0
_bestSolutionsFound = 0
_solutions = []
_lenAss = 0
_wML = 1
_wMF = 1
_wPA = 1
_minFees = 0
_addML = 0
_addMF = 0
_mulPA = 1
_localMinFound = 0

def buy_an_asset(assetsToBuy, moneyLeft):
    minAssetsBuying = []# {{{
    _minPA = 100
    minMoneyLeft = moneyLeft
    global iterations
    iterations += 1

    global isDebug
    if isDebug: print("fun called with: ", assetsToBuy, moneyLeft)

    currAsset = assetsToBuy[0]

    # The base case
    if len(assetsToBuy) == 1:# {{{
        maxCnt = int((moneyLeft - currAsset[3]) / currAsset[1])
        #print("maxCnt: {}".format(maxCnt))
        if maxCnt == 0:
            return [0]
        cnt = maxCnt
        fee = calc_fee(currAsset, cnt)
        cost = calc_sum_bought([currAsset], [cnt]) 
        #print("fee + cost: {}, will 'while': {}".format(fee + cost, cnt > 0 and fee + cost > moneyLeft))
        while cnt > 0 and fee + cost > moneyLeft:
            cnt -= 1
            fee = calc_fee(currAsset, cnt)
            cost = calc_sum_bought([currAsset], [cnt]) 
            # print("Count: {4}, Fee: {0}, cost: {1}, fee+cost: {2}, money left: {3}".format(fee, cost, fee + cost, moneyLeft, cnt))
        # print(cnt)
        return [cnt]# }}}

    leftAssetsToBuy = assetsToBuy[1:]
    if isDebug: print("leftAssetsToBuy: ", leftAssetsToBuy)

    timesToCycle = int((moneyLeft - currAsset[3]) / currAsset[1])
    timesToCycle = timesToCycle + 1 if timesToCycle >= 0 else 1
    for currAssetCount in range(0, timesToCycle):
        currMoneyLeft = moneyLeft - calc_sum_bought_w_fees([currAsset], [currAssetCount])
        if currMoneyLeft >= 0:
            # import pdb; pdb.set_trace()
            currAssetsBuying = buy_an_asset(leftAssetsToBuy, currMoneyLeft)
            if isDebug: print("   after recursion: currAssetsBuying:", currAssetsBuying)
            currMoneyLeft -= calc_sum_bought_w_fees(leftAssetsToBuy, currAssetsBuying)
            currFees = calc_sum_fees([currAsset] + leftAssetsToBuy, [currAssetCount] + currAssetsBuying)
            currPA = calc_allocation_distance([currAsset] + leftAssetsToBuy, [currAssetCount] + currAssetsBuying)

            global _minFees
            #global _minPA
            global _addML
            global _addMF
            global _mulPA
            if isDebug: print("   currMoneyLeft: {}".format(currMoneyLeft))
            if isDebug: print("   minMoneyLeft: {}, +addML: {}".format(minMoneyLeft, minMoneyLeft + _addML))
            if isDebug: print("   currPA: {:6.3f}, *mulPA: {:6.3f}".format(currPA, currPA * _mulPA))
            if isDebug: print("   minPA: {:6.3f}".format(_minPA))

            if currMoneyLeft >= 0 and currMoneyLeft <= minMoneyLeft + _addML and currFees <= _minFees + _addMF and currPA * _mulPA <= _minPA:

                global _localMinFound
                _localMinFound += 1
                global _lenAss
                if len(assetsToBuy) == _lenAss:
                    minMoneyLeft = currMoneyLeft
                    minAssetsBuying = [currAssetCount] + currAssetsBuying
                    _minFees = currFees
                    _minPA = currPA
                    global _solutionsFound
                    _solutionsFound += 1
                    global _solutions
                    _solutions += [minAssetsBuying]

                if isDebug: print("        Found local min: minMoneyLeft: ", minMoneyLeft)
                if isDebug: print("        minAssetsBuying: ", minAssetsBuying)

            returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + currAssetsBuying
        else:
            returnValue = minAssetsBuying if minAssetsBuying != [] else [currAssetCount] + [0 for x in leftAssetsToBuy]

    if isDebug: print("Exiting fun. Will return minAssetsBuying: ", returnValue)
    return returnValue# }}}


def allocate_assets(assetsToBuy, moneyLeft, wML=1, wMF=1, wPA=1):
    """# {{{
    Find the best allocation of assets.
    assetsToBuy: a list of tuples with assets (format TBD)
    moneyLeft: a value of money we can use
    wML: weight of "Min money left" solution where 1 is "No leeway" and 0 is "I don't care about this"
    wMF: weight of "Min fees" solution
    wPA: weight of "Perfect Allocation" solution
    """
    
    if not (0 <= wML <= 1 and 0 <= wMF <= 1 and 0 <= wPA <= 1):
        raise WrongConstraintWeights

    global _wML
    global _wMF
    global _wPA
    _wML = wML
    _wMF = wMF
    _wPA = wPA

    # Will add this to the minimums to relax the constraint
    global _addML
    global _addMF
    global _mulPA
    _addML = (1 - _wML) * moneyLeft
    _addMF = (1 - _wMF) * moneyLeft
    _mulPA = _wPA

    global _minFees
    _minFees = moneyLeft
    global _lenAss
    _lenAss = len(assetsToBuy)

    #global _minPA
    # YES, that's an arbitrary number. However, it's impossible (?) to reach it so should be safe.
    # VERY, very bad idea.
    #_minPA = 100


    if moneyLeft <= 0:
        raise NonPositiveCash

    _pricesPosit = [c[1] > 0 for c in assetsToBuy]
    if not all(_pricesPosit):
        raise NonPositivePrices

    _feesPosit = [f[2] >= 0 and f[3] >= 0 for f in assetsToBuy]
    if not all(_feesPosit):
        raise NegativeFees

    _cantBuySome = [calc_sum_bought_w_fees([a], [1]) > moneyLeft for a in assetsToBuy]
    if any(_cantBuySome):
        raise TooLittleCash

    _sumPA = 0
    for ass in assetsToBuy:
        _sumPA += ass[4]

    if _sumPA != 1:
        raise WrongModelAllocation

    global _solutionsFound
    _solutionsFound = 0
    global _solutions
    _solutions = []
    global _bestSolutionsFound
    result = buy_an_asset(assetsToBuy, moneyLeft)

    if len(assetsToBuy) > 1 and _solutionsFound > 0:
        # print("Solutions: {}".format(len(_solutions)))
        #print(_solutions)
        minSolutionDis = calc_sol_distance(assetsToBuy, _solutions[0], moneyLeft, wML, wMF, wPA)
        bestSolution = _solutions[0]
        #_bestSolutionsFound = 1
        #print("Starting Sol distance: {:5.3f}, solution: {}".format(minSolutionDis, bestSolution))
        for sol in _solutions:
            currSolDis = calc_sol_distance(assetsToBuy, sol, moneyLeft, wML, wMF, wPA)
            #print("Current Sol distance: {:5.3f}, solution: {}".format(currSolDis, sol))
            if currSolDis < minSolutionDis:
                minSolutionDis = currSolDis
                bestSolution = sol
                #print("Best solution found: {}, minSolutionDis: {:5.3f}".format(bestSolution, minSolutionDis))
                #_bestSolutionsFound += 1

        return bestSolution
    else:
        if len(assetsToBuy) == 1:
            _solutionsFound = 1
            return result
        else:
            return []
# }}}


if __name__ == '__main__':
    # ass = [("VNQI", 3.5, 0.01, 1), ("LQD", 2.5, 0.01, 1), ("SCHA", 2.01, 0.01, 1), ("S&P", 0.91, 0.01, 1), ("C", 9.9, 0.01, 1), ("AAPL", 1.1, 0.1, 1)]
    #ass = [("LQD", 2, 0.01, 1, 0.1), ("SCHA", 2, 0.01, 1, 0.2), ("S&P", 1, 0.01, 1, 0.5), ("C", 10, 0.01, 1, 0.1), ("AAPL", 1.1, 0.1, 1, 0.1)]
    #ass = [("A", 5, 0, 0)]
    #ass = [("A", 5, 0, 0, .1), ("C", 5, 0, 0, .4), ("AAPL", 6, 0, 0, .5)]
    # ass = [("ETFDAX", 426.70, 0.0039, 3, .25), ("ETFW20L", 273.00, 0.0039, 3, .25), ("ETFSP500", 94.50, 0.0039, 3, .5)]
    ass = [("SCHA", 226.30, 0.0029, 38, .15), ("VNQI", 196.76, 0.0029, 38, .10), ("LQD", 422.80, 0.0029, 38, .15), ("ETFDAX", 426.70, 0.0039, 3, .15), ("ETFW20L", 273.00, 0.0039, 3, .15), ("ETFSP500", 94.50, 0.0039, 3, .3)]
    weights = [.0, 1, .0]
    cash = 5331.60
    print("Allocating: ", ass)
    print("Cash available: {:}".format(cash))
    print("Weights: MinMoneyLeft: {:5.3f}, MinFees: {:5.3f}, PerfectAllocation: {:5.3f}".format(*weights))
    buying = allocate_assets(ass, cash, *weights)

    if _solutionsFound > 0:
        cashUsed = calc_sum_bought_w_fees(ass, buying)
        print("Will buy: ")
        for a, c in zip(ass, buying):
            print("   {0:4d} of {1:8} @ {2:8.2f} (total: {3:8.2f}, fees: {4:6.2f}). Allocation: {5:5.2%} (ideal: {6:5.2%}).".format(c, a[0], a[1], c * a[1], calc_fee(a, c), c * a[1] / cashUsed, a[4]))
        print("Total cost: {:8.2f}".format(cashUsed))
        print("Money left: {:8.2f}".format(cash - cashUsed))
        print("Total fees: {:8.2f}".format(calc_sum_fees(ass, buying)))
        print("Calculated in ", iterations, " iterations")
        print("Solutions found: {:}".format(_solutionsFound))
        print(_solutions)
        #print("Best solutions found: {:}".format(_bestSolutionsFound))
    else:
        print("NO solutions found!")
        print("_localMinFound: {}".format(_localMinFound))

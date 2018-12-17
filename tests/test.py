import unittest
import portfolio

class UnitTestsCase(unittest.TestCase):

    def test_buyNothing(self):
        self.assertTrue(portfolio.buy_an_asset([("A", 5, 0)], 4) == [0])
        self.assertTrue(portfolio.buy_an_asset([("A", 5, 0), ("A", 5, 0)], 4) == [0, 0])
        self.assertTrue(portfolio.buy_an_asset([("A", 5, 0), ("A", 5, 0), ("A", 5, 0)], 4) == [0, 0, 0])
        self.assertTrue(portfolio.buy_an_asset([("A", 4.000001, 0), ("A", 4.1, 0), ("A", 4.000000000001, 0)], 4) == [0, 0, 0])
        self.assertTrue(portfolio.buy_an_asset([("A", 101, 0)], 100) == [0])

    def test_buyOneAssetClass(self):
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0)], 4) == [1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0)], 7) == [1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0)], 7.9999999999999) == [1])
        self.assertTrue(portfolio.buy_an_asset([("A", 3.99, 0)], 7.9999999999999) == [2])
        self.assertTrue(portfolio.buy_an_asset([("A", 666, 0)], 666) == [1])
        self.assertTrue(portfolio.buy_an_asset([("A", 666, 0)], 667) == [1])
        self.assertTrue(portfolio.buy_an_asset([("A", 1, 0)], 666) == [666])
        self.assertTrue(portfolio.buy_an_asset([("A", 1, 0)], 6660) == [6660])

    def test_buySome(self):
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 4, 0)], 4) == [0,1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 4, 0)], 40) == [0,10])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 5, 0)], 4) == [1,0])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 5, 0)], 6) == [0,1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 5, 0)], 10) == [0,2])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 5, 0)], 9) == [1,1])
        self.assertTrue(portfolio.buy_an_asset([("A", 1, 0), ("A", 1.1, 0)], 666) == [281,350])

    def test_buyMany(self):
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 4, 0), ("A", 4, 0), ("A", 5, 0)], 9) == [0,0,1,1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 2, 0), ("A", 6, 0), ("A", 7, 0)], 15.7) == [0,1,1,1])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 6, 0), ("A", 4, 0), ("A", 5, 0)], 15) == [0,0,0,3])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 60, 0), ("A", 40, 0), ("A", 50, 0)], 15) == [3,0,0,0])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 6, 0), ("A", 4, 0), ("A", 5, 0)], 100) == [0,0,0,20])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 6, 0), ("A", 4, 0), ("A", 5.1, 0)], 100) == [0,0,25,0])
        self.assertTrue(portfolio.buy_an_asset([("A", 4, 0), ("A", 6, 0), ("A", 4.1, 0), ("A", 5.1, 0)], 100) == [0,0,2,18])
        self.assertTrue(portfolio.buy_an_asset([("A", 1, 0), ("A", 1, 0), ("A", 1, 0), ("A", 4, 0)], 100) == [0,0,0,25])

if __name__ == '__main__':
    unittest.main()

import unittest
import portfolio

class UnitTestsCase(unittest.TestCase):

    def test_calcFee(self):
        self.assertTrue(portfolio.calc_fee(("A", 5, 0.01, 1), 4) == 1)
        self.assertTrue(portfolio.calc_fee(("A", 5, 0.01, 1), 40) == 2)
        self.assertTrue("{:.3f}".format(portfolio.calc_fee(("A", 25.25, 0.01, 1), 10)) == "2.525")


    def test_buyNothing(self):
        self.assertTrue(portfolio.allocate_assets([("A", 5, 0, 0)], 4) == [0])
        self.assertTrue(portfolio.allocate_assets([("A", 5, 0, 0), ("A", 5, 0, 0)], 4) == [0, 0])
        self.assertTrue(portfolio.allocate_assets([("A", 5, 0, 0), ("A", 5, 0, 0), ("A", 5, 0, 0)], 4) == [0, 0, 0])
        self.assertTrue(portfolio.allocate_assets([("A", 4.000001, 0, 0), ("A", 4.1, 0, 0), ("A", 4.000000000001, 0, 0)], 4) == [0, 0, 0])
        self.assertTrue(portfolio.allocate_assets([("A", 101, 0, 0)], 100) == [0])

    def test_buyOneAssetClass(self):
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0)], 4) == [1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0)], 7) == [1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0)], 7.9999999999999) == [1])
        self.assertTrue(portfolio.allocate_assets([("A", 3.99, 0, 0)], 7.9999999999999) == [2])
        self.assertTrue(portfolio.allocate_assets([("A", 666, 0, 0)], 666) == [1])
        self.assertTrue(portfolio.allocate_assets([("A", 666, 0, 0)], 667) == [1])
        self.assertTrue(portfolio.allocate_assets([("A", 1, 0, 0)], 666) == [666])
        self.assertTrue(portfolio.allocate_assets([("A", 1, 0, 0)], 6660) == [6660])

    def test_buySome(self):
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0)], 4) == [0,1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0)], 40) == [0,10])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 4) == [1,0])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 6) == [0,1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 10) == [0,2])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 9) == [1,1])
        self.assertTrue(portfolio.allocate_assets([("A", 1, 0, 0), ("A", 1.1, 0, 0)], 666) == [6,600])

    def test_buyMany(self):
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 9) == [0,0,1,1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 2, 0, 0), ("A", 6, 0, 0), ("A", 7, 0, 0)], 15.7) == [0,1,1,1])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 15) == [0,0,0,3])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 60, 0, 0), ("A", 40, 0, 0), ("A", 50, 0, 0)], 15) == [3,0,0,0])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 100) == [0,0,0,20])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5.1, 0, 0)], 100) == [0,16,1,0])
        self.assertTrue(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4.1, 0, 0), ("A", 5.1, 0, 0)], 100) == [0,0,2,18])

    def test_buyDeep(self):
        self.assertTrue(portfolio.allocate_assets([("A", 1, 0, 0), ("A", 1, 0, 0), ("A", 1, 0, 0), ("A", 4, 0, 0)], 120) == [0,0,0,30])
        print("   Iterations: ", portfolio.iterations)
        # self.assertTrue(portfolio.iterations == 310124)

if __name__ == '__main__':
    unittest.main()

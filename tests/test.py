import unittest
import portfolio

class UnitTestsCase(unittest.TestCase):

    def test_calcFee(self):
        self.assertEqual(portfolio.calc_fee(("A", 5, 0.01, 1), 4), 1)
        self.assertEqual(portfolio.calc_fee(("A", 5, 0.01, 1), 40), 2)
        self.assertEqual("{:.3f}".format(portfolio.calc_fee(("A", 25.25, 0.01, 1), 10)), "2.525")
        self.assertEqual(portfolio.calc_fee(("A", 1, 0, 10), 1), 10)

    def test_calc_bought_w_fees(self):
        self.assertEqual(portfolio.calc_sum_bought_w_fees([("A", 1, 0, 10)], [1]), 11)

    def test_buyOneAssetClass(self):
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0)], 4), [1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0)], 7), [1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0)], 7.9999999999999), [1])
        self.assertEqual(portfolio.allocate_assets([("A", 3.99, 0, 0)], 7.9999999999999), [2])
        self.assertEqual(portfolio.allocate_assets([("A", 666, 0, 0)], 666), [1])
        self.assertEqual(portfolio.allocate_assets([("A", 666, 0, 0)], 667), [1])
        self.assertEqual(portfolio.allocate_assets([("A", 1, 0, 0)], 666), [666])
        self.assertEqual(portfolio.allocate_assets([("A", 1, 0, 0)], 6660), [6660])

    def test_buySome(self):
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0)], 4), [0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0)], 40), [0,10])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0)], 4), [0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 6), [0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 10), [0,2])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 9), [1,1])
        self.assertEqual(portfolio.allocate_assets([("A", 1, 0, 0), ("A", 1.1, 0, 0)], 666), [6,600])

    def test_buyMany(self):
        ass = portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 9)
        with self.subTest(assets = ass):
            self.assertEqual(ass, [0,1,0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 9), [0,1,0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 2, 0, 0), ("A", 6, 0, 0), ("A", 7, 0, 0)], 15.7), [0,4,0,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 15), [0,1,1,1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 11.1, 0, 0), ("A", 11.1, 0, 0), ("A", 11.1, 0, 0)], 15), [3,0,0,0])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5, 0, 0)], 100), [0,16,1,0])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4, 0, 0), ("A", 5.1, 0, 0)], 100), [0,16,1,0])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4.1, 0, 0), ("A", 5.1, 0, 0)], 100), [0,9,5,5])

    @unittest.skip("too much time to calculate")
    def test_buyDeep(self):
        self.assertEqual(portfolio.allocate_assets([("A", 1, 0, 0), ("A", 1, 0, 0), ("A", 1, 0, 0), ("A", 4, 0, 0)], 120), [120,0,0,0])
        print("   Iterations: ", portfolio.iterations)
        # self.assertEqual(portfolio.iterations, 310124)

    def test_buySomeRelax(self):
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 0)], 9, 1, .9), [1, 1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 1)], 10, .9, 1), [1, 1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 1)], 10, .5, 1), [1, 1])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 1)], 11, .9, 1), [0, 2])
        self.assertEqual(portfolio.allocate_assets([("A", 4, 0, 0), ("A", 5, 0, 1)], 11, .3, 1), [0, 2])


    def test_calcDistStrictML(self):
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 0)], [1, 1], 9), 0)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 0)], [0, 1], 9), 4/9)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 0)], [1, 0], 9), 5/9)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 0)], [0, 0], 9), 1)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4.1, 0, 0), ("A", 5.1, 0, 0)], [25,0,0,0], 100), 0)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4.1, 0, 0), ("A", 5.1, 0, 0)], [24,0,0,0], 100), 4/100)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("A", 6, 0, 0), ("A", 4.1, 0, 0), ("A", 5.1, 0, 0)], [0,0,0,0], 100), 1)

    def test_calcDistStrictMF(self):
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 1)], [1, 1], 10), 0.1)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 1, 0, 8)], [1, 1], 13), 8/13)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 9, 0, 0)], [0, 1], 9), 0)

    def test_calcDistRelaxedML(self):
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 5, 0, 0)], [1, 1], 9, .5), 0)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 4, 0, 0)], [1, 1], 9, .5), 1 / 9 * .5)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 4, 0, 0)], [1, 1], 9, .1), 1 / 9 * .1)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 0), ("C", 4, 0, 0)], [1, 1], 9, 0), 0)

    def test_calcDistRelaxedMF(self):
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 1), ("C", 5, 0, 0)], [1, 1], 10, 1, 0), 0)
        self.assertEqual(portfolio.calc_sol_distance([("A", 4, 0, 1), ("C", 5, 0, 0)], [1, 1], 10, 1, .5), .05)

    def test_nonpositive_prices(self):
        with self.assertRaises(portfolio.NonPositivePrices):
            portfolio.allocate_assets([("A", 0, 0, 0), ("A", 5, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NonPositivePrices):
            portfolio.allocate_assets([("A", 0, 0, 0), ("A", 0, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NonPositivePrices):
            portfolio.allocate_assets([("A", -1, 0, 0), ("A", 0, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NonPositivePrices):
            portfolio.allocate_assets([("A", 1, 0, 0), ("A", -1, 0, 0)], 9, .9, .9)

    def test_negative_fees(self):
        with self.assertRaises(portfolio.NegativeFees):
            portfolio.allocate_assets([("A", 1, -1, 0), ("A", 5, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NegativeFees):
            portfolio.allocate_assets([("A", 1, 1, -1), ("A", 5, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NegativeFees):
            portfolio.allocate_assets([("A", 1, 1, 1), ("A", 5, -1, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.NegativeFees):
            portfolio.allocate_assets([("A", 1, 1, 1), ("A", 5, 1, -1)], 9, .9, .9)

    def test_too_little_cash(self):
        with self.assertRaises(portfolio.TooLittleCash):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 9, .9, .9)
        with self.assertRaises(portfolio.TooLittleCash):
            portfolio.allocate_assets([("A", 1, 0, 10), ("A", 5, 0, 10)], 9, .9, .9)
        with self.assertRaises(portfolio.TooLittleCash):
            portfolio.allocate_assets([("A", 1, 0, 1), ("A", 5, 0, 10)], 9, .9, .9)
        with self.assertRaises(portfolio.TooLittleCash):
            portfolio.allocate_assets([("A", 1, 0, 1), ("A", 5, 1, 0)], 9, .9, .9)


    def test_nonpositive_cash(self):
        with self.assertRaises(portfolio.NonPositiveCash):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 0, .9, .9)
        with self.assertRaises(portfolio.NonPositiveCash):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], -1, .9, .9)


    def test_weird_weights(self):
        with self.assertRaises(portfolio.WrongConstraintWeights):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 20, 9, .9)
        with self.assertRaises(portfolio.WrongConstraintWeights):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 20, -9, .9)
        with self.assertRaises(portfolio.WrongConstraintWeights):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 20, .9, .9, -666)
        with self.assertRaises(portfolio.WrongConstraintWeights):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 20, .9, .9, 666)
        with self.assertRaises(portfolio.WrongConstraintWeights):
            portfolio.allocate_assets([("A", 10, 0, 0), ("A", 15, 0, 0)], 20, 9)




if __name__ == '__main__':
    unittest.main()

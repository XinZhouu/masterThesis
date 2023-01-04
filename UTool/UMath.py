import decimal

class mathUsr:
    @staticmethod
    def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
        # note: use math.isclose() outside 15-112 with Python version 3.5 or later
        return (abs(d2 - d1) < epsilon)
    
    @staticmethod
    def roundHalfUp(d): #helper-fn
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
    
    @staticmethod
    def batchRoundHalfUp(lst):
        newLst = []
        for num in lst:
            new = mathUsr.roundHalfUp(num)
            newLst.append(new)
        return newLst
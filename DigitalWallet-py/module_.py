import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: module_


class DigitalWallet:
    def  __init__(self):
        self.Balances: _dafny.Map = _dafny.Map({})
        self.PINs: _dafny.Map = _dafny.Map({})
        self.WrongAttempts: _dafny.Map = _dafny.Map({})
        pass

    def __dafnystr__(self) -> str:
        return "_module.DigitalWallet"
    def ctor__(self):
        (self).Balances = _dafny.Map({})
        (self).PINs = _dafny.Map({})
        (self).WrongAttempts = _dafny.Map({})

    def Valid(self):
        def lambda0_(forall_var_0_):
            d_0_userId_: int = forall_var_0_
            return not ((d_0_userId_) in (self.Balances)) or (((self.Balances)[d_0_userId_]) >= (0))

        return ((((self.Balances).keys) == ((self.PINs).keys)) and (((self.PINs).keys) == ((self.WrongAttempts).keys))) and (_dafny.quantifier((self.Balances).keys.Elements, True, lambda0_))

    def AccountIsLocked(self, userId):
        return ((self.WrongAttempts)[userId]) >= ((self).MaxWrongAttempts)

    def NewAccount(self, userId, initialBalance, pin):
        (self).Balances = (self.Balances).set(userId, initialBalance)
        (self).PINs = (self.PINs).set(userId, pin)
        (self).WrongAttempts = (self.WrongAttempts).set(userId, 0)

    def Authenticate(self, userId, pin):
        isSuccessful: bool = False
        d_0_locked_: bool
        d_0_locked_ = (self).AccountIsLocked(userId)
        if (not(d_0_locked_)) and (((self.PINs)[userId]) == (pin)):
            (self).WrongAttempts = (self.WrongAttempts).set(userId, 0)
            isSuccessful = True
            return isSuccessful
        elif (not(d_0_locked_)) and (((self.PINs)[userId]) != (pin)):
            d_1_currentAttempts_: int
            d_1_currentAttempts_ = (self.WrongAttempts)[userId]
            (self).WrongAttempts = (self.WrongAttempts).set(userId, (d_1_currentAttempts_) + (1))
            isSuccessful = False
            return isSuccessful
        elif True:
            isSuccessful = False
            return isSuccessful
        return isSuccessful

    def GetBalance(self, userId, pin):
        balance: int = int(0)
        balance = (self.Balances)[userId]
        return balance
        return balance

    def Credit(self, userId, pin, amount):
        (self).Balances = (self.Balances).set(userId, ((self.Balances)[userId]) + (amount))

    def Transfer(self, sourceId, sourcePin, destinationId, amount):
        (self).Balances = (self.Balances).set(sourceId, ((self.Balances)[sourceId]) - (amount))
        (self).Balances = (self.Balances).set(destinationId, ((self.Balances)[destinationId]) + (amount))

    def AddInterest(self, ratePercentage):
        d_0_keys_: _dafny.Set
        d_0_keys_ = (self.Balances).keys
        d_1_userIds_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = (self).SetToSeq(d_0_keys_)
        d_1_userIds_ = out0_
        d_2_i_: int
        d_2_i_ = 0
        d_3_oldBalances_: _dafny.Map
        d_3_oldBalances_ = self.Balances
        while (d_2_i_) < (len(d_1_userIds_)):
            d_4_userId_: int
            d_4_userId_ = (d_1_userIds_)[d_2_i_]
            d_5_currentBalance_: int
            d_5_currentBalance_ = (d_3_oldBalances_)[d_4_userId_]
            d_6_interest_: int
            d_6_interest_ = _dafny.euclidian_division((d_5_currentBalance_) * (ratePercentage), 100)
            (self).Balances = (self.Balances).set(d_4_userId_, (d_5_currentBalance_) + (d_6_interest_))
            d_2_i_ = (d_2_i_) + (1)

    def SetToSeq(self, s):
        result: _dafny.Seq = _dafny.Seq({})
        result = _dafny.SeqWithoutIsStrInference([])
        d_0_remaining_: _dafny.Set
        d_0_remaining_ = s
        while (d_0_remaining_) != (_dafny.Set({})):
            d_1_x_: int
            with _dafny.label("_ASSIGN_SUCH_THAT_d_0"):
                assign_such_that_0_: int
                for assign_such_that_0_ in (d_0_remaining_).Elements:
                    d_1_x_ = assign_such_that_0_
                    if (d_1_x_) in (d_0_remaining_):
                        raise _dafny.Break("_ASSIGN_SUCH_THAT_d_0")
                raise Exception("assign-such-that search produced no value")
                pass
            result = (result) + (_dafny.SeqWithoutIsStrInference([d_1_x_]))
            d_0_remaining_ = (d_0_remaining_) - (_dafny.Set({d_1_x_}))
        return result

    @property
    def MaxWrongAttempts(self):
        return 3

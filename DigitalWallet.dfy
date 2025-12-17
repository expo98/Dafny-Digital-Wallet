class DigitalWallet {
    // 1. STATE VARIABLES
    var Balances: map<int, int>
    var PINs: map<int, int>
    var WrongAttempts: map<int, int>

    // 2. CONSTANT (must come before constructor)
    const MaxWrongAttempts: int := 3

    // 3. CONSTRUCTOR
    constructor() 
        ensures Valid()
        ensures Balances == map[]
    {
        Balances := map[];
        PINs := map[];
        WrongAttempts := map[];
    }

    // 5. INVARIANT PREDICATE
    predicate Valid()
        reads this
    {
        Balances.Keys == PINs.Keys && PINs.Keys == WrongAttempts.Keys &&
        forall userId :: userId in Balances ==> Balances[userId] >= 0
    }

    // 6. OTHER PREDICATES/FUNCTIONS
    predicate AccountIsLocked(userId: int)
        reads this
        requires Valid()
        requires userId in Balances
    {
        WrongAttempts[userId] >= MaxWrongAttempts
    }

    // 7. METHODS

    method NewAccount(userId: int, initialBalance: int, pin: int) 
        modifies this 
        requires Valid()
        requires userId !in Balances                  
        requires initialBalance >= 0
        ensures Valid()
        ensures userId in Balances                    
        ensures Balances[userId] == initialBalance    
        ensures PINs[userId] == pin                   
        ensures WrongAttempts[userId] == 0
        ensures forall id :: id in old(Balances) ==> id in Balances && Balances[id] == old(Balances[id])
    {
        Balances := Balances[userId := initialBalance];
        PINs := PINs[userId := pin];
        WrongAttempts := WrongAttempts[userId := 0];
    }

    // Function 2: Authenticate
    method Authenticate(userId: int, pin: int) returns (isSuccessful: bool) 
        modifies this 
        requires Valid()
        requires userId in Balances
        ensures Valid()
    {
        var locked := AccountIsLocked(userId);
        
        if !locked && PINs[userId] == pin {
            WrongAttempts := WrongAttempts[userId := 0];
            return true;
        } else if !locked && PINs[userId] != pin {
            var currentAttempts := WrongAttempts[userId];
            WrongAttempts := WrongAttempts[userId := currentAttempts + 1];
            return false;
        } else {
            return false;
        }
    }
    
    // Function 3: GetBalance
    method GetBalance(userId: int, pin: int) returns (balance: int) 
        requires Valid()
        requires userId in Balances 
        requires pin == PINs[userId]                  
        requires !AccountIsLocked(userId)            
        ensures balance == Balances[userId]          
    {
        return Balances[userId];
    }
    
    // Function 4: Credit
    method Credit(userId: int, pin: int, amount: int) 
        modifies this 
        requires Valid()
        requires userId in Balances
        requires pin == PINs[userId]
        requires !AccountIsLocked(userId)
        requires amount > 0
        ensures Valid()
        ensures userId in Balances
        ensures Balances[userId] == old(Balances[userId]) + amount 
        ensures Balances.Keys == old(Balances.Keys)
        ensures forall id :: id in Balances && id != userId ==> Balances[id] == old(Balances)[id]
    {
        Balances := Balances[userId := Balances[userId] + amount];
    }
    
    // Function 5: Transfer
    method Transfer(sourceId: int, sourcePin: int, destinationId: int, amount: int) 
        modifies this 
        requires Valid()
        requires sourceId in Balances && destinationId in Balances 
        requires sourceId != destinationId
        requires sourcePin == PINs[sourceId] && !AccountIsLocked(sourceId) 
        requires amount > 0                                        
        requires Balances[sourceId] >= amount
        ensures Valid()
        ensures sourceId in Balances && destinationId in Balances
        ensures Balances[sourceId] == old(Balances[sourceId]) - amount
        ensures Balances[destinationId] == old(Balances[destinationId]) + amount
        ensures Balances.Keys == old(Balances.Keys)
        ensures forall id :: id in Balances && id != sourceId && id != destinationId ==>
            Balances[id] == old(Balances)[id]
    {
        Balances := Balances[sourceId := Balances[sourceId] - amount];
        Balances := Balances[destinationId := Balances[destinationId] + amount];
    }
    
    // Function 6: AddInterest
    method AddInterest(ratePercentage: int)
        modifies this
        requires Valid()
        requires ratePercentage >= 0 
        ensures Valid()
        ensures Balances.Keys == old(Balances.Keys)
        ensures forall userId :: userId in old(Balances) ==>
            Balances[userId] == old(Balances)[userId] + (old(Balances)[userId] * ratePercentage / 100)
    {
        var keys := Balances.Keys;
        var userIds := SetToSeq(keys);
        var i := 0;
        var oldBalances := Balances;
        
        while i < |userIds|
            invariant 0 <= i <= |userIds|
            invariant Valid()
            invariant Balances.Keys == old(Balances.Keys)
            invariant PINs == old(PINs)
            invariant WrongAttempts == old(WrongAttempts)
            invariant oldBalances == old(Balances)
            invariant forall j :: 0 <= j < i ==> 
                Balances[userIds[j]] == oldBalances[userIds[j]] + (oldBalances[userIds[j]] * ratePercentage / 100)
            invariant forall userId :: userId in Balances && userId !in userIds[..i] ==>
                Balances[userId] == oldBalances[userId]
        {
            var userId := userIds[i];
            var currentBalance := oldBalances[userId];
            var interest := (currentBalance * ratePercentage) / 100;
            Balances := Balances[userId := currentBalance + interest];
            i := i + 1;
        }
    }
    
    // Helper method to convert set to sequence
    method SetToSeq(s: set<int>) returns (result: seq<int>)
        ensures forall x :: x in s <==> x in result
        ensures |result| == |s|
    {
        result := [];
        var remaining := s;
        while remaining != {}
            decreases remaining
            invariant forall x :: x in result ==> x in s
            invariant forall x :: x in s <==> x in remaining || x in result
            invariant forall x :: x in result ==> x !in remaining
            invariant |result| + |remaining| == |s|
        {
            var x :| x in remaining;
            result := result + [x];
            remaining := remaining - {x};
        }
    }
}
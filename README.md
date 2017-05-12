# ou-parser-test
a parser test

# Data format to be parsed:

```haskell
data HashAlg = SHA256
             | SHA384
             deriving Show

data OU = OUApplicationId Int64
        | OUHashAlg       HashAlg
        | OUSerialNumbers [Int32]
        | OUAllowsExec    Bool

-- "01 xxxxxxxxxxxxxxxx APPID"        <-> OUApplicationId Int64
-- "02 01 SHA256"                     <-> OUHashAlg SHA256
-- "02 01 SHA384"                     <-> OUHashAlg SHA384
-- "03 xxxxxxxx yyyyyyyy zzzzzzzz SN" <-> OUSerialNumbers [Int32]
-- "04 01 EXEC"                       <-> OUAllowsExec Bool
```

write two functions:

read :: String -> OU
show :: OU -> String

to parse or show the data.

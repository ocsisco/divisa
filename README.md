# DIVISA

**"Divisa" is an api for currency exchange, it works in a similar way to the commercial apis available in the market**

How to use "divisa"?
"divisa" consists of the next endpoints:

``` [python]
/fetch-one
/fetch-multi
/fetch-all
/convert
/currencies
```



* /fetch-one:

If you GET: */fetch-one?from=USD&to=EUR*

the api return: 
`{
  "base": "USD",
  "result": {
    "EUR": 0.87259
  },
  "updated": "2021-11-11 11:18:24"
}`



* /fetch-multi:*separate paragraph*

If you GET: /fetch-multi?from=USD&to=EUR

return:
`{
  "base": "USD",
  "results": {
    "EUR": 0.87208,
    "GBP": 0.74628
  }
}`

* /fetch-all:

If you GET: /fetch-all?from=USD

return:
`{
  "base": "USD",
  "results": {
    "EUR": 0.87208,
    "GBP": 0.74633,
    "USD": 1.0
  }
}`

* /convert

If you GET: /convert?from=GBP&to=USD&amount=200

return: 
`{
  "amount": "200",
  "base": "GBP",
  "result": {
    "USD": 268.02,
    "rate": 1.34011
  }
}`

* /currencies

If you GET: /currencies

return: 
`{
  "EUR": "Euro",
  "GBP": "British Pound Sterling",
  "USD": "United States Dollar"
}`



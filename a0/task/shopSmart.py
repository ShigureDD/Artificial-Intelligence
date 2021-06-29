"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    CostList = {}
    for shop in fruitShops:
        cost = shop.getPriceOfOrder(orderList)
        CostList[shop] = cost
    
    ans = min(CostList, key=CostList.get) 
    return ans
    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
    totalProfit = 0.0
    for fruit in orderList:
        maxFriutPrice = 0.0
        minFriutPrice = fruitShops[0].fruitPrices[fruit[0]]
        for shop in fruitShops:
            if(shop.fruitPrices[fruit[0]]>maxFriutPrice):
                maxFriutPrice = shop.fruitPrices[fruit[0]]
            if(shop.fruitPrices[fruit[0]]<minFriutPrice):
                minFriutPrice = shop.fruitPrices[fruit[0]]
        totalProfit += fruit[1]*(maxFriutPrice-minFriutPrice)

    return totalProfit

def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    cost = 0.0
    for fruit in orderList:
        minFriutPrice = fruitShops[0].fruitPrices[fruit[0]]
        for shop in fruitShops:
            if(shop.fruitPrices[fruit[0]]<minFriutPrice):
                minFriutPrice = shop.fruitPrices[fruit[0]]
        cost += fruit[1]*minFriutPrice
    return cost

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())

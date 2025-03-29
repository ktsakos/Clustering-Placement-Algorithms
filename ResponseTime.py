import json
import math


firstjson= """
{"checkoutservice": {"cartservice": "72", "shippingservice": "72", "emailservice": "461", "paymentservice": "224", "currencyservice": "86", "productcatalogservice": "5"}, "recommendationservice": {"productcatalogservice": "15"}, "frontend": {"adservice": "79", "cartservice": "98", "checkoutservice": "4835", "recommendationservice": "1917", "shippingservice": "24", "currencyservice": "1360", "productcatalogservice": "47"}, "loadgenerator": {"frontend": "20"}}
"""

firstdict=json.loads(firstjson)


secondjson= """
{"checkoutservice": {"cartservice": "284", "shippingservice": "69", "emailservice": "417", "paymentservice": "218", "currencyservice": "200", "productcatalogservice": "5"}, "recommendationservice": {"productcatalogservice": "23"}, "frontend": {"adservice": "173", "cartservice": "280", "checkoutservice": "4842", "recommendationservice": "1225", "shippingservice": "79", "currencyservice": "2270", "productcatalogservice": "90"}, "loadgenerator": {"frontend": "1617"}}
"""
seconddict=json.loads(secondjson)

firstsum=0
#first sum calculations
listofcouples=[]
for x in sorted(firstdict.keys()):
    for y in sorted(firstdict[x].keys()):
        couples=[]
        print(x+"->"+y)
        firstsum+=int(firstdict[x][y])
        couples.append(int(firstdict[x][y]))
        listofcouples.append(couples)
#print(firstdict)

counter=0
secondsum=0
#secon sum calculations
for x in sorted(seconddict.keys()):
    for y in sorted(seconddict[x].keys()):
        #print(x+"->"+y)
        secondsum+=int(seconddict[x][y])
        listofcouples[counter].append(int(seconddict[x][y]))
        counter+=1

print(listofcouples)
sqsum=0
absdifsum=0
for i in listofcouples:
    #print(i[0]-i[1])
    sqsum+=math.pow(i[1]-i[0],2)
    absdifsum+=abs(i[1]-i[0])



variation=firstsum-secondsum
print("Variation after placement of the overall response time is: "+ str(variation))

print("Mean Squared Error: "+str(math.sqrt(sqsum)/len(listofcouples)))

print("Sum of Absolute Differences:"+str(absdifsum))


if(variation>0):
    print("Reduced "+str(variation)+" ms")
elif(variation<0):
    print("Increased "+str(abs(variation))+" ms")
else:
    print("No change was noticed!")
list = []
hasCalled = False


def getUserChooseCurrency():
    list = []
    f = open('currencyList.txt', 'r')
    for line in f.readlines():
        list.append(line.strip())
    f.close()
    #print(list)
    return list





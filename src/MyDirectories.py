class MyDirectories(object):
    # Sihan = "/Users/sihanliu"
    # TempDir = Sihan + "Desktop/AlgoTradingCourse/taq"
    # UnitTests = TempDir + "/unit_tests"
    #
    # TAQ = "/Users/sihanliu/Desktop/AlgoTradingCourse/taq/data"
    #
    # BinRTTradesDir = TAQ + "/trades"
    # BinRQQuotesDir = TAQ + "/quotes"
    Ruihan = "/Users/apple"
    TempDir = Ruihan + "/taq_2"
    UnitTests = TempDir + "/src"

    TAQ = "/Users/apple/taq_2/data"

    BinRTTradesDir = TAQ + "/trades"
    BinRQQuotesDir = TAQ + "/quotes"



def getTempDir():
    return MyDirectories.TempDir


def getTradesDir():
    return MyDirectories.BinRTTradesDir


def getQuotesDir():
    return MyDirectories.BinRQQuotesDir


def getTAQDir():
    return MyDirectories.TAQ
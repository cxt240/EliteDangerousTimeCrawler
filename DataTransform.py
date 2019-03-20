def TransformYears(years, months, days):
    total = int(years) + (int(months)/12) + (int(days)/365.25)
    print("Total: ", total)
    return total


# Transforms an array without data to an actual year decimal
def TransformYearArray(dataArray):
    return TransformYears(dataArray[1], dataArray[2], dataArray[3])

def squaredNormalizedProbabilities(fitnessValues):
    maxValue=max(fitnessValues)
    minValue=min(fitnessValues)
    normalized = list(
        map(
            lambda x: (x - minValue)**2,
            fitnessValues
        )
    )
    total = sum(normalized)
    probabilities=list(map(lambda x: x/total, normalized))
    probabilities.sort(reverse=True)
    return probabilities
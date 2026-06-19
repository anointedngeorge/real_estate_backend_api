


def stepsCounter(paginator, start=10, stop=10):
    steps = list(range(start, paginator + 1, stop))
    if not steps or steps[-1] != paginator:
        steps.append(paginator)
    return steps
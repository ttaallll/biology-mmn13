__author__ = 'pais'

from random import randint
import sys


CONFIG_map = 'map6'
CONFIG_mutation = 2  # out of 10
CONFIG_crossover = 7  # out of 10
CONFIG_generationsNum = 10000

# populationSize = 20
populationSize = 40
# populationSize = 60


######
currentSolutions = []
mapStart = (0, 0)
mapEnd = (0, 0)
gameMap = []


def readMap(mapFile):

    global gameMap
    global mapStart
    global mapEnd

    with open(mapFile) as f:
        gameMap = f.readlines()

    # find start and end
    for i in range(len(gameMap)):
        for j in range(len(gameMap[i])):
            if gameMap[i][j] == 'S':
                mapStart = (i, j)
            elif gameMap[i][j] == 'E':
                mapEnd = (i, j)


def manhattan(currentPoint, targetPoint):
    # return manhattan distance - heuristic
    return abs(currentPoint[0] - targetPoint[0]) + abs(currentPoint[1] - targetPoint[1])


def fitness(solution):
    count = 0
    tempLocation = mapStart
    for tempDirection in solution:

        if tempDirection == 0: #Up
            tempLocation = (tempLocation[0] - 1, tempLocation[1])
        elif tempDirection == 1: #Down
            tempLocation = (tempLocation[0] + 1, tempLocation[1])
        elif tempDirection == 2: #Left
            tempLocation = (tempLocation[0], tempLocation[1] - 1)
        elif tempDirection == 3: #Right
            tempLocation = (tempLocation[0], tempLocation[1] + 1)

        if gameMap[tempLocation[0]][tempLocation[1]] == '|':
            return [False, 10000]

        if gameMap[tempLocation[0]][tempLocation[1]] == 'X':
            return [False, 10000]

        if tempLocation[0] == mapEnd[0] and tempLocation[1] == mapEnd[1]:
            return [True, count]

        count += 1

    return [False, manhattan(tempLocation, mapEnd)]


def initializeSolutions():
    global currentSolutions
    currentSolutions = []
    for i in range(populationSize):
        newTempSolution = [randint(0, 3)]
        currentSolutions += [{
            'path': newTempSolution,
            'score': 0
        }]


def getLetterForIndex(index1):
    if index1 == 0:
        return 'U'
    elif index1 == 1:
        return 'D'
    elif index1 == 2:
        return 'L'
    elif index1 == 3:
        return 'R'


def mutation(solution):
    if randint(0, 10) < CONFIG_mutation:
        indexRand = randint(0, len(solution) - 1)
        directionRand = randint(0, 3)
        solution[indexRand] = directionRand
    # return solution

    return solution + [randint(0, 3)]


def crossover(solution1, solution2):
    if randint(0, 10) < CONFIG_crossover:

        minRange = min(len(solution1), len(solution2))

        indexRand = randint(0, minRange - 1)
        newSolution1 = solution1[:indexRand] + solution2[indexRand:]
        newSolution2 = solution2[:indexRand] + solution1[indexRand:]

        return newSolution1, newSolution2

    else:
        return solution1, solution2


def isExist(solution, bestSolutions):

    for tempSolution in bestSolutions:

        if 'path' not in tempSolution:
            continue

        tempSolution = tempSolution['path']
        if len(tempSolution) != len(solution):
            continue

        exist = True
        k = 0
        while k < len(tempSolution):
            if tempSolution[k] != solution[k]:
                exist = False
                break
            k += 1
        if exist:
            return True

    return False


def main():

    global currentSolutions

    readMap(CONFIG_map)
    initializeSolutions()

    minGlobalGeneration = 0
    minGlobalPath = []
    minGlobalLength = 9999

    for i in range(CONFIG_generationsNum):

        nextSolutions = []

        countSolution = 0

        minScore = 9999
        maxPath = []
        for tempSolution in currentSolutions:
            countSolution += 1
            score = fitness(tempSolution['path'])
            if score[0]:
                # print 'found'
                # print 'generation - ' + str(i)
                # print 'solution - ' + str(countSolution)
                # print 'score ' + str(score[1])
                # for tempDirection in tempSolution['path'][:score[1] + 1]:
                #     sys.stdout.write(str(getLetterForIndex(tempDirection)) + ',')
                # print ''
                # for tempDirection in tempSolution['path']:
                #     sys.stdout.write(str(tempDirection) + ',')
                # return
                pass
            if score[1] == 10000:
                tempSolution['path'] = tempSolution['path'][:-1]

            if score[1] < minScore:
                minScore = score[1]
                maxPath = tempSolution['path']

            if score[0] and len(tempSolution['path']) < minGlobalLength:
                # minGlobalScore = score[1]
                minGlobalPath = tempSolution['path']
                minGlobalLength = len(tempSolution['path'])
                minGlobalGeneration = i

            tempSolution['score'] = score[1]

        # print 'min score this generation - ' + str(minScore)
        # print 'min path: '
        # for tempDirection in maxPath:
        #     sys.stdout.write(str(getLetterForIndex(tempDirection)) + ',')
        # print ''
        # print '---------'

        print 'min length global - ' + str(minGlobalLength)
        print 'min generation - ' + str(minGlobalGeneration)
        print 'min path: '
        for tempDirection in minGlobalPath:
            sys.stdout.write(str(getLetterForIndex(tempDirection)) + ',')
        print ''
        print '##############'

        bestSolutionsThisGeneration = [{'score': 99999}] * (populationSize/2)

        for tempSolution in currentSolutions:
            if tempSolution['score'] == -1:
                nextSolutions += [tempSolution]
                continue

            if not isExist(tempSolution['path'], bestSolutionsThisGeneration):
                for j in range(len(bestSolutionsThisGeneration)):
                    if tempSolution['score'] < bestSolutionsThisGeneration[j]['score']:
                        bestSolutionsThisGeneration[j] = tempSolution
                        break

        k = 0
        while k < len(bestSolutionsThisGeneration) and len(nextSolutions) + 1 < populationSize:

            tempSolution1 = bestSolutionsThisGeneration[k]
            tempSolution2 = bestSolutionsThisGeneration[k+1]

            if 'path' not in tempSolution1 or len(tempSolution1['path']) == 0:
                tempSolution1['path'] = [randint(0, 3)]

            if 'path' not in tempSolution2 or len(tempSolution2['path']) == 0:
                tempSolution2['path'] = [randint(0, 3)]

            # do crossover
            crossoverSolution1, crossoverSolution2 = crossover(tempSolution1['path'], tempSolution2['path'])

            # do mutation
            newSolution1 = mutation(crossoverSolution1)
            newSolution2 = mutation(crossoverSolution2)


            nextSolutions += [{
                'path': newSolution1,
                'score': 0
            }]
            nextSolutions += [{
                'path': newSolution2,
                'score': 0
            }]

            k += 2


        currentSolutions = nextSolutions + bestSolutionsThisGeneration
        currentSolutions = currentSolutions[:populationSize]


    print 'min length global - ' + str(minGlobalLength)
    print 'min generation - ' + str(minGlobalGeneration)
    print 'min path: '
    for tempDirection in minGlobalPath:
        sys.stdout.write(str(getLetterForIndex(tempDirection)) + ',')
    print ''

main()
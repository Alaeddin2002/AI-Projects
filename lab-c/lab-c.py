import os
import math

def rebuild(dict,feature):
    elements = {}
    index = 0
    for x in dict.keys():
        if x == feature:
            for value in dict[x]:
                if value in elements.keys():
                    elements[value].append(index)
                else:
                    elements[value] = []
                    elements[value].append(index)
                index += 1
    outerDict = {}
    for x in elements.keys():
        innerDict = {}
        for y in dict.keys():
            if y != feature:
                innerDict[y] = []
                for value in elements[x]:
                    innerDict[y].append(dict[y][value])
                outerDict[x] = innerDict
    return outerDict

def split(node,feature):
    node._featureSplit = feature
    data = rebuild(node._dataDict,feature)
    for key in data.keys():
        yesCount = 0
        noCount = 0
        values = list(data[key].values())
        classificationCol = values[len(values)-1]
        for value in classificationCol:
            if value == 'yes':
                yesCount += 1
            else:
                noCount += 1
        total = yesCount + noCount
        if yesCount > noCount:
            percent = "{:.0%}".format(yesCount/total)
            classification = 'yes, '+ "Percentage accuracy: "  + str(percent)
        else:
            percent = "{:.0%}".format(noCount/total)
            classification = 'no, ' + "Percentage accuracy: " + str(percent)
        newNode = Node(data[key],classification)
        data[key] = newNode
    node.childrenDict = data

def build_tree(node):
    if (len(node._dataDict) == 1):
        return node.classification
    entropies = attribute_entropies(node._dataDict)
    lowest_feat = smallest_entropy(entropies)
    split(node,list(lowest_feat.keys())[0])
    for i in range(0,len(node.childrenDict)):
        build_tree(node.childrenDict[list(node.childrenDict.keys())[i]])

def smallest_entropy(dict):
    lowest = 2
    for key in dict:
        if dict[key] < lowest:
            lowest = dict[key]
            lowestDict = {key : dict[key]}
    return lowestDict

def visualize(node,space):
    if node.childrenDict == None:
        return 0
    space += "   "
    for key in node.childrenDict:
        print(space + node._featureSplit + " = " + key + ": " + node.childrenDict[key].classification)
        visualize(node.childrenDict[key],space)

class Node:
    def __init__(self,dataDict,classification):
        self._featureSplit = None
        self._dataDict = dataDict
        self.childrenDict = None
        self.classification = classification

def occurrence(dataset,attribute):
    dictionary = dataset #transfer data set into dictionary based on columns(will be a function)
    values = entropies(dataset,attribute) #the entropy of each unique value in attribute
    counts = 0
    count={}
    for i in values:
        count[i] = 0
    for i in range(len(dictionary[attribute])):
            if dictionary[attribute][i] in values:
                count[dictionary[attribute][i]] +=1

    for i in count:
        counts+= count[i]
    for i in count:
        count[i] = count[i]/counts
    return count

def attribute_entropies(dataset):
    attributes= dataset
    values = {}
    for i in attributes:
        column = entropies(dataset,i)
        number = occurrence(dataset,i)
        values[i]=0
        for j in column:
            values[i] += (column[j]*number[j])
    values.popitem()
    return values #  multiply of the fraction of how many values are

def read_file(filename):
    dictionary = {}
    t = []
    second = []
    third = []
    f = open(filename, "r")
    
    # get the number of rows
    m = f.readlines()
    count = 0
    for i in m:
        count +=1
        
    # append each line in the file to a list
    for i in m:
        d = i.strip()
        t.append(d)
    # adjusting the list (t) by removing \t and adding them to another list   
    for i in range(len(t)):
        a = (t[i].replace('\t',','))
        second.append(a)
     # spliting the strings in list (second)  and adding them to another list      
    for i in second:
        a = i.split(',')
        third.append(a)
        
    # Creating the dictionary
    size = len(third[0])
    for i in range ((size)):
        dictionary[third[0][i]] = []
    for j in range (len(third)-1):
        for i in range (size):
            dictionary[third[0][i]].append(third[j+1][i])
        
    return dictionary

def unique(lst):
    lst2 = []
    for i in lst:
        if i not in lst2:
            lst2.append(i)
    return lst2

def entropies(dataset,attribute):
    dictionary = dataset #transfer data set into dictionary based on columns (will be a function)
    attributes = []
    values = [] #values in attribute
    entropies = {}
    for i in dictionary:
        attributes.append(i)
    for i in range(len(dictionary[attribute])):
        values.append(dictionary[attribute][i])
    unique_val = unique(values) #unique will be a seperate function that returns a list of unique values

    uni = {} #dictionary 2
    for i in unique_val:
        uni[i] = [0,0]
    #create a dictionary of unique values in format value:[number of yes,number of no]
    for i in range(len(values)): #len values because we want the number of rows in dataset
        if dictionary[attributes[-1]][i] == 'yes':
            for j in range(len(unique_val)):
                if dictionary[attribute][i] == unique_val[j]:
                    uni[unique_val[j]][0] +=1
        elif dictionary[attributes[-1]][i] == 'no':
            for j in range(len(unique_val)):
                if dictionary [attribute][i] == unique_val[j]:
                    uni[unique_val[j]][1] +=1
    #calculate enolopies for each value
    for i in (uni):
        if (-uni[i][0]) == 0 or (-uni[i][1]) == 0:
            entropies[i] = 0
        else:
            entropies[i] = (-uni[i][0])/(uni[i][0]+uni[i][1])*math.log(uni[i][0]/(uni[i][0]+uni[i][1])) - (uni[i][1]/(uni[i][0]+uni[i][1])*math.log(uni[i][1]/(uni[i][0]+uni[i][1])))
    for i in ((uni)):
        uni[i] = entropies [i] # assosiate each value with its entropy
    return uni

def accuracy(dict):
    data = dict
    accurate = 0
    unaccurate = 0
    ori = Node(data,'no')
    original = build_tree(ori)
    ori_class = ori.classification
    for j in data:
        size = len(data[j])

    for i in range((size)):
        for j in data:
            element = data[j].pop(0)
        root = Node(data,'no')
        tree = build_tree(root)
        data[j].append(element)
        if root.classification == ori_class:
            accurate+=1
        else:
            unaccurate+=1
    return (accurate/(accurate+unaccurate) *100)
def row_acc(dict):
    data = dict
    row = {}
    accurate = 0
    unaccurate = 0
    for key in data.keys():
        return key
    for j in data:
        size = len(data[j])

    for i in range((size)):
        for key in data.keys():
            return key
            element = data[j].pop(0)
            row[j] = element
        return row
        root = Node(data,'yes')
        tree = build_tree(root)
        data[j].append(element)
        x = query(root,row)
        if x[0] == 'y':
            if root.classification is 'yes':
                accurate+=1
            else:
                unaccurate+=1
        elif x[0] == 'n':
            if root.classification is 'no':
                accurate+=1
            else:
                unaccurate+=1
    return (accurate/(accurate+unaccurate) *100)
    
    
def query(node,dict):
    node = node
    while node.childrenDict != None:
        feature = node._featureSplit
        split = dict[feature]
        node = node.childrenDict[split]
    return node.classification

def main(text):
    data = read_file(text)
    print(data)
    #print(data)
#     root = Node(data,'yes')
#     build_tree(root)
#     space = " "
#     visualize(root,space)
#     dict = {'size':'tiny','color':'white','earshape':'pointed','tail':'yes','iscat':'no'}
#     classif = query(root,dict)
#     print(classif)
    #treeAccuracy = str(accuracy(data))
    #print(" ")
    #print("Accuracy: "+treeAccuracy)
   # print(row_acc(data))
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='classification')
    parser.add_argument('-t', '--Text', type=str, required = True)
    args = parser.parse_args()
    if not (os.path.isfile(args.Text)):
        exit(-1)
    main(args.Text)

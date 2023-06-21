#Michael Ellerkamp
#Project A05: Graphviz
#GraphViz.Helper.py is made to do the brunt of the work for my graphing.
#it has one edge creation method and 2 node creation methods, only use one of them per run.

import graphviz
import random
#refer to def ClanSubGraph(graph, list, people): for more details
#main point of this one is that name includes "cluster" this enables the subgraphs
#once enabled their color, and other attributes all turn on and it groups up nodes within the cluster.
def ClanSubGraph(graph, list, people):
    i=0
    SubColor = ["red","yellow","green","orange","brown",'grey','violet','maroon']
    random.shuffle(SubColor)
    j=0
    for item in list:
        with graph.subgraph(name = 'cluster_' + item) as g:
            g.attr(cluster = 'true')
            g.attr(bgcolor = SubColor[j])
            g.attr(label = str(item) + ' Clan')
            g.attr(labelloc = 't')
            g.attr(rankdir ='TB')
            g.node_attr.update({'shape':'record'})
            for person in people:
                if str(person[10]) == str(list[i]):
                    temp = person[0]
                    details = '<first>'+person[1]+'|<last>'+person[15]+'|<byear> Birth Year: '+person[4]+'|<dyear>Death Year = '+person[5]+'|<age>Age: '+str((int(person[5])-int(person[4])))
                    if person[2] == 'M':
                        g.node(temp,details, color = 'blue', rank = person[3])
                    else:
                        g.node(temp,details, color = 'pink', rank = person[3])
            i+=1
        j= (j+1) % len(SubColor)
#the prettier of my graphing solutions, the backbone of subgraphs is in here but they are turned off
#only when "cluster" is added to the name will those attributes turn on.
#As is this version is much more readable.
#This produces all my nodes and applies them to their respective subgraphs.
def NoClanSubGraph(graph, list, people):
    i=0
    SubColor = ["red","yellow","green","orange","brown",'grey','violet','maroon']
    random.shuffle(SubColor)
    j=0
    #list here is refering to my unique clan list as I wanted a subgraph for each clan
    for item in list:
        #here is where we would add cluster to turn on subgraphs, see the method above.
        with graph.subgraph(name = '_' + item) as g:
            g.attr(cluster = 'true')
            g.attr(bgcolor = SubColor[j])
            g.attr(label = str(item) + ' Clan')
            g.attr(labelloc = 't')
            g.attr(rankdir ='TB')
            g.node_attr.update({'shape':'record'})
            for person in people:
                #this goes through my entire list and sees if they are in the clan of the current subgraph I am working on.
                if str(person[10]) == str(list[i]):
                    temp = person[0]
                    #populating the nice details for the node.
                    details = '<first>'+person[1]+'|<last>'+person[15]+'|<byear> Birth Year: '+person[4]+'|<dyear>Death Year = '+person[5]+'|<age>Age: '+str((int(person[5])-int(person[4])))
                    #color coordinating genders: M = blue, F = pink.
                    #this also ranks them in their respective subgraph based off their generation number
                    if person[2] == 'M':
                        g.node(temp,details, color = 'blue', rank = person[3])
                    else:
                        g.node(temp,details, color = 'pink', rank = person[3])
            #i is important to track subgraphs
            i+=1
        #j is tracking my colors.
        j= (j+1) % len(SubColor)
#this beauty is where we connect everything together.
#All edges live here
def PopulateEdges(graph,family):
    Edges = []
#this is for each partner pair
#checking for uniqueness before I make partners pair up so I don't have 2 edges between them.
    for person in family:
        if person[11] and [person[11], person[0]] not in Edges and [person[0],person[11]] not in Edges:
            Edges.append([person[11],person[0]])        
    for Edge in Edges:
        graph.edge(Edge[0], Edge[1], dir='none')
#now for parent-child
#the goal here is to have a list with the first index being a unique parent, next index is the other parent, and then the last index is a list of all their children.
    Edges = []
    Parent = []
    for person in family:
        #Do they have a parent
        if person[12]:
            #Is there parent in my list already?
            if person[12] in Parent:
                #If the parent exists I add the other parent and the child to my list at that index
                Parent[Parent.index(person[12])].append([person[13], person[0]])
            else:
                #if they are not in my parent list I make the initial index for that parent.
                Parent.append([person[12],person[13],person[0]])
    #for this I want to make an invisible node between the parents and the children
    #That way the parents' edges merge and then become a single line to each child.
    for person in Parent:
        #unique identifyer for the edge so I can track the source easier.
        temp = person[0] + "___" + person[1]
        #the invisible node to connect the parents edges into one
        graph.node(temp, style = 'invisible')
        #duplicated edges were a pain aso this prevents it
        if [person[0], temp] not in Edges:
            graph.edge(person[0], temp, headclip = 'false', dir = 'none',)
            Edges.append([person[0], temp])
        if [person[1], temp] not in Edges:
            graph.edge(person[1], temp, headclip = 'false', dir = 'none')
            Edges.append([person[1], temp])
        #the edge leading to the child from the invisible node
        graph.edge(temp, person[2], tailclip = 'false')



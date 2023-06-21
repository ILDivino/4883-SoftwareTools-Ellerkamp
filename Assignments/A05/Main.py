#Michael Ellerkamp
#Project A05: Graphviz
#Main.py is the primary program I will be working in.
#It calls on two libraries I made in order to facilitate most of the work
#Sanitizer populates the family list with correct data.
#GraphViz_Helper handles most of the edge and node work.
import os
import csv
import random
import Sanitizer
import GraphViz_Helper
import graphviz

#path starts at my repo /4883-SoftwareTools_Ellerkamp
Root_Path = os.path.join(os.getcwd(), "Assignments\\A05\\")
Family_Path = os.path.join(Root_Path,"Family\\dwarf_family_tree.csv")
Name_Path = os.path.join(Root_Path,"Names\\asian_first_names.csv")
Clan_Path = os.path.join(Root_Path,"Names\\clan_names.txt")
Surname_Path = os.path.join(Root_Path,"Names\\asian_surnames.txt")
#The important lists that will be in the main program.
#Family Tree will be the key list that will be manipulated by having female/male names and clan surnames replacing the names in the list.
Family_Tree_Data = []
Female_Names = []
Male_Names = []
Surnames = []
Clan_Names = []

#This is where I populate all my lists with the files above.
Family_Tree_Data = Sanitizer.Populate_Family_Data(Family_Path)
Female_Names, Male_Names = (Sanitizer.Populate_Names(Name_Path))
Surnames = Sanitizer.Populate_Txt(Surname_Path)
Clan_Names = Sanitizer.Populate_Txt(Clan_Path)

#Then I populate the master list with the corrected data
Family_Tree_Data = Sanitizer.Assign_Partner(Family_Tree_Data)
Family_Tree_Data = Sanitizer.Apply_Given_and_Clan(Family_Tree_Data, Male_Names, Female_Names, Clan_Names)
Family_Tree_Data = Sanitizer.Apply_Surname(Family_Tree_Data, Surnames)

#this is the start of my graphing
#getting my unique clan list for subgraphs later
Clans = Sanitizer.Get_Unique_Clan(Family_Tree_Data)

#primary graph
Base_Graph = graphviz.Digraph('Family Tree',
                     node_attr={'shape': 'square'})
Base_Graph.attr(label = (Family_Tree_Data[0][15] + ' of clan '+Family_Tree_Data[0][10] + ' Family'), labelloc = 't')
Base_Graph.attr(rankdir = 'TB')

#Only enable one of these two. Cluster gives clans colors but messes up the format.
#Graph has a good view but no clans.
GraphViz_Helper.NoClanSubGraph(Base_Graph, Clans, Family_Tree_Data)
#GraphViz_Helper.ClanSubGraph(Base_Graph, Clans, Family_Tree_Data)

GraphViz_Helper.PopulateEdges(Base_Graph,Family_Tree_Data)

with open("Dot.txt","w") as f:
    f.write(Base_Graph.source)



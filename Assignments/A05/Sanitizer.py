#Michael Ellerkamp
#Project A05: Graphviz
"""
This is Sanitizer.py as part of my A05 assignment.
This method is designed to read in data we pulled from a family tree website.
The data has a great many flaws but most of them are fixed by this method.

notable flaws: ID do not match up with indexes making them reference out of bounds of you try to navigate using them as raw indices ( use list.index() instead)
Out of a pair of two people who are married only the created partner references the other.
No listing for last names.

Here are the columns we will reference.
0. ID
1. first name
2. gender
3. generation
4. birth year

5. death year
6. death age
7. marriage year
8. marriage age
*9. Personality type (Ignore this)

10. clan
11. spouseId
12. Parent ID (assuming a patriarch system so focusing on male parent)
*13. parent ID2
*14. parentnodeID (ignore this)

15. Last name
"""
import os
import re
import csv
import random

#since I have to index the 2d array.
def Index_2D(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))
#this populates my list with the initial data from the .csv we pull from the family website
#creates a 15th column which is my last name column since it was not in my original dataset.
def Populate_Family_Data(path):
    Temp = []
    with open(path, 'r') as csvfile:
        Temp = list(csv.reader(csvfile, delimiter=','))
    Temp.pop(0)
    #populates my 15th column which is last name with a placeholder value
    Temp = [x + ['0'] for x in Temp]
    return Temp
#This one reads in from the .txt that were provided by the instructor.
#they hold both male and female names and we have to supply them to the correct people.
def Populate_Names(path):
    Temp = []
    Temp2 = []
    Temp3 = []
    with open(path, 'r') as csvfile:
        Temp = list(csv.reader(csvfile, delimiter=','))
    for line in Temp:
        if str(line[-1]) == 'F':
            Temp2.append(line)
        elif str(line[-1]) == 'M':
            Temp3.append(line)
    random.shuffle(Temp2)
    random.shuffle(Temp3)
    return Temp2, Temp3
#reads in data from the .txt files and puts them into a list for me.
#clan and surnames each call this.
def Populate_Txt(path):
    Temp = []
    with open(path, 'r') as file:
        Temp = file.readlines()
    random.shuffle(Temp)
    return Temp
#default only the created partner points to their other partner. The original partner points to no one.
#This will make it so they point to each other.
#Had to create a function to index a 2d list to get the index calls right.
def Assign_Partner(list):
    for line in list:
        if line[11]:
            list[Index_2D(list,line[11])[1]][11] = line[11]
    return list
#this method is very heavy so even though it may be more costly I am putting it in it's own method for readability.    
#applying surnames is going to be interesting. 
#1. I believe the best route is to apply a unique surname to every index that has no parent that is male. This captures the patriarch and all males that enter the family through marriage.
#2. I will then apply that surname to their partner, regardless of their parent status, this ensure that all the women that married outside the family have their husband's name. 
#3. I will then traverse the list checking each member to see if they have a last name already.
#If they do have a last name and are male then they will populate their partner's last name with their last name. Giving the wives the name of their husbands.
#Since I am starting from the top this should populate each parent group before I reach their children.
#4.Now if they do not have surname they will look to their parents to acquire a surname, which if I did everything right both parents should have the same surname.
def Apply_Surname(Family_List, Surenames):
    i = 0
    #1.
    for line in Family_List:
        #using not line[12] as a comparison to see if they are empty. If they had content they would return true and thus !true is false.
        if(line[2] == 'M' and not line[12] and not line[13]):
            line[15] = str(Surenames[i]).strip()
            i+=1
    #2.
    for line in Family_List:
        #using not line[12] as a comparison to see if they are empty. If they had content they would return true and thus !true is false.
        if(line[2] == 'F' and line[11] and Family_List[Index_2D(Family_List,line[11])[1]] in Family_List and Family_List[int(Index_2D(Family_List,line[11])[1])][15] != "0"):
            line[15] = Family_List[Index_2D(Family_List,line[11])[1]][15].strip()
    #3
    for line in Family_List:
        if line[15] == '0':
            line[15] = Family_List[Index_2D(Family_List,line[12])[1]][15].strip()
    #4
    for line in Family_List:
        if line[2] == 'M':
            Family_List[Index_2D(Family_List,line[11])[1]][15] = line[15].strip()

    return Family_List
#pretty straightforward apply 3 lists worth of names to my main data list (family_list)
#found a bunch of new line crude hiding in my text so did a lot of stripping here.
def Apply_Given_and_Clan(Family_List, male,female, clan):
    M,F = 0,0
    for line in Family_List:
        #this is where we apply the clan name by converting the int in column 10 to a corresponding clan name in the clan list.
        line[10] = str(clan[int(line[10])]).strip()
        if line[2] == 'M':
            #if there are more people than I have names the list repeats without randomizing.
            line[1] = male[M][1].strip()
            M = (M+1) % len(male)
        if line[2] == 'F':
            line[1] = female[F][1].strip()
            F = (F+1) % len(female)
    return Family_List
#this makes a list of only the unique clan names, very vital for my clan subgraphs
def Get_Unique_Clan(list):
    temp = []
    for line in list:
        if line[10] not in temp:
            temp.append(line[10].strip())
    return temp

#This if statement allows me a person to test methods by running them by themself.
#when this is called by a different program the code block will not execute at all.
#I did a lot of my original data testing here, refer to Main.py for commends on the code.
if __name__ == "__main__":
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

    Family_Tree_Data = Populate_Family_Data(Family_Path)
    Female_Names, Male_Names = (Populate_Names(Name_Path))
    Surnames = Populate_Txt(Surname_Path)
    Clan_Names = Populate_Txt(Clan_Path)
    
    Family_Tree_Data = Assign_Partner(Family_Tree_Data)
    Family_Tree_Data = Apply_Given_and_Clan(Family_Tree_Data, Male_Names, Female_Names, Clan_Names)
    Family_Tree_Data = Apply_Surname(Family_Tree_Data, Surnames)
   # for line in Family_Tree_Data:
    #    print(line[1] + " " + line[15])   
    Clans = Get_Unique_Clan(Family_Tree_Data)
    print(Clans)
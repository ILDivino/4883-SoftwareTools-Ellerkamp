## Project A05
#### Name: Michael Ellerkamp
#### Description: Our goal is to create a graph of family trees and clans. We are given family data but we must change the names in the data. Once the data is proper sanitzed we must then create a program that turns the data into the dot language for graphviz.


|   #   |    File     |      Description                           |
| :---: | ----------- | -------------------------------------------|
|   1   |   Names   | Folder that contains the raw name data files, csv and txt name files. |
|   2   |   Family  | Folder that houses the raw family tree raw data, before any changes  |
|   3   | GraphViz_Helper.py | This file handles the bulk of the edge and node creation for the dot language|
|   4   | Sanitizer.py | This file will contain all the methods used to maniuplate the the Family_Clean.csv |
|   5   | Main.py   | Primary program that calls on methods from file 3 and file 4 to produce my data, it has two outputs to choose from based on which node method you call. Outputs to Dot.txt |
|  6    | Dot.txt  | plain text document that holds my output in the form of dot code.  |

## I use the following imports graphviz, random, OS, and CSV.
## Graphviz will require a pip install.
## data files provided by my instructor, for all my testing I used the asian name files and the generic clan file
### This program has two outputs based on which method you have Main.py call.
### When subgraphs are called the family tree as a whole looks bad but the clans are separated properly.
### When no subgraphs are used the family tree looks great.
### I found that my program tends to break at 150+ people, graphviz just kicks the bucket.
## Project #2 Page Ranking Algorithm

## Breakdown
-------------------------------------------------------------------------------------------------------------------------------------------------------
My project exists in /src/pagerank.py and starts from line 5 all the way to line 85. Rest of code is either imports or the Main function.

## Description
-------------------------------------------------------------------------------------------------------------------------------------------------------
For starting the project I implemented the recommended starter main function from Moodle. From there, I defined a new PageRank function (lines 5-85), which takes in all of the provided parameters from the project description.

For the PageRank function itself, I created a dictionary with keys with outlinks for each of the source pages and their target pages in the format:
    P = {Page: [Target, Target], Page: [Target], Page: []} and provided a key for target pages that were not source pages just so they would be scored
    as well and not ignored.

For tracking the scores themselves, I created another dictionary for each of the pages and a corresponding index value that correllated with an index in both I and R from the algorithm description in the slides:
    Indexes = {A: 0, B:1, C: 2}
    R = [1/lambda, 1/lambda, 1/lambda]
    I = [1/n, 1/n, 1/n]
    Where the values for each unique key corresponds to the specific list index in both R and I.

The implementation of the ranking itself closely follows the given slides presented in class, with some exceptions in order to increase the runtime of the program. Firstly for all List initialization, no for loops where used, as there are built in methods for python that allow arrays of multiple of the same element to be completed much more efficiently:
    R = [1/lambda]*len(P)
    I = [1/n]*len(P)

A major change I made in order to increase runtime, was for when every single item needed to be ranked, instead of switching array items over and over again, I took a running sum rather than looking through every single list/dictionary index. When the sum was done, I just applied it to each of the entires in R. I've listed it below as it was crucial into figuring out the problem:
        else:#We take a sum of the values for ALL terms
            sum += (1-lambda_val)*(I[indexes[key]])/len(P)
    for i in range(len(R)):
        R[i] += sum#Increment here for Efficiency

Another crucial component of the algorithm was setting the previous (I) to the current new values (R), which was another roadblock because when we simply set I = R and don't create a new object for R, our program only executes one loop since both lists are pointing to the same object rather than two separate. Thus, for each pass in the while loop a new object was created for R in order to correctly track entries shifting and changing.

## Libraries
-------------------------------------------------------------------------------------------------------------------------------------------------------
I used normal python libraries alongside **sys, gzip, and numpy linalg/norm**

## Dependencies
-------------------------------------------------------------------------------------------------------------------------------------------------------
Python 3 is needed in order to run the project, also **sys, gzip, and numpy linalg/norm** which may need to be installed in the terminal using pip.

## Building
-------------------------------------------------------------------------------------------------------------------------------------------------------
In order to run code from terminal provide **python3 pagerank.py links.srt.gz 0.2 0.005 inlinks.txt pagerank.txt 100** or just use 
**python3 pagerank.py** for default configurations.

## Running
-------------------------------------------------------------------------------------------------------------------------------------------------------
Use **python3 pagerank.py links.srt.gz 0.2 0.005 inlinks.txt pagerank.txt 100**

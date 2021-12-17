# final-project
Final Project for SI 507
Bryan Flowers

All Required Packages
--------------------------------------------------------------------------------------------------------------------------------
plotly
plotly.graph_objs
bs4
bs4.element
BeautifulSoup
requests
json

Description
--------------------------------------------------------------------------------------------------------------------------------
My Final Project is an NBA team builder game that outputs statistics and ratings for the team of 5 players that you have created. 
When the program begins you must choose a year to pick your players from. The range is from 1980 - 2021.
Once you have chosen a year, you will then choose 5 players to complete the team.
You will then be prompted to enter your team name.
Lastly once this is all complete, you will be shown a menu screen asking you to choose how you want to display your data.
You may choose from any of the 4 options as many times as you like.
Once you are done, type "exit" to terminate the program.

Data Structures
--------------------------------------------------------------------------------------------------------------------------------
My program utilizes a graph structure to organize the players chemistry between one another.
Each players connection (weight) is determined by their position and if they have played for the same franchise.
Once their chemistry is determined, they are placed into the graph as 2 vertices with their weight being the chemistry score.
All other additional data is stored in 1D or 2D dictionary structures.


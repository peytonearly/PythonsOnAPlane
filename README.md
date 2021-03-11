## Snakes on a Plane
### HackCU 007 Hackathon
#### Created by: Peyton Early, Tyler Kirkpatrick, Mason Milligan, Nathan Shaver

---------------

PlaneTracker is a program designed to display flights above a given longitude and latitude. 

## Inspiration
Our inspiration for this project came from Google's lost ability to tell you exactly what planes are above you when you ask it. 

## What it does
Our program taps into the OpenSky REST API to collect information about planes flying within a specified radius of the given coordinates. The program then takes the collected information and turns it into a plot that shows the location of each plane as well as an estimate of their direction. The program is tied to a Discord bot, which is hosted on a Raspberry Pi, and upon the command "!export" the Raspberry Pi will export the image to Discord and also display the image on a OLED screen connected to the Raspberry Pi.

## How we built it
Our program was built with Python. We used multiple Python libraries, such as the discord, matplotlib, numpy, and requests libraries. The Raspberry Pi was connected to SparkFun GPS and OLED modules. 

## Challenges we ran into
We ran into multiple problems at each stage of the development. We had difficulty getting information from certain API's, difficulty connecting our bot to our Discord server, difficulty displaying our information in a plot, and various problems with running the code on the Raspberry Pi, such as the graph being upside down.

## Accomplishments that we're proud of
We are proud of nearly everything that we accomplished. Most of us had no experience with API's, yet we were able to connect to and pull information from multiple APIs (even though some weren't used in the final code). We also had no experience with creating Discord bots, but were able to successfully connect our program and Raspberry Pi to the bot, so that commands given in a server would translate to running our code. For plotting our results, most of us have experience with MATLAB, but none of us have worked with matplotlib and numpy to create graphs. Finally, we had little experience with Raspberry Pi development going into the project, but we were able to build on past knowledge to get the Raspberry Pi working.

## What we learned
We learned a lot about connecting to APIs, displaying and outputting information using Python, and connecting multiple different systems to work together and share information amongst programs.

## What's next for Pythons on a Plane
Given more time, we would like have the output PNG file contain a map image of the location of the given coordinates, which would help demonstrate where the planes are over the ground. We would also like to implement more functionality with the Discord bot, such as being able to give it coordinates that it could use when running the program, as well as displaying historical flight data given a time and location. Finally, there is a slight power issue that kept coming up with the Raspberry Pi that could be addressed in the future.
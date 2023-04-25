# Welcome to my Final Project!
## Before we get started:

I have some basic system requirements for you. They are below. However, you can still reliably work with more or less than what is here. These are just what I use.

Software:
1. MacOS Ventura+ or Windows 10+
1. Python Version 3.10.0 + preferred

Hardware:
1. CPU: Intel I5 or M1
1. RAM 16GB
1. Please allocate some space for files.

Wifi:
* Proper wifi is required to access the API
* If you are caching, this is not required
* If you are using the API, enter your key

## As you run

1. You will be asked for a city to input, if you are caching, input Detroit or Ann Arbor. If you have a key, you can enter it in the file to use the API. Just note, this will take a while.
1. You then will see preview of 50 out of 1000 results. You can look through this to get an idea of what interests you.
1. You will be asked if you want to filter by restaurant type. If yes, input your answer. If it exists, it'll work and show you the filtered data. If not, you'll have the chance to keep inputting a valid statement. If you say no to the question, the program will move on.
1. Similarly, you will be asked a question on if you want to store by minimum rating. Please answer these in floats between 1 and 5. The numbers need to be in .0 or .5 also. If you don't get these right, you will be given the chance to adjust your input. If you said yes and followed prompts correctly, you will see the additional filtered data.
1. Once again, you will be asked a question on if you want to filter by price. The prices listed are in dollar signs. Please keep your answers to $, $$, $$$ or $$$$. If you enter a invalid input, you'll have the chance to fix this.
1. If any of the above inputs is a single value, the session will jump to the final step because there is nothing you can filter down. If your returned list is empty, such as a typo in your inputs or that the data just didn't have it, then you can enter a new answer till you get it right.

## The Final Step
1. When you are done, either by finishing the above steps, or getting one value, you will asked if you'd like to get directly sent to Google Maps with the location of the restaurant. If you say yes, it'll automatically load in your web browser and end the session. If you say no, your session will end anyways.
1. If you have more than one restaurants left, you can choose directly which restaurant you want to get directions for. There will be numbers next to your choices.

### Hope you have fun!
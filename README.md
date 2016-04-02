# AlexaHackCU

## Before you run the app

pip install -r requirements.txt


## Information
This skill for Alexa was written for the 2016 HackCU hackathon.
The intent is to build a skill that allows one to access the
Wolfram Alpha computational engine by voice. The idea behind
this skill is to have a virtual assistant one can ask to run
complex math (like integrations and derivations) without lifting
pencil from paper.

## Setup
This program was designed to run with the Lambda Function
on Amazon Web Services. To run this properly:
- Create a new Lambda Function
- When prompted for code, upload the Dist.zip file
- In configuration, change the handler to main.lambda_handler
- Create a new skill on Amazon Developer
- The invocation name can be anything, but it is recommended to
use Wolfram Alpha as the invocation name
- Copy and paste the Intent Schema, Slot Types, and Utterances
from the respective files into the interaction model

## Use
The skill can be used simply by stating:
"Alexa ask Wolfram Alpha [math question]"

The program attempts to parse the request into a format easily
understood by Wolfram Alpha, with the aim of returning undesired
results due to poorly formatted input. If the program cannot
parse the input, it will pass the full query to Wolfram Alpha
regardless.

## Files
If editing this, the files to edit are those in the Amazon
Distrubtion folder. All other files were first drafts and are
not useful for the skill
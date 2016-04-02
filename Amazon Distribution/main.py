"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import wolframalpha
import re

def lambda_handler(event, context):
	""" Route the incoming request based on type (LaunchRequest, IntentRequest,
	etc.) The JSON body of the request is provided in the event parameter.
	"""
	
	print("event.session.application.applicationId=" +
		event['session']['application']['applicationId'])
	
	"""
	Uncomment this if statement and populate with your skill's application ID to
	prevent someone else from configuring a skill that sends requests to this
	function.
	"""
	if (event['session']['application']['applicationId'] !=
			"amzn1.echo-sdk-ams.app.e006375b-483a-4baa-955c-0e1b63a57814"):
		raise ValueError("Invalid Application ID")

	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']},
						   event['session'])

	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
	""" Called when the session starts """

	session_attributes = {}
	print("on_session_started requestId=" + session_started_request['requestId']
		  + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
	""" Called when the user launches the skill without specifying what they
	want
	"""

	print("on_launch requestId=" + launch_request['requestId'] +
		  ", sessionId=" + session['sessionId'])
	# Dispatch to your skill's launch
	return get_welcome_response()


def on_intent(intent_request, session):
	""" Called when the user specifies an intent for this skill """

	print("on_intent requestId=" + intent_request['requestId'] +
		  ", sessionId=" + session['sessionId'])

	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']

	# Dispatch to your skill's intent handlers
	if intent_name == "Math":
		return math_input(intent, session)
	elif intent_name == "General":
		return general_input(intent, session)
	elif intent_name == "SetDec":
		return setDec(intent, session)
	elif intent_name == "AMAZON.CancelIntent":
		return end_session(session)
	elif intent_name == "AMAZON.StopIntent":
		return end_session(session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	else:
		raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
	""" Called when the user ends the session.

	Is not called when the skill returns should_end_session=true
	"""
	print("on_session_ended requestId=" + session_ended_request['requestId'] +
		", sessionId=" + session['sessionId'])

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
	""" If we wanted to initialize the session to have some attributes we could
	add those here
	"""

	session_attributes = {}
	card_title = "Welcome"
	speech_output = "You've reached the Wolfram Alpha speech converter. " \
					"Say an input to send to Wolfram Alpha."
	# If the user either does not reply to the welcome message or says something
	# that is not understood, they will be prompted again with this text.
	reprompt_text = "Say an input to send to Wolfram Alpha."
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def end_session(session):
	should_end_session = True
	speech_output = "Ending your Wolfram Alpha session."
	reprompt_text = None
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))
		

def math_input(intent, session):
	""" Does input that is math based
	"""
	# Set flags for if statements
	opFlag = True
	genFlag = True
	limMinFlag = True
	limMaxFlag = True
	intArgFlag = True
	algArgFlag = True
	algNumFlag = True
	
	# Define session_attributes
	try:
		session_attributes
	except NameError:
		session_attributes = {}
	
	# Set flags for if statements
	try:
		intent['slots']['Operation']['value']
	except KeyError:
		opFlag = False
	
	try:
		intent['slots']['GeneralInput']['value']
	except KeyError:
		genFlag = False
	
	try:
		intent['slots']['LimitMin']['value']
	except KeyError:
		limMinFlag = False
	
	try:
		intent['slots']['LimitMax']['value']
	except KeyError:
		limMaxFlag = False
	
	try:
		intent['slots']['IntegralArgument']['value']
	except KeyError:
		intArgFlag = False
	
	try:
		intent['slots']['AlgebraArgument']['value']
	except KeyError:
		algArgFlag = False
	
	try:
		intent['slots']['AlgebraNum']['value']
	except KeyError:
		algNumFlag = False
	
	card_title = intent['name']
	should_end_session = False

	if opFlag == True and genFlag == True and limMinFlag == False and intArgFlag == False and algArgFlag == False and algNumFlag == False:
		# Is some sort of covered mathematical operation
		operation = intent['slots']['Operation']['value'].lower()
		general = intent['slots']['GeneralInput']['value'].lower()
		input = operation + general
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	elif opFlag == True and genFlag == True and limMinFlag == True and intArgFlag == False and algArgFlag == False and algNumFlag == False:
		# Is integral with numerical range with no defined argument of integration
		operation = intent['slots']['Operation']['value'].lower()
		general = intent['slots']['GeneralInput']['value'].lower()
		limitMin = intent['slots']['LimitMin']['value'].lower()
		limitMax = intent['slots']['LimitMax']['value'].lower()
		input = "integrate(" + general + ")," + limitMin + "," + limitMax + ")"
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	elif opFlag == True and genFlag == True and limMinFlag == False and intArgFlag == True and algArgFlag == False and algNumFlag == False:
		# Is integral or derivative with defined argument variable for itnegration or derivation
		operation = intent['slots']['Operation']['value'].lower()
		general = intent['slots']['GeneralInput']['value'].lower()
		argument = intent['slots']['IntegralArgument']['value'].lower()
		input = operation + general + "," + argument
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	elif opFlag == True and genFlag == True and limMinFlag == True and intArgFlag == True and algArgFlag == False and algNumFlag == False:
		# Is integral with numerical range and defined argument of integration
		operation = intent['slots']['Operation']['value'].lower()
		general = intent['slots']['GeneralInput']['value'].lower()
		argument = intent['slots']['IntegralArgument']['value'].lower()
		limitMin = intent['slots']['LimitMin']['value'].lower()
		limitMax = intent['slots']['LimitMax']['value'].lower()
		input = "integrate (" + general + "," + argument + "," + limitMin + "," + limitMax + ")"
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	elif opFlag == False and genFlag == True and limMinFlag == False and intArgFlag == False and algArgFlag == True and algNumFlag == True:
		general = intent['slots']['GeneralInput']['value'].lower()
		argument = intent['slots']['AlgebraArgument']['value'].lower()
		algNum = intent['slots']['AlgebraNum']['value'].lower()
		input = "solve " + general + " where " + argument + " = " + algNum
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	elif opFlag == True and genFlag == True and limMinFlag == False and intArgFlag == False and algArgFlag == True and algNumFlag == True:
		operation = intent['slots']['Operation']['value'].lower()
		general = intent['slots']['GeneralInput']['value'].lower()
		argument = intent['slots']['AlgebraArgument']['value'].lower()
		algNum = intent['slots']['AlgebraNum']['value'].lower()
		input = "solve " + operation + " " + general + " where " + argument + " = " + algNum
		speech = choose(input)
		speech_output = speech
		reprompt_text = "Say an input to send to Wolfram Alpha."
	else:
		input = "I didn't understand your query. " \
				"Please try again."
		speech_output = input
		reprompt_text = "Say an input to send to Wolfram Alpha."
	
	print("Math Input")
	print(input)
	print(speech)
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def general_input(intent, session):
	""" Does general input that Wolfram Alpha hopefully understands
	This results from Alexa not understanding the words
	"""
	try:
		session_attributes
	except NameError:
		session_attributes = {}
	
	should_end_session = False
	card_title = intent['name']
	
	input = intent['slots']['GeneralInput']['value']
	speech = choose(input)
	speech_output = speech
	reprompt_text = "Say an input to send to Wolfram Alpha."
	
	print("General Input")
	print(input)
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def setDec(intent, session):
	""" Changes the session attribute 'decimal' to setnumber of decimal points
	"""
	try:
		session_attributes
	except NameError:
		session_attributes = {}
	
	should_end_session = False
	card_title = intent['name']
	
	decimalPts = intent['slots']['Decimals']['value']
	session_attributes = create_decimal_attribute(decimalPts)
	speech_output = "I've changed your decimal settings. " \
					"Say an input to send to Wolfram Alpha."
	reprompt_text = "Say an input to send to Wolfram Alpha."
	
	print("Decimal Input")
	print(input)	
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def create_decimal_attribute(decimalPts):
    return {"decimals": decimalPts}


def mathtotext(text):
    mathoperators = {'+' : " plus " , '-' : " minus " , '*' : " times " , '/' : " over ", '^' : " raised to ", '=' : " equals", '(': " of " , ")" : "", "sin": "sine", "|": "upto", "sqrt": "square root" ,"~~": " approximately equal to "}
    uppercase = ['d[a-z]', '[a-z]']
    mathoppatterns = re.compile('|'.join(re.escape(key) for key in mathoperators.keys()))
    ucpatterns = re.compile(r'\b(' + '|'.join(uppercase) + r')\b')
    processed = mathoppatterns.sub(lambda x: mathoperators[x.group()], text)
    processed = ucpatterns.sub(lambda x: x.group(0).upper(), processed)
    return processed    


def choose(query):
    client = wolframalpha.Client("369TU4-JQAVJKXQ9Y")
    res = client.query(query)
    query1=query.split()
    if 'integrate' in query1 or 'differentiate' in query1:
        return calculus(res)
    else:
        return algebra(res)
        

def calculus(res):
    text = res.pods[0].text
    integral= ""
    if 'integral' in  text :
        text_array = text.split()
        text_array[0] = text_array[0].replace('_', ' from ')
        text_array[0] = text_array[0].replace('^', ' to ')
        text = " ".join(text_array)
        
    res = mathtotext(text)
    return res

def algebra(res):
    query = res.pods[0].text
    text= res.pods[1].text
    queryres = mathtotext(query)
    res = mathtotext(text)
    return queryres + " equals " + res

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'card': {
			'type': 'Simple',
			'title': 'SessionSpeechlet - ' + title,
			'content': 'SessionSpeechlet - ' + output
		},
		'reprompt': {
			'outputSpeech': {
				'type': 'PlainText',
				'text': reprompt_text
			}
		},
		'shouldEndSession': should_end_session
	}


def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}
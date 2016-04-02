"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

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
	
	card_title = intent['name']
	should_end_session = False

	if opFlag == True and genFlag == True and limMinFlag == False and intArgFlag == False:
		# Is some sort of covered mathematical operation
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		speech_output = "Filler1."
		reprompt_text = "Filler1."
	elif opFlag == True and genFlag == True and limMinFlag == True and intArgFlag == False:
		# Is integral with numerical range with no defined argument of integration
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		limitMin = intent['slots']['LimitMin']['value']
		limitMax = intent['slots']['LimitMax']['value']
		speech_output = "Filler2."
		reprompt_text = "Filler2."
	elif opFlag == True and genFlag == True and limMinFlag == False and intArgFlag == True:
		# Is integral or derivative with defined argument variable for itnegration or derivation
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		argument = intent['slots']['IntegralArgument']['value']
		speech_output = "Filler3."
		reprompt_text = "Filler3."
	elif opFlag == True and genFlag == True and limMinFlag == True and intArgFlag == True:
		# Is integral with numerical range and defined argument of integration
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		argument = intent['slots']['IntegralArgument']['value']
		limitMin = intent['slots']['LimitMin']['value']
		limitMax = intent['slots']['LimitMax']['value']
		speech_output = "Filler4."
		reprompt_text = "Filler4."
	else:
		print("Crash")
		speech_output = "I didn't understand your query. " \
					"Please try again."
		reprompt_text = "Say an input to send to Wolfram Alpha."
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
	speech_output = "FillerGen."
	reprompt_text = "FillerGen."
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
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def create_decimal_attribute(decimalPts):
    return {"decimals": decimalPts}


def get_color_from_session(intent, session):
	session_attributes = {}
	reprompt_text = None

	if "favoriteColor" in session.get('attributes', {}):
		favorite_color = session['attributes']['favoriteColor']
		speech_output = "Your favorite color is " + favorite_color + \
						". Goodbye."
		should_end_session = True
	else:
		speech_output = "I'm not sure what your favorite color is. " \
						"You can say, my favorite color is red."
		should_end_session = False

	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))

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
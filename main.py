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

	card_title = intent['name']
	should_end_session = False

	if 'Operation' in intent['slots'] and 'GeneralInput' in intent['slots'] and 'LimitMin' not in intent['slots'] and 'IntegralArgument' not in intent['slots']:
		# Is some sort of covered mathematical operation
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		print(operation)
		print(general)
		speech_output = "Filler."
		reprompt_text = "Filler."
	elif 'Operation' in intent['slots'] and 'GeneralInput' in intent['slots'] and 'LimitMin' in intent['slots'] and 'IntegralArgument' not in intent['slots']:
		# Is integral with numerical range with no defined argument of integration
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		limitMin = intent['slots']['LimitMin']['value']
		limitMax = intent['slots']['LimitMax']['value']
		print(operation)
		print(general)
		print(limitMin)
		print(limitMax)
		speech_output = "Filler."
		reprompt_text = "Filler."
	elif 'Operation' in intent['slots'] and 'GeneralInput' in intent['slots'] and 'LimitMin' not in intent['slots'] and 'IntegralArgument' in intent['slots']:
		# Is integral or derivative with defined argument variable for itnegration or derivation
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		argument = intent['slots']['IntegralArgument']['value']
		print(operation)
		print(general)
		speech_output = "Filler."
		reprompt_text = "Filler."
	elif 'Operation' in intent['slots'] and 'GeneralInput' in intent['slots'] and 'LimitMin' in intent['slots'] and 'IntegralArgument' in intent['slots']:
		# Is integral with numerical range and defined argument of integration
		operation = intent['slots']['Operation']['value']
		general = intent['slots']['GeneralInput']['value']
		argument = intent['slots']['IntegralArgument']['value']
		limitMin = intent['slots']['LimitMin']['value']
		limitMax = intent['slots']['LimitMax']['value']
		print(operation)
		print(general)
		print(argument)
		print(limitMin)
		print(limitMax)
		speech_output = "Filler."
		reprompt_text = "Filler."
	else:
		speech_output = "I didn't understand your query. " \
						"Please try again."
		reprompt_text = "Say an input to send to Wolfram Alpha."
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


def general_input(intent, session):
	""" Does general input that Wolfram Alpha hopefully understands
	This results from Alexa not understanding the words
	"""
	input = intent['slots']['GeneralInput']['value']
	print(input)
	speech_output = "Filler."
	reprompt_text = "Filler."


def setDec(intent, session):
	""" Changes the session attribute 'decimal' to setnumber of decimal points
	"""
	decimalPts = intent['slots']['SecDec']['Decimals']['value']
	session_attributes = create_decimal_attribute(decimalPts)
	print(session_attributes)
	speech_output = "I've changed your decimal settings. " \
					"Say an input to send to Wolfram Alpha."
	reprompt_text = "Say an input to send to Wolfram Alpha."
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))


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
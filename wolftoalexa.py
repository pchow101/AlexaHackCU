import wolframalpha
import re




def mathtotext(text):
    mathoperators = {'+' : " plus " , '-' : " minus " , '*' : " times " , '/' : " over ", '^' : " raised to ", '=' : " equals", '(': " of " , ")" : "", "sin": "sine"}
    uppercase = ['d[a-z]+', '[a-z]']
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
    res = mathtotext(text)
    return res

def algebra(res):
    query = res.pods[0].text
    text= res.pods[1].text
    queryres = mathtotext(query)
    res = mathtotext(text)
    return queryres + " equals " + res

if __name__ == "__main__":
    query = " two decimal digits e^2"

    res = choose(query)
    print (res)

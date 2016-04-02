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


def querytoresult(query):
    client = wolframalpha.Client("369TU4-JQAVJKXQ9Y")
    res = client.query(query)
    query1=query.split()
    if 'integrate' in query1 or 'differetiate' in query1:
        text = res.pods[0].text
    else:
        test1=res.pods[1].text.split(".")
        x=test1[1]
        test1[1]=x[:4]
        test=test1[0]+'.'+test1[1] 
        text = res.pods[0].text+' equals '+test
    #print text
    res = mathtotext(text)
    return res


if __name__ == "__main__":
    query = "e^2"
    res = querytoresult(query)
    print res

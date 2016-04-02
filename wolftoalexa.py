import wolframalpha
import re


client = wolframalpha.Client("369TU4-JQAVJKXQ9Y")


def mathtotext(text):
    mathoperators = {'+' : " plus " , '-' : " minus " , '*' : " times " , '/' : " over ", '^' : " raised to ", '=' : " equals", '(': " of " , ")" : "", "sin": "sine"}
    uppercase = ['d[a-z]+', '[a-z]']
    mathoppatterns = re.compile('|'.join(re.escape(key) for key in mathoperators.keys()))
    ucpatterns = re.compile(r'\b(' + '|'.join(uppercase) + r')\b')
    processed = mathoppatterns.sub(lambda x: mathoperators[x.group()], text)
    processed = ucpatterns.sub(lambda x: x.group(0).upper(), processed)
    return processed


def querytoresult(query):
    res = client.query(query)
    text = res.pods[0].text
    print text
    res = mathtotext(text)
    return res


if __name__ == "__main__":
    query = "differentiate "
    res = querytoresult(query)
    print res

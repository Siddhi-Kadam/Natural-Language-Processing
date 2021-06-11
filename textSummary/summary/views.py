# -*- coding: utf-8 -*-
import googletrans
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation as punc
from nltk.tokenize import word_tokenize
import gtts
import playsound
from django.shortcuts import render


# Create your views here.
def homePage(request):
    return render(request, 'homePage.html')


def way1(message, val):
    data = message
    translator = googletrans.Translator()
    tr = translator.translate(data, src='mr', dest='en')
    text = tr.text
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    tokens = [i.text for i in doc]
    print(tokens)

    punctuation = punc + '\n'

    words = {}
    for i in doc:
        if i.text.lower() not in stopwords:
            if i.text.lower() not in punctuation:
                if i.text not in words.keys():
                    words[i.text] = 1
                else:
                    words[i.text] += 1
    print(words)

    maxFreq = max(words.values())
    print(maxFreq)

    for i in words.keys():
        words[i] = words[i] / maxFreq
    print(words)

    sentenceTokens = [i for i in doc.sents]
    print(sentenceTokens)

    sentenceScores = {}
    for i in sentenceTokens:
        for j in i:
            if j.text.lower() in words.keys():
                if i not in sentenceScores.keys():
                    sentenceScores[i] = words[j.text.lower()]
                else:
                    sentenceScores[i] = words[j.text.lower()]
    print(sentenceScores)

    from heapq import nlargest
    selectLength = int(len(sentenceTokens) * (int(val) / 100))
    print(selectLength)

    summary = nlargest(selectLength, sentenceScores, key=sentenceScores.get)
    print(summary)

    finalSummary = [i.text for i in summary]
    print(finalSummary)

    summary = ' '.join(finalSummary)
    print("Summary:\n", summary)

    print('Length of Text: ', len(text))
    print('Length of Summary: ', len(summary))
    print('Summary word length: ', len(word_tokenize(summary)))

    tr = translator.translate(summary, src='en', dest='mr')
    text1 = tr.text
    print("***************************************************************************")
    print("Original Summary in marathi:\n", data, "\n")
    print("Original Summary:\n", text, "\n")
    print("Final Summary in english:\n", summary, "\n")
    print("Final Summary:\n", text1)
    convertedAudio = gtts.gTTS(text1, lang='mr')
    convertedAudio.save('xyz.mp3')
    return text1, summary, text


def way2(data, val):
    from inltk.inltk import tokenize
    doc = tokenize(data, "mr")
    print(doc)
    print('Length of original: ', len(doc))
    stopwords = ['आहे', 'या', 'आणि', 'व', 'नाही', 'आहेत', 'यानी', 'हे', 'तर', 'ते', 'असे', 'होते', 'केली', 'हा', 'ही',
                 'पण', 'करण्यात',
                 'काही', 'केले', 'एक', 'केला', 'अशी', 'मात्र', 'त्यानी', 'सुरू', 'करून', 'होती', 'असून', 'आले',
                 'त्यामुळे', 'झाली', 'होता',
                 'दोन', 'झाले', 'होत', 'त्या', 'आता', 'असा', 'याच्या', 'त्याच्या', 'ता', 'आली', 'की', 'पम', 'तो',
                 'झाला', 'त्री',
                 'तरी', 'म्हणून', 'त्याना', 'अनेक', 'काम', 'माहिती', 'हजार', 'सांगितले', 'दिली', 'आला', 'आज', 'ती',
                 'तसेच', 'एका',
                 'याची', 'येथील', 'सर्व', 'ने', 'डॉ', 'तीन', 'येथे', 'पाठील', 'असल्याचे', 'त्याची', 'काय', 'आपल्या',
                 'म्हणजे', 'यांना', 'म्हणाले',
                 'त्याचा', 'असलेल्या', 'मी', 'गेल्या', 'याचा', 'येत', 'लाख', 'कमी', 'जात', 'टा', 'होणार', 'किंवा', 'का',
                 'अधिक', 'घेऊन',
                 'पर्यटन', 'कोटी', 'झालेल्या', 'निर्ण्य', 'येणार', 'व्यकत']
    punctuation = punc + '\n'
    words = {}
    for i in doc:
        if i not in stopwords:
            if i not in punctuation:
                if i not in words.keys():
                    words[i] = 1
                else:
                    words[i] += 1
    print(words)

    maxFreq = max(words.values())
    print(maxFreq)

    for i in words.keys():
        words[i] = words[i] / maxFreq
    print(words)

    sentenceTokens = [i for i in doc]
    print(sentenceTokens)

    sentenceScores = {}
    for i in sentenceTokens:
        for j in i:
            if j in words.keys():
                if i not in sentenceScores.keys():
                    sentenceScores[i] = words[j]
                else:
                    sentenceScores[i] = words[j]
    print('Sentence Tokens:\n', sentenceScores)

    from heapq import nlargest
    selectLength = int(len(sentenceTokens) * val)
    print(selectLength)

    summary = nlargest(selectLength, sentenceScores, key=sentenceScores.get)
    print(summary)

    finalSummary = [i for i in summary]
    print(finalSummary)
    summary = ' '.join(finalSummary)
    print("Summary:\n", summary)
    for i in range(len(finalSummary)):
        finalSummary[i] = ' ' + finalSummary[i][1:]
    print(finalSummary)
    print('Length Summary: ', len(finalSummary))
    summary = ' '.join(finalSummary)
    print("Summary:\n", summary)

    print("Data:\n", data)
    translator = googletrans.Translator()
    tr = translator.translate(data, src='mr', dest='en')
    text = tr.text
    print("Translated Data(Original):\n", text)

    tr = translator.translate(summary, src='mr', dest='en')
    text = tr.text
    print("Translated Data(Original):\n", text)
    return summary, text


def summarize(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        val = request.POST.get('service')
        sum1, eng, text = way1(message, val)
        sum2, mar = way2(message, val)
        return render(request, 'answer.html', {'data': message, 'english': sum1, 'marathi': sum2, 'eng': eng,
                                               'mar': mar, 'text': text})


def audio1(request):
    if request.method == 'POST':
        original = request.POST.get('original')
        english = request.POST.get('english')
        marathi = request.POST.get('marathi')
        eng = request.POST.get('eng')
        mar = request.POST.get('mar')
        text = request.POST.get('text')
        playsound.playsound('xyz.mp3')
        return render(request, 'answer.html', {'data': original, 'english': english, 'marathi': marathi, 'eng': eng, 'mar': mar, 'text': text})

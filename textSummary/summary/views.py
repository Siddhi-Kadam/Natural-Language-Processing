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


def summarize(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        val = request.POST.get('service')
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
        selectLength = int(len(sentenceTokens) * (int(val)/100))
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
        # playsound.playsound('abc.mp3')
        return render(request, 'answer.html', {'data': data, 'text': text, 'summary': summary, 'final': text1})


def audio(request):
    if request.method == 'POST':
        original = request.POST.get('original')
        final = request.POST.get('final')
        text = request.POST.get('originalE')
        summary = request.POST.get('finalE')
        playsound.playsound('xyz.mp3')
        return render(request, 'answer.html', {'data': original, 'final': final, 'text': text, 'summary': summary})

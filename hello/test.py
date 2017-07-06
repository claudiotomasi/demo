from hmm import hmm_init
from utility import utility
import hidden_markov as hmlib
import codecs, pickle, argparse, glob, csv
from sklearn import metrics
import numpy as np
from flask import Flask, request, jsonify, render_template
import enchant

app = Flask('ciao', instance_relative_config=True)
def confusion(states):
    real = ""
    with codecs.open('remain/Pontifex_test_of_remains.txt' , "r", 'utf-8-sig') as f:
        for s in f:
            real+=s
    real = list(real)
    pred = ""
    with codecs.open('test/Pontifex_test_of_remains.txt_correct' , "r", 'utf-8-sig') as f:
        for s in f:
            #print s
            pred+=s
    pred = list(real)

    matrix = metrics.confusion_matrix(real,pred,states)
    with open('csv/confusion.csv', 'wb') as f:
        writer = csv.writer(f)

        writer.writerow(states)
        for i in range(0, matrix.shape[0]):
            writer.writerows(matrix[i:])

def pred_without_dictionary(list_of_words, model):

    pred = []
    for word in list_of_words:

        #se frase non vuota aggiungo un punto alla fine
        if word!= '':
            word+=' '
        obs = list(word)
        #print obs
        if obs!=[]:
            # Rimuovo spazi all'inizio
            if obs[0]==' ':
                obs = obs[1:]
            if obs[0]!='\n':
                pred += model.viterbi(obs)
    return pred

def pred_with_dictionary(list_of_words, language, model):
    if language == 'en':
        d = enchant.Dict("en_US")
    else:
        if language == 'it':
            d = enchant.Dict("it_IT")
    pred = []
    for word in list_of_words:
            #se frase non vuota aggiungo un punto alla fine

            if word!= '':
                if d.check(word)==False:
                    to_correct = True
                else:
                    to_correct = False
                word+=' '
                obs = list(word)
            if to_correct:

                #print obs
                if obs!=[]:
                    # Rimuovo spazi all'inizio
                    if obs[0]==' ':
                        obs = obs[1:]
                    if obs[0]!='\n':
                        pred += model.viterbi(obs)
            else:
                pred+=obs
    return pred


def find_difference(typed, correct):
    diff = []
    typed = list(typed)
    correct = list(correct[:(len(correct)-1)])
    for i in range(len(typed)):
        if typed [i] != correct[i]:
            diff.append(i)

    return ''.join(typed), diff


@app.route('/', methods=['GET'])
def demo():
    # Load default dataset sensors configuration
    return render_template('index.html',language = 'en')

@app.route('/correct', methods=['POST'])
def correct():

    dictionary = request.form.get('dictionary')

    language =  request.form['language']

    afile = open('training/'+language+'/model', 'rb')
    model = pickle.load(afile)
    afile.close()
    states = model.states
    # for filename in glob.glob('test/'+language+'/Pontifex_'+language+'_test_of_remains.txt'):
    #     tweet = ""
    #     with codecs.open(filename , "r", 'utf-8-sig') as f:
    #         print ("Start prediction of "+filename+"...")
    typed = request.form['typed']

    # for tweets in typed:
    #     tweet += utility.convert(tweets)
    #     #elimino newline
    # tweet = tweet.replace('\n','')
    #separo per frasi

        # list_of_words = tweet.split('.')
    list_of_words = typed.split()

    correct = ""
    if dictionary:
        pred = pred_with_dictionary(list_of_words, language, model)
    else:
        pred = pred_without_dictionary(list_of_words,  model)
    # pred_with_dictionary()

    #trasformo lista predizioni in stringa
    correct += ''.join(pred)
    print correct
    # with codecs.open(filename+'_correct', 'w', 'utf-8-sig') as f:
    #     correct = unicode(correct)
    #     f.write(correct)
    # print ("End prediction of "+filename+"\n")
    res_typed, diff = find_difference(typed, correct)
    return render_template('index.html', typed=typed, corrected = correct, language = language, dictionary = dictionary, res_typed = res_typed, res_correct = correct, diff = diff)
        #eeconfusion(states)

if __name__ == '__main__':

    app.run(debug=True)
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--train', help='Training or not', action='store_true')
    # parser.add_argument('-l', '--language', help='Select language', choices = ['en', 'it'], default = 'en')
    # parser.add_argument('-d', '--dictionary', help='Use the dictionary', action='store_true')
    # args = parser.parse_args()
    # language = args.language
    # dictionary = args.dictionary
    # #print dictionary, language
    # print "Language: "+language
    # if dictionary:
    #     used_dict = "Yes"
    # else:
    #     used_dict = "No"
    # print "Use dictionary: "+ used_dict
    # if args.train:
    #     print ("With Training")
    #     prior = hmm_init.prior_probability(language)
    #     transitions = hmm_init.transition_model(language)
    #     states=hmm_init.states(language)
    #     possible_obs = hmm_init.observation(language)
    #     emissions = hmm_init.emission_probability(utility.adjacents(), language)
    #     model = hmlib.hmm(states, possible_obs, prior, transitions, emissions)
    #     afile = open('training/'+language+'/model', 'wb')
    #     pickle.dump(model, afile)
    #     afile.close()
    #     print ("End of training\n")


        # print ("Without Training\n")

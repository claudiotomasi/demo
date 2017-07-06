import codecs, collections, sys
import numpy as np
import glob, os
from utility import utility
# def extract_test_training():
#     total_characters=0
#     for filename in glob.glob('originals/*.txt'):
#         with codecs.open(filename, 'r', 'utf-8-sig') as tweets:
#             with codecs.open('training/knowledge_base.txt', 'w', 'utf-8-sig') as know:
#                 with codecs.open('test/test_of_remains.txt', 'w', 'utf-8-sig') as test:
#                     size = (os.stat(filename).st_size/100.0)*80
#                     for line in tweets:
#                         for character in line:
#                             if total_characters<size:
#                                 total_characters +=len(character)
#                                 know.write(unicode(character))
#                             else:
#                                 test.write(unicode(character))


def count_character(language):
    number_of_characters = {}
    total_characters = 0.0
    for filename in glob.glob('training/'+language+'/*.txt'):
        with codecs.open(filename, 'r', 'utf-8-sig') as tweets:
            for line in tweets:
                line = utility.convert(line)
                for character in line:
                    total_characters = count_character_helper(character, number_of_characters, total_characters)
    #for k in number_of_characters:
    #    print repr(k), number_of_characters[k]
    #print total_characters, number_of_characters
    return number_of_characters, total_characters


def count_character_helper(character, number_of_characters, total_characters):
    if character != '\n':
        if character in number_of_characters.keys():
            number_of_characters[character] += 1
        else:
            number_of_characters[character] = 1
        total_characters += 1;
    return total_characters


def prior_probability(language):
    state_list = states(language)
    length_state = len(state_list)
    prior_prob= np.full(length_state, 0.0)
    numb_of_char, total = count_character(language)
    s = 0.0

    #Transform in frequences numb_of_char
    for k,v in numb_of_char.iteritems():
        prior_prob[state_list.index(k)]=numb_of_char[k]/total
    #Verify if prior_probability sums to 1
    #for i in range(0,length_state):
        #s+=prior_probability[i]
    #print s
    return np.matrix(prior_prob)
def states(language):
    numb_of_char, total = count_character(language)
    list_of_states = numb_of_char.keys()
    #print list_of_states
    return list_of_states

def calc_probabilities_transictions(row):
    sum = np.sum(row)
    return row / sum

def transition_model(language):
    numb_of_char , total= count_character(language)
    list_of_states = states(language)
    n_states = len(list_of_states)
    transitions = np.asmatrix(np.full((n_states, n_states), 1.0/sys.maxint))

    for filename in glob.glob('training/'+language+'/*.txt'):
        print ("Training of "+filename+"...")
        with codecs.open(filename, 'r', 'utf-8-sig') as tweets:
            for line in tweets:
                line = utility.convert(line)
                for i in range(0, len(line)-1):
                    filename_helper(i, line, list_of_states, transitions)
    transitions = np.apply_along_axis( calc_probabilities_transictions, axis=1, arr=transitions )
    #'print' transitions
    return transitions


def filename_helper(i, line, list_of_states, transitions):
    if line[i] != '\n' and line[i + 1] != '\n':
        row_index = list_of_states.index(line[i])
        col_index = list_of_states.index(line[i + 1])
        transitions[row_index, col_index] += 1


def observation(language):
    observations = states(language)
    return observations

def emission_probability(adj_list, language):
    obs = observation(language)
    n_obs = len(obs)
    #print obs
    epsilon = 1.0/1000
    emissions = np.asmatrix(np.full((n_obs, n_obs), 0.0))
    likelihood = 0.8
    for k,v in adj_list.iteritems():
        state = obs.index(k)
        emissions[state, state] += likelihood
        if k != ' ' and k!= '.':
            not_spacecharacter_helper(emissions, k, obs, state, v)
        else:
            space_character_helper(emissions, k, obs, state, v)

        epsilon=0.02/(len(obs)-len(v))
        for j in range(0,len(obs)):
            if emissions[state,j]==0:
                    emissions[state,j] = epsilon

    #print np.sum(emissions, axis=1)
    return emissions


def space_character_helper(emissions, k, obs, state, v):
    if k == ' ':
        emissions[state, state] = 0.9
        weight = 0.08
    else:
        weight = 0.18
    elements = v[1:]
    prob = weight / len(elements)
    for el in elements:
        obs_index = obs.index(el)
        emissions[state, obs_index] += prob


def not_spacecharacter_helper(emissions, k, obs, state, v):
    index_capital = v.index(k.upper())
    if k.islower():
        low = v[1: index_capital]
        up = v[index_capital:]
        weight_low = 0.15
        weight_up = 0.03
        prob_low = weight_low / len(low)
        prob_up = weight_up / len(up)
    else:
        low = v[: index_capital]
        up = v[index_capital + 1:]
        weight_low = 0.03
        weight_up = 0.15
        prob_low = weight_low / len(low)
        prob_up = weight_up / len(up)
    for el in low:
        obs_index = obs.index(el)
        emissions[state, obs_index] += prob_low
    for el in up:
        obs_index = obs.index(el)
        emissions[state, obs_index] += prob_up

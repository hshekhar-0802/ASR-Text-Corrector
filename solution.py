import json

class Agent:
    def __init__(self, phoneme_table, vocabulary):
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

    def asr_corrector(self, environment):
        init_sentence = environment.init_state
        self.best_state = init_sentence
        min_cost = environment.compute_cost(init_sentence)

        self.best_state, subs_idx = substitute_phonemes_by_words(init_sentence, self.best_state, self.phoneme_table, environment, min_cost, set(range(len(self.best_state.split()))))
        min_cost = environment.compute_cost(self.best_state)

        self.best_state, org_idx = substitute_original(init_sentence, self.best_state, min_cost, environment)
        min_cost = environment.compute_cost(self.best_state)

        reversed_table = reverse_phoneme(self.phoneme_table)
        self.best_state, subs_idx = substitute_phonemes_by_words(init_sentence, self.best_state, reversed_table, environment, min_cost, subs_idx-org_idx)
        min_cost = environment.compute_cost(self.best_state)
        
        self.best_state = substitute_phonemes_by_sentence(self.best_state, self.phoneme_table, environment, min_cost)
        min_cost = environment.compute_cost(self.best_state)
        
        self.best_state, front, back = add_vocabulary(self.best_state, self.vocabulary, environment, min_cost)
        min_cost = environment.compute_cost(self.best_state)
        return self.best_state
        

def reverse_phoneme(phoneme_table):
    reversed_table={}
    for key, substitutions in phoneme_table.items():
        for sub in substitutions:
            if sub not in reversed_table.keys():
                reversed_table[sub]=[key]
            else:
                reversed_table[sub].append(key)
    return reversed_table
    
def substitute_phonemes_by_words(init_sentence, sentence, phoneme_table, environment, min_cost, to_substitute):
    words_init=init_sentence.split()
    words=sentence.split()
    new_words = words[:]
    substitute = True
    lst=to_substitute
    substituted_word_indexes = set()
    while substitute:
        substitute=False
        new_lst=set()
        for i in lst:
            new_words = words[:]
            new_words[i] = words_init[i]
            for key, substitutions in phoneme_table.items():
                for sub in substitutions:
                    start=0
                    while start<len(new_words[i]):
                        start=new_words[i].find(sub, start)
                        if start == -1:
                            break
                        new_word = new_words[i][:start] + key + new_words[i][start+len(sub):]
                        original_new_word = new_words[i]
                        new_words[i] = new_word
                        new_sen = ' '.join(new_words)
                        new_cost =  environment.compute_cost(new_sen)
                        if new_cost<min_cost:
                            words = new_words[:]
                            min_cost = new_cost
                            substitute = True
                            new_lst.add(i)
                            substituted_word_indexes.add(i)
                        else:
                            new_words[i]=original_new_word
                        start+=len(key)
        lst=new_lst
    return ' '.join(words), substituted_word_indexes

def substitute_original(init_sentence, sentence, min_cost, environment):
    words_init=init_sentence.split()
    words_now=sentence.split()
    original_word_indexes = set()
    for i in range(len(words_init)):
        new_words = words_now[:]
        new_words[i]=words_init[i]
        new_sentence=' '.join(new_words)
        new_cost=environment.compute_cost(new_sentence)
        if new_cost<min_cost:
            min_cost=new_cost
            words_now=new_words[:]
            original_word_indexes.add(i)
    return ' '.join(words_now), original_word_indexes

def substitute_phonemes_by_sentence(sentence, phoneme_table, environment, min_cost):
    best_state = sentence
    substitutions_made = True    
    # Keep making substitutions until no more improvements can be made
    while substitutions_made:
        substitutions_made = False
        for key, substitutions in phoneme_table.items():
            for sub in substitutions:
                start = 0
                while start < len(best_state):
                    start = best_state.find(sub, start)
                    if start == -1:
                        break
                    new_sentence = best_state[:start] + key + best_state[start + len(sub):]
                    new_cost = environment.compute_cost(new_sentence)
                    if new_cost < min_cost:
                        best_state = new_sentence
                        min_cost = new_cost
                        substitutions_made = True 
                    start += len(key)
    return best_state

def add_vocabulary(sentence, vocabulary, environment, min_cost):
    original_sentence = sentence
    best_state = sentence
    front,back = False, False
    # Try adding words to the start
    for word in vocabulary:
        new_sentence = word + " " + original_sentence
        new_cost = environment.compute_cost(new_sentence)
        if new_cost < min_cost:
            best_state = new_sentence
            min_cost = new_cost
    if(len(original_sentence.split())<len(best_state.split())):
        front=True
    original_sentence = best_state
    # Try adding words to the end
    for word in vocabulary:
        new_sentence = original_sentence + " " + word
        new_cost = environment.compute_cost(new_sentence)
        if new_cost < min_cost:
            best_state = new_sentence
            min_cost = new_cost
    if(len(original_sentence.split())<len(best_state.split())):
        back=True
    return best_state, front, back

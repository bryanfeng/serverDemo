#-*- coding:utf-8 -*-
import sys
import codecs
import os
import math
import operator
import json


# 如果是一份答案的话，务必在答案的后面加上.txt   python Bleu.py Candidate ref.txt 
# 如果是多份答案的话，把多份答案放到一个文件夹中  python Bleu.py Candidate 文件夹

# 读取译文和参考译文
def fetch_data(cand, ref):
    """ Store each reference and candidate sentences as a list """
    references = []
    if '.txt' in ref:
        reference_file = codecs.open(ref, 'r', 'utf-8')
        references.append(reference_file.readlines())
    else:
        for root, dirs, files in os.walk(ref):
            for f in files:
                reference_file = codecs.open(os.path.join(root, f), 'r', 'utf-8')
                references.append(reference_file.readlines())
    candidate_file = codecs.open(cand, 'r', 'utf-8')
    candidate = candidate_file.readlines()
    return candidate, references


def count_ngram(candidate, references, n):
    clipped_count = 0
    count = 0
    r = 0
    c = 0
    for si in range(len(candidate)):
        # Calculate precision for each sentence
        #print si
        ref_counts = []
        ref_lengths = []
        #print references
        # Build dictionary of ngram counts
        for reference in references:
            #print 'reference' + reference
            ref_sentence = reference[si]
            ngram_d = {}
            words = ref_sentence.strip().split()
            ref_lengths.append(len(words))
            limits = len(words) - n + 1
            # loop through the sentance consider the ngram length
            for i in range(limits):
                ngram = ' '.join(words[i:i+n]).lower()
                if ngram in ngram_d.keys():
                    ngram_d[ngram] += 1
                else:
                    ngram_d[ngram] = 1
            ref_counts.append(ngram_d)
        # candidate
        cand_sentence = candidate[si]
        cand_dict = {}
        words = cand_sentence.strip().split()
        limits = len(words) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(words[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        clipped_count += clip_count(cand_dict, ref_counts)
        count += limits
        r += best_length_match(ref_lengths, len(words))
        c += len(words)
    if clipped_count == 0:
        pr = 0
    else:
        pr = float(clipped_count) / count
    bp = brevity_penalty(c, r)

    # 精度处理
    if pr > 1.000001:
        pr = 1.0
        
    if bp > 1.000001:
        bp = 1.0
        pass
    return pr, bp


def clip_count(cand_d, ref_ds):
    """Count the clip count for each ngram considering all references"""
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = 0
        for ref in ref_ds:
            if m in ref:
                m_max = max(m_max, ref[m])
        m_w = min(m_w, m_max)
        count += m_w
    return count


def best_length_match(ref_l, cand_l):
    """Find the closest length of reference to that of candidate"""
    least_diff = abs(cand_l-ref_l[0])
    best = ref_l[0]
    for ref in ref_l:
        if abs(cand_l-ref) < least_diff:
            least_diff = abs(cand_l-ref)
            best = ref
    return best


def brevity_penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    
    return bp


def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def BLEU(candidate, references):
    BleuResult = {}
    precisions = []
    for i in range(4):
        pr, bp = count_ngram(candidate, references, i+1)
        precisions.append(pr)
        # print 'P'+str(i+1), ' = ',round(pr, 2)
        BleuResult['P'+str(i+1)] = round(pr, 4)
    #print 'BP = ',round(bp, 2) 
    BleuResult['BP'] = round(bp, 4)
    bleu = geometric_mean(precisions) * bp
    BleuResult['BLEU'] = round(bleu, 4)
    return str(json.dumps(BleuResult))

class Bleu():

    def __init__(self, argv1, argv2):
        
        candidate, references = fetch_data(argv1, argv2)
        self.bleu = BLEU(candidate, references)

    def getBleu(self):
        return self.bleu;

        

if __name__ == "__main__":
    candidate, references = fetch_data(sys.argv[1], sys.argv[2])
    bleu = BLEU(candidate, references)
    print 'BLEU = ',round(bleu, 4)
    out = open('bleu_out.txt', 'w')
    out.write(str(bleu))
    out.close()

    my_dog = Bleu(sys.argv[1], sys.argv[2])
    print my_dog.getBleu()




import protein_tests as test

### PHASE 1 ###

def read_file(filename):
  f = open(filename, 'r')
  code = f.readlines()
  f.close()
  result = str()
  for i in code:
      result += i.strip()
  return result

def dna_to_rna(dna, start_index):
    result =[]
    found = 0
    for i in range(start_index,len(dna)-2):
        index3 = str(dna[i] + dna[i + 1] + dna[i + 2])
        if index3 == 'ATG' and found != 1:
            result.append('AUG')
            three = i%3
            found = 1
            continue
        if found == 1:
            if i %3 == three:
                result.append(index3.replace('T','U'))
                if result[-1] == 'UAA' or result[-1] == 'UAG' or result[-1] == 'UGA':
                    break
    return result
import json
def make_codon_dictionary(filename):
    f = open(filename,'r')
    dict1 = json.load(f)
    f.close()
    dict2 = {}
    for i in dict1:
        for j in dict1[i]:
            dict2[j.replace('T','U')] = i
    return dict2

def generate_protein(codons, codon_dict):
    result = []
    foundstart = 0
    for i in codons:
        if i == 'AUG' and foundstart == 0:
            result.append('Start')
            foundstart = 1
        elif i == 'UAA' or i == 'UAG' or i == 'UGA':
            result.append('Stop')
            break
        else:
            result.append(codon_dict[i]) 
    return result

def synthesize_proteins(dna_filename, codon_filename):
    raw_code = read_file(dna_filename)
    dict1 = make_codon_dictionary(codon_filename)
    result = []
    index = 0 #will be used to skip across codons to avoid reading the same proteins twice
    unused_codons = 0
    for i in range(len(raw_code)):
      if dna_to_rna(raw_code,i) != dna_to_rna(raw_code,i+1) and i >= index:
        result.append(generate_protein(dna_to_rna(raw_code,i),dict1))
        index += len(result[-1])*3 + i - index
    return result

### PHASE 2 ###

def common_proteins(protein_list1, protein_list2):
    result = []
    for i in protein_list1:
        if i in protein_list2 and i not in result:
            result.append(i)
    return result

def combine_proteins(protein_list):
    result = []
    for i in range(len(protein_list)):
        for j in protein_list[i]:
            result.append(j)
    return result

def amino_acid_dictionary(aa_list):
    dict1 = {}
    for i in aa_list:
        if i in dict1:
            dict1[i] +=1
        else:
            dict1[i] = 1
    return dict1

def find_amino_acid_differences(protein_list1, protein_list2, cutoff):
    dict1 = amino_acid_dictionary(combine_proteins(protein_list1))
    total_genes1 = sum(dict1.values())
    dict2 = amino_acid_dictionary(combine_proteins(protein_list2))
    total_genes2 = sum(dict2.values())
    frequency1 = []
    for i in dict1:
        dict1[i] = dict1[i]/total_genes1
        if i not in dict2.keys():
            print('not')
            dict2[i] = 0
    frequency2 = []
    for i in dict2: #adjusting dict to have every amino acid and its frequency (even if zero)
        dict2[i] = dict2[i]/total_genes2
        if i not in dict1.keys():
            print('not2')
            dict1[i] = 0
    print(dict1,dict2)
    result = []
    for i in dict1:
        if i == 'Start' or i == 'Stop':
            continue
        elif abs(dict1[i] -dict2[i]) > cutoff:
            result.append([i,dict1[i],dict2[i]])
    result.sort()
    return result
import os
def display_commonalities(commonalities):
    list1 = []
    for i in range(len(commonalities)):
        commonalities[i].pop(0)
        commonalities[i].pop(-1)
    commonalities.sort()
    result = str()
    for i in range(len(commonalities)):
      for j in range(len(commonalities[i])):
        if len(commonalities[i]) == 1:
          result += commonalities[i][j]+'\n'
        elif len(commonalities[i]) > 1 and j + 1 < len(commonalities[i]):
          result += commonalities[i][j]+'-'
        elif len(commonalities[i]) > 1 and j + 1 == len(commonalities[i]):
          result += commonalities[i][j]+'\n'

    print(result)

def display_differences(differences):
    differences.sort()
    result = str()
    for i in range(len(differences)):
      for j in range(3):
        if j == 0:
          result += differences[i][j]+": "
        else:
          differences[i][j] = f"{differences[i][j]*100:.2f}"
          result += differences[i][j].rstrip('0')+r"% in Seq"+str(j)
          if j == 1:
            result += ', '
          else:
            result += '\n'
    print(result)
    return

### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    test.test_all()
    test.run()
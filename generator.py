import func as fc
import time

'''
    -------------------------------------------------------------------------------------------------------
                                    Generator to start the word cloud process
    -------------------------------------------------------------------------------------------------------
'''

'''
    Two options: 
        Set - STATIC=True - for static word list
        Set - STATIC=False - for file reader word list (wordfile.txt)
'''
STATIC = True

if STATIC:
    word_list = [
                    'Alex', 'Jay', 'AI', 'Computer', 'Python', 'Java', 'C#', 'CPU', 'Jacob', 'Model', 'Network', 'Code', 
                    'System', 'React', 'JS', 'RAM', 'SQL', 'Algorithms', 'Database', 'Tech', 'Internet', 'Protocol',
                    'Binary', 'Data', 'Software', 'Storage', 'Theory', 'Access', 'Web', 'Security', 'User', 'Virtual',
                    'Error', 'Assert', 'Functionality', 'Feature', 'Mobile', 'Application', 'Program', 'XOR', 'Sets',
                    'Schema', 'Relation', 'Docker', 'Array', 'Stack', 'Queue', 'Graph', 'GPU', 'PHP',
                    'Error', 'Assert', 'Functionality', 'Feature', 'Mobile', 'Application', 'Program', 'XOR', 'Sets',
                    'Schema', 'Relation', 'Docker', 'Array', 'Stack', 'Queue', 'Graph', 'GPU', 'PHP'
    ]
                    
else:
    word_list = fc.read_wordfile()

'''
    Two options:
        Set - BASIC=True - for basic word cloud generator
        Set - BASIC=False - for advanced word cloud generator
'''
BASIC = True

if BASIC:
    start_time = time.time()
    fc.basic_word_cloud(word_list)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {round(elapsed_time, 2)} seconds")

else:
    start_time = time.time()
    fc.gen_word_cloud(word_list)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {round(elapsed_time, 2)} seconds")
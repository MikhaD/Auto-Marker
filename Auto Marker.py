"""Auto Marker"""
__author__ = 'Mikha Davids'
#11/05/2019
#What happens if the input statement has text?
from io import StringIO
import sys

print('-'*50)
print('{:^50}'.format('Auto Marker'))
print('-'*50)

s_fileName = input('Enter the name of the file to test: ')
s_inputType = input('Use default input & output files? (y/n): ').lower()

s_path = ''

i_pathEnd = s_fileName.rfind('\\')
if i_pathEnd == -1 :
    i_pathEnd = s_fileName.rfind('/')
if i_pathEnd != -1 :
    s_path = s_fileName[:i_pathEnd+1]

if s_inputType == 'n' :
    s_inputFile = s_path + input('Input file: ')
    s_outputFile = s_path + input('Output file: ')
else:        
    s_inputFile = f'{s_path}sampleinput.txt'
    s_outputFile = f'{s_path}sampleoutput.txt'

if s_fileName[-3:] != '.py' :
    s_fileName += '.py'

try :
    with open(s_fileName, 'r') as f_file :
        s_script = f_file.read()
    
    print('\nExecuting program', end='\n\n')

    s_script = s_script.replace('input()', 'f_input.readline()')
    output = StringIO()
    temp_stdout = sys.stdout
    sys.stdout = output
    
    with open(s_inputFile, 'r') as f_input :
        exec(s_script)
    #For some reason this doesn't work if I read the file in the same with as the exec statement
    with open(s_inputFile, 'r') as f_input :
        s_input = f_input.read()
    
    sys.stdout = temp_stdout
    
    with open(s_outputFile, 'r') as f_answer :
        s_answer = f_answer.read()

    a_answer = s_answer.splitlines()
    
    a_output = output.getvalue().splitlines()
    
    print('Comparing output', end='\n\n')
    a_ansLines, a_outLines = [], []
    for i, (ansLine, outLine) in enumerate(zip(a_answer, a_output), 1):
        if ansLine != outLine :
            a_ansLines.append([i, ansLine])
            a_outLines.append([i, outLine])
    
    if a_outLines != [] :
        print('Output not correct\nThe expected output was:')
        print(s_answer, end='\n\n')
        print('Your program produced:')
        print(output.getvalue())
        print('Input supplied to your program:')
        print(s_input, end='\n\n\n')
        print('Differences are as follows:\nYours:')
        for i, line in a_outLines :
            print('Line: {:<3}>'.format(i), line)
        print('Desired:')
        for i, line in a_ansLines :
            print('Line: {:<3}>'.format(i), line)
    else:
        print('Output correct')
    
except FileNotFoundError:
    print('File name invalid or sampleinput.txt or sampleoutput.txt file missing.')
#except :
    #print('Unspecified error')

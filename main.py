import sys
import subprocess
from openai import OpenAI
import ast
from datetime import datetime

client = OpenAI()

file = sys.argv[1]
file_code_original = sys.argv[2].replace("\\", "\\\\")
file_code_new = file_code_original
extension = file.split('.')[-1]

if extension == 'py':
    language = 'python'
    command = 'python3'
elif extension == 'rb':
    language = 'ruby'
    command = 'ruby'
elif extension == 'java':
    language = 'java'
    command = 'javac'
elif extension == 'swift':
    language = 'swift'
    command = 'swift'
elif extension == 'sh':
    language = 'shell'
    command = './'
elif extension == 'c':
    language = 'C'
    command = 'gcc'

result = subprocess.run(['./run_file.sh', file_code_original, command, file], capture_output=True, text=True, check=True)

if result.stdout == 'no error\n':
    print('Your file had no errors 🔥')
else:
    if len(file_code_original) > 1500:
        iterations = 0
        output_dicts = []
        while (result.stdout != 'no error\n') and (iterations < 10):
            message = client.chat.completions.create(
            model='gpt-4o',
                messages=[
                    {"role": "system", "content": "I am going to provide you with the content of a file of code, an error message, and the language of that code. I want you to return a dictionary that includes the change you make to one single line of code to address the error message. It is important that you only address one line of code. Also, your dictionary should include a very brief description of the change you made and the line number of the change. Your dictionary should be ordered by increasing line numbers changed.  Your response should only contain the dictionary. No other information is necessary. Your response must be ONLY a valid JSON object with these keys: code, description, line. It must not include '''json. You should be very careful to maintain indentation consistent with the rest of the file in your 'code' output."},
                    {"role": "user", "content": f"###Code: {file_code_new}\n ###Error message: {result.stdout} ###Language{language}"},
                ]
            )
            openai_output = ast.literal_eval(message.choices[0].message.content)
            file_code_new = subprocess.run(['./make_change.sh', file, str(openai_output['line']), openai_output['code'].replace('\\', '\\\\')], capture_output=True, text=True, check=True).stdout.replace('\\', '\\\\')
            result = subprocess.run(['./run_file.sh', file_code_new, command, file], capture_output=True, text=True, check=True)
            output_dicts.append(openai_output)
            if result.stdout == 'no error\n':
                output = output_dicts
            elif iterations == 9:
                output = 'not fixed'
            iterations += 1
    else:
        message = client.chat.completions.create(
        model='gpt-4o',
            messages=[
                {"role": "system", "content": "I am going to provide you with the content of a file of code, an error message, and the language of that code. I want you to address the error message and fix the cause or causes of the error, as well as search for and fix errors in the rest of the code. In your response, code should be simply the fixed code of the input file, descriptions should be a list of the descriptions of the changes made in order of increasing line numbers (and should not include the line numbers), and line numbers should be a list of the numbers of lines changed also in increasing order. Your response must be a ONLY a valid JSON object with these keys: code, descriptions, lines. It must not include '''json. You should maintain proper indentation in your output."},
                {"role": "user", "content": f"###Code: {file_code_new}\n ###Error message: {result.stdout} ###Language{language}"},
            ]
        )
        openai_output = ast.literal_eval(message.choices[0].message.content)
        file_code_new = openai_output['code']
        result = subprocess.run(['./run_file.sh', file_code_new.replace("\\", "\\\\"), command, file], capture_output=True, text=True, check=True)
        if result.stdout == 'no error\n':
            output = openai_output
        else: 
            output = 'not fixed'
    if output == 'not fixed':
        print('Your code was not fixed. The original file has not been changed. Try again.')
        with open(f'{file}', 'w') as writer:
            writer.write(file_code_original)
    else:
        print("✅ Your code was fixed. Your original file has been moved to changed-files.")
        current_time = datetime.now().strftime('%m.%d.%H.%M.%S')
        with open(f'changed-files/{current_time}', 'w') as writer:
            writer.write(file_code_original)
        with open(file, 'w') as writer:
            writer.write(file_code_new)
        if isinstance(output, list):
            for n, each in enumerate(output):
                print(f"### FIX {n} ###\nLine number: {each['line']}\nDescription: {each['description']}")
        else:
            for n, (line, description) in enumerate(zip(output['lines'], output['descriptions'])):
                print(f"### FIX {n} ###\nLine number: {line}\nDescription: {description}")

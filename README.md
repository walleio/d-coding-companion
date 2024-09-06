# ✅ d-coding-companion
A coding companion that can be used to fix bugs in the terminal.

# instructions:
1. type 'git clone https://github.com/oscarrivera2028/d-coding-companion.git'
2. type 'cd d-coding-companion'
3. Add your OpenAI api key to the main.py file on line 7. You can get this from https://platform.openai.com/settings/profile?tab=api-keys.
   3a. Under this line, there is a variable 'make_changes' set to 'False'. If you want the coding companion to actually change your file, change this to 'True'. Keep in mind, original     files are saved in the 'changed-files' directory.
5. create your file to be edited. For example 'vi file.py'
6. Write some faulty code 'print("Hello"'
7. Exit file and return to terminal
8. Allow d to run and change files - 'chmod +x run_file.sh make_change.sh d.sh'
9. Use d - './d file.py' and done! 🔥

Here are some examples of use (Currently works with java, c, shell, python, ruby, and swift):

https://github.com/user-attachments/assets/086e1fbf-4a43-4feb-bdb7-89c794204d63

https://github.com/user-attachments/assets/1054aaa8-9b95-4dd4-85c4-cee20179ac68

https://github.com/user-attachments/assets/b0cf97b7-72c7-472e-b0bf-8b943247cb2a

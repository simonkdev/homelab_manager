from InquirerPy import inquirer, prompt

choice = inquirer.select(
    message="Pick an option:",
    choices=["Option 1", "Option 2", "Option 3"],
).execute()

print("You chose:", choice)

name = inquirer.text(message="What's your name:").execute()
print(type(name))
confirm = inquirer.confirm(message="Confirm?").execute()

questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    }
]

answers = prompt(questions)

print("Hello", answers['first_name'])
def parse_quiz_file():
    with open('1vs1200.txt', 'r', encoding='KOI8-R') as file:
        file_content = file.read()

    quiz_file_content = file_content.split('\n\n')

    questions = [question for question in quiz_file_content if question.startswith('Вопрос')]
    answers = [answer for answer in quiz_file_content if answer.startswith('Ответ')]

    return dict(zip(questions, answers))

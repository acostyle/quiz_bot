import glob


def parse_quiz_file(path_to_folder):
    text_files_in_folders = glob.glob('{0}/*.txt'.format(path_to_folder))

    questions_with_anwers = {}
    for file in text_files_in_folders:
        with open(file, 'r', encoding='KOI8-R') as text_file:
            file_content = text_file.read()

        quiz_file_content = file_content.split('\n\n')

        questions = [
            question
            for question in quiz_file_content
            if question.startswith('Вопрос')
        ]

        answers = [
            answer
            for answer in quiz_file_content
            if answer.startswith('Ответ')
        ]

        questions_with_anwers.update(zip(questions, answers))
    
    return questions_with_anwers


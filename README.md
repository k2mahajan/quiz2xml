# quiz2xml

# Input Question Document

Arrange your questions/answers in a simple format as given in sample_quiz.txt (unicode, other languages supported).
Recommended way is to copy the Word document into simple text file.
A few points to note:
1. First non-empty line is considered as title of the quiz.
2. Write 'Q' at both the start and the end of question. It is to differentiate question from answers.
3. Answeres should ideally be bulleted with a., b. etc.
4. If the question type is other that Single Choice, add it before the end Q. It should be one of [single], [multiple], [matrix], [essay]. (No spaces.) Default is [single].
5. Add a '#' at the end of correct answer. For Multiple Choice questions, add it to all the correct answers.
6. For matrix sort questions, separate the items in a pair with a '>' as given in sample quiz Q4.

# Usage
python3 xml_generator.py <document_path>
E.g.
python3 xml_generator.py sample_quiz.txt

# Output
The output XML is named as <document_path>.converted.xml
E.g. sample_quiz.txt.converted.xml

# Upload
1. On the LMS Portal, go to Quizzes.
2. On the top right, click Actions.
3. Click Import/Export.
4. On the new screen, at the bottom, click Import button.
5. Import the local file by following the instructions.

Please reach out to me in case of any issues.
Feel free to contribute.

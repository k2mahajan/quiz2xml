import sys
import xml.etree.cElementTree as ET
import json
import fileinput

doc_name = 'qdoc.txt'

DEFAULT_POINTS = "1"

answer_types = {
    '[single]': 'single',
    '[multiple]': 'multiple',
    '[matrix]': 'matrix_sort_answer',
    '[essay]': 'essay'
}

def parse_doc(doc_name):
    fdoc = open(doc_name, encoding="utf8")
    lines = fdoc.readlines()
    title = None
    question_sets = list()
    mode = 'title'
    i = 0
    while i < len(lines):
        #print(lines[i])
        if not lines[i] or lines[i].replace(' ', '').replace('\t', '') in ['', '\n']:
            i += 1
            continue
        if mode == 'title':
            title = lines[i][:-1]

            print(f'Added title: {title}')
            mode = 'question'
            i += 1
            continue
        elif mode == 'question':
            if lines[i].startswith('Q'):
                qset = dict()
                que = ''
                while not lines[i].endswith('Q\n'):
                    que += lines[i]
                    i += 1
                    #print(lines[i])
                que += lines[i]
                que = que[1:-2]
                qset['answers'] = list()
                qset['answer_type'] = 'single'
                for at, at_value in answer_types.items():
                    if at in que:
                        qset['answer_type'] = at_value
                        que = que.replace(at, '')
                        if qset['answer_type'] == 'essay':
                            qset['answers'].append({
                                'answer': '',
                                'short_answer': '',
                                'attrib': {
                                    'correct': 'false'
                                    
                                    ,
                                    'points': '0',
                                    'gradingProgression': 'not-graded-none',
                                    'gradedType': 'text'}
                                })

                        break

                print(f'Adding question: {que}')
                #
                # sys.exit(0)
                qset['question'] = que
                mode = 'answer'
            i += 1
            continue
        elif mode == 'answer':
            if lines[i].startswith('Q'):
                mode = 'question'
                question_sets.append(qset)
                continue
            ans = lines[i][:-1]
            short_ans = ''
            correct = False
            if '#' in ans:
                correct = True
                ans = ans.replace('#', '')
            if '>' in ans:
                ans, short_ans = ans.split('>')
            print(f'Adding ans: {ans}, Short ans: {short_ans}, correct: {correct}')
            qset['answers'].append({
                'answer': ans,
                'short_answer': short_ans,
                'attrib': {
                    'correct': str(correct).lower(),
                    'points': DEFAULT_POINTS if correct else '0'
                    }
                })
            i += 1
            continue
    question_sets.append(qset)

    doc_parsed = {
        'title': title,
        'question_sets': question_sets
    }
    return doc_parsed

def get_xml_text(str, bold=False):
    if bold:
        return f'__CDATA_START_BOLD__{str}__CDATA__END_BOLD__'
    else:
        return f'__CDATA_START__{str}__CDATA__END__'

def post_process_xml(xml_name, bold=False):
    fxml = open(xml_name, encoding='utf-16')
    xml_content = fxml.read()
    fxml.close()

    start_replace = '<![CDATA['
    end_replace = ']]>'
    xml_content = xml_content.replace('__CDATA_START__', start_replace)
    xml_content = xml_content.replace('__CDATA__END__', end_replace)

    start_replace += '<p><strong>'
    end_replace = '</strong></p>' + end_replace
    xml_content = xml_content.replace('__CDATA_START_BOLD__', start_replace)
    xml_content = xml_content.replace('__CDATA__END_BOLD__', end_replace)

    fxml = open(xml_name, 'w', encoding='utf-16')
    fxml.write(xml_content)
    fxml.close()



def generate_xml(doc_name):
    quiz_root_xml = ET.parse('elements/quiz.xml')
    questions_xml = quiz_root_xml.find('data/quiz/questions')

    doc_parsed = parse_doc(doc_name) 
    
    title_xml = quiz_root_xml.find('data/quiz/title')
    title_xml.text = get_xml_text(doc_parsed['title'])
    post_title_xml = quiz_root_xml.find('data/quiz/post/post_title')
    post_title_xml.text = get_xml_text(doc_parsed['title'])

    qt = 1
    print('Questions:')
    for qs in doc_parsed['question_sets']:
        qs_xml = ET.parse('elements/question_set.xml')
        qs_xml.getroot().attrib['answerType'] = qs['answer_type']
        qs_title_xml = qs_xml.find('title')
        qs_title_xml.text = get_xml_text(f'Q{qt}')
        question_xml = ET.parse('elements/question.xml')
        question_xml.getroot().text = get_xml_text(qs['question'], bold=True)
        print(f"Q{qt} ({qs['answer_type']}): {qs['question']}")
        qt += 1
        qs_xml.getroot().append(question_xml.getroot())
        answers_xml = qs_xml.find('answers')
        for ans in qs['answers']:
            ans_xml = ET.parse('elements/answer.xml')
            for atr, val in ans['attrib'].items(): 
                ans_xml.getroot().attrib[atr] = val
            ans_text_xml = ans_xml.find('answerText')
            ans_text_xml.text = get_xml_text(ans['answer'])
            short_text_xml = ans_xml.find('stortText')
            short_text_xml.text = get_xml_text(ans['short_answer'])
            answers_xml.append(ans_xml.getroot())
        questions_xml.append(qs_xml.getroot())

    converted_doc_name =  doc_name + '.converted.xml'
    quiz_root_xml.write(converted_doc_name, encoding='utf-16')
    post_process_xml(converted_doc_name)
    print(f"Number of questions: {len(doc_parsed['question_sets'])}")
    print(f'Generated XML: {converted_doc_name}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage:')
        print(f'python3 {sys.argv[0]} <sample_doc_path>')
        sys.exit(1)
    doc_name = sys.argv[1]
    generate_xml(doc_name)
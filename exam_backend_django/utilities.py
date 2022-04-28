def evaluate_answer(answer: dict, solution: dict, exam_content: dict, mode="exam") -> int:
    """Evaluates a student answer"""
    answer, solution, exam_content = answer[mode], solution[mode], exam_content[mode]
    total_marks = 0
    for index, question in exam_content.items():
        marks = question["marks"]
        print(index, question, evaluate_question(answer.get(index, None), solution[index], qtype=question["qtype"]) * marks)
        total_marks += evaluate_question(answer.get(index, None), solution[index], qtype=question["qtype"]) * marks
    return total_marks

def evaluate_question(qanswer, qsolution, qtype: str):
    """Evaluate one question"""
    type_to_default = {
        "YN": False,
        "CO": "0",
        "CM": [],
        "SA": ""
    }
    if qanswer is None:
        qanswer = type_to_default[qtype]
    if qtype in ("YN", "CO"):
        return qanswer == qsolution
    elif qtype == "CM":
        return sum(1 if el in qsolution else -1  for el in qanswer) / len(qsolution)
    elif qtype == "SA":
        return qanswer.lower() == qsolution.lower()
    else:
        raise NotImplementedError(f"qtype {qtype} is not implemented")


def check_malformed_answer(answer: dict, exam_content: dict, mode="exam") -> bool:
    answer, exam_content = answer[mode], exam_content[mode]
    for index, question in exam_content.items():
        qtype = question["qtype"]
        if answer.get(index, None) is None:
            return False, f"Answer is malformed: does not include question {index}"
        qanswer = answer[index]
        if qtype in ("YN", "CO"):
            if isinstance(qanswer, int):
                continue
        elif qtype == "CM":
            if isinstance(qanswer, list) and all(isinstance(el, int) for el in qanswer):
                continue
        elif type == "SA":
            if isinstance(qanswer, str):
                continue
        return False, f"Answer is malformed: question {index} has wrong answer types"
    return True, "OK"

# def delete_question(question_sheet: dict, index: str, mode: str="exam") -> dict:
#     question_sheet = question_sheet[mode]
#     del question_sheet[index]
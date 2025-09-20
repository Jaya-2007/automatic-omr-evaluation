import cv2
import numpy as np

def evaluate_omr_sheet(image_path, answer_key):

    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubble_contours = [c for c in contours if cv2.contourArea(c) > 100]  # filter noise

    bubble_contours = sorted(bubble_contours, key=lambda c: cv2.boundingRect(c)[1])

    
    student_answers = {}
    question_number = 1
    options_per_question = 4  
    bubbles_per_row = options_per_question

    for i in range(0, len(bubble_contours), bubbles_per_row):
        q_bubbles = bubble_contours[i:i+bubbles_per_row]
        filled_values = []

        for idx, c in enumerate(q_bubbles):
            mask = np.zeros_like(thresh)
            cv2.drawContours(mask, [c], -1, 255, -1)
            filled = cv2.countNonZero(cv2.bitwise_and(thresh, mask))
            filled_values.append(filled)

        
        max_idx = np.argmax(filled_values)
        option = chr(ord('A') + max_idx)
        student_answers[question_number] = option
        question_number += 1

    
    score = 0
    for q, selected in student_answers.items():
        correct = answer_key.get(q, None)
        if correct and selected == correct:
            score += 1

    subject_scores = {}
    total_questions = len(answer_key)
    questions_per_subject = total_questions // 5
    for s in range(5):
        start = s*questions_per_subject + 1
        end = (s+1)*questions_per_subject + 1
        sub_score = sum([1 for q in range(start, end) if student_answers.get(q) == answer_key.get(q)])
        subject_scores[f"subject{s+1}"] = sub_score

    return {
        "student_answers": student_answers,
        "subject_scores": subject_scores,
        "total_score": score
    }


if __name__ == "__main__":

    answer_key = {i: 'A' for i in range(1, 101)}

    result = evaluate_omr_sheet("sample_omr_sheet.jpg", answer_key)
    print("OMR Evaluation Result:")
    print(result)

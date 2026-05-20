import pandas as pd
import numpy as np

def main():
    while True:

        # TASK 1
        while True:
            filename = input("\nEnter a class file to grade (i.e. class1 for class1.txt) hoặc 'exit' để thoát: ").strip()
            
            if filename.lower() == 'exit':
                print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
                return  
                
            if not filename.endswith(".txt"):
                filename += ".txt"
                
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    raw_lines = [line.strip() for line in f if line.strip()]
                
                df_raw = pd.Series(raw_lines, name='raw_data').to_frame()
                print(f"Successfully opened {filename}")
                break  
            except FileNotFoundError:
                print("File cannot be found.")

        print("\n**** ANALYZING ****")
        
        answer_key = np.array("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(","))
        
        df_split = df_raw['raw_data'].str.split(',', expand=True)
        total_rows = len(df_split)
        
        row_status_mask = np.ones(total_rows, dtype=bool)

        # TASK 2
        invalid_lines = 0     
        
        for idx in range(total_rows):
            row_data = df_split.iloc[idx]
            raw_line_str = df_raw['raw_data'].iloc[idx]
            
            if len(row_data) != 26:
                print(f"Invalid line of data: does not contain exactly 26 values:\n{raw_line_str}")
                invalid_lines += 1
                row_status_mask[idx] = False
                continue
                
            student_id = str(row_data[0]).strip()
            remaining_part = student_id[1:]
            
            if not student_id.startswith("N") or len(remaining_part) != 8 or not remaining_part.isdigit():
                print(f"Invalid line of data: N# is invalid\n{raw_line_str}")
                invalid_lines += 1
                row_status_mask[idx] = False
                continue

        valid_lines = total_rows - invalid_lines
        
        if invalid_lines == 0:
            print("No errors found!")

        # TASK 3
        all_student_ids = df_split[0].str.strip().values
        
        answers_matrix = df_split.iloc[:, 1:26].fillna("").apply(lambda x: x.str.strip()).values
        
        correct_mask = (answers_matrix == answer_key)
        blank_mask = (answers_matrix == "")
        wrong_mask = (~correct_mask) & (~blank_mask)

        matrix_scores = (correct_mask * 4) + (blank_mask * 0) + (wrong_mask * -1)
        calculated_scores = matrix_scores.sum(axis=1)

        valid_scores = calculated_scores[row_status_mask]
        
        total_skips_per_col = blank_mask[row_status_mask].sum(axis=0)
        total_wrongs_per_col = wrong_mask[row_status_mask].sum(axis=0)

        print("\n**** REPORT ****")
        print(f"Total valid lines of data: {valid_lines}")
        print(f"Total invalid lines of data: {invalid_lines}")
        
        if valid_lines > 0:
            high_scores_count = np.sum(valid_scores > 80)
            mean_score = np.mean(valid_scores)
            highest_score = np.max(valid_scores)
            lowest_score = np.min(valid_scores)
            score_range = highest_score - lowest_score
            median_score = np.median(valid_scores)
            
            if isinstance(median_score, float) and median_score.is_integer():
                median_score = int(median_score)

            print(f"\nTotal student of high scores: {high_scores_count}")
            print(f"Mean (average) score: {round(mean_score, 3)}")
            print(f"Highest score: {highest_score}")
            print(f"Lowest score: {lowest_score}")
            print(f"Range of scores: {score_range}")
            print(f"Median score: {median_score}")
            
            max_skip = np.max(total_skips_per_col)
            if max_skip > 0:
                most_skipped_qs = [
                    f"{q+1} - {max_skip} - {round(max_skip / valid_lines, 3)}"
                    for q in range(25) if total_skips_per_col[q] == max_skip
                ]
                print(f"Question that most people skip: {', '.join(most_skipped_qs)}")
            else:
                print("Question that most people skip: None")
                
            max_wrong = np.max(total_wrongs_per_col)
            if max_wrong > 0:
                most_wrong_qs = [
                    f"{q+1} - {max_wrong} - {round(max_wrong / valid_lines, 3)}"
                    for q in range(25) if total_wrongs_per_col[q] == max_wrong
                ]
                print(f"Question that most people answer incorrectly: {', '.join(most_wrong_qs)}")
            else:
                print("Question that most people answer incorrectly: None")

        # TASK 4
        output_filename = filename.replace(".txt", "_grades.txt")
        
        final_output_results = np.where(row_status_mask, calculated_scores.astype(str), "Lỗi định dạng")
        
        df_output = pd.DataFrame({
            'student_id': all_student_ids,
            'result': final_output_results
        })
        
        df_output.to_csv(output_filename, header=False, index=False)
        print(f"\n[THÀNH CÔNG] Đã chấm điểm lớp học và xuất file kết quả tổng hợp: {output_filename}")
                    
        print("\n" + "="*50)

if __name__ == "__main__":
    main()

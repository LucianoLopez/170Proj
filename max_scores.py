import sys
import os
from shutil import copyfile
import output_scorer

def take_max_scores(path1, path2):
    keep_file_path = "./true_outputs"
    size_categories = ["small", "medium", "large"]
    path_to_inputs = "./all_inputs"
    outputs = []
    outputs.append(path1)
    outputs.append(path2)
    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        for input_folder in os.listdir(category_dir):
            category_path = path_to_inputs + "/" + size
            input_name = os.fsdecode(input_folder)
            max = 0.0
            file_to_keep = None
            for path_to_outputs in outputs:
                if input_name == ".DS_Store":
                    continue
                output_file = output_category_path + "/" + input_name + ".out"
                score, msg = output_scorer.score_output(category_path+"/"+input_name, output_file)
                if score and score > max:
                    max = score
                    file_to_keep = output_file
            copyfile(output_file, keep_file_path+"/"+file_to_keep)



if __name__ == '__main__':
    take_max_scores(sys.argv[1], sys.argv[2])

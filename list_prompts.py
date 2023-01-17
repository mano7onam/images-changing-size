import glob

PROMPTS_SOURCE = 'glob::::/Users/andrey.matveev/Downloads/plants_512_512_PP/*.txt'
PROMPTS_FILE_OUT = 'prompts_plants.txt'


def process_files_get_prompts(files_or_globs):
    all_files = []
    res_all_prompts = []
    for file in files_or_globs:
        if file.startswith('glob::::'):
            glob_str = file.split('::::')[1]
            cur_files = glob.glob(glob_str)
            all_files.extend(cur_files)
        elif file.startswith('prompt::::'):
            cur_prompt = file.split('::::')[1]
            res_all_prompts.append(cur_prompt)
        else:
            all_files.append(file)

    for file in all_files:
        with open(file, 'r') as f:
            for line in f:
                to_add = line
                if line.endswith('\n'):
                    to_add = line[:-1]
                res_all_prompts.append(to_add)
    return res_all_prompts


all_prompts = process_files_get_prompts([PROMPTS_SOURCE])
with open(PROMPTS_FILE_OUT, 'w') as f:
    for prompt in all_prompts:
        f.write(prompt)
        f.write('\n')

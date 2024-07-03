import os
import re
import argparse


def load_preds(pred_file):
    preds = []
    with open(pred_file, 'r', encoding='utf-8') as inf:
        for line in inf:
            line = line.strip()
            if line:
                preds.append(line)
    return preds


def evaluate(gold_file, eval_dir, result_file):
    results = {}
    gold = load_preds(gold_file)
    for file in os.listdir(eval_dir):
        filename = os.fsdecode(file)
        if re.match(r'.*(?<!_viz)\.txt', filename):
            preds = load_preds(os.path.join(eval_dir, filename))
            name = filename[:-4]
            score = 0.0
            for x, y in zip(gold, preds):
                if x == y:
                    score += 0.5
            results[name] = score
    with open(result_file, 'w', encoding='utf-8') as otf:
        for name in sorted(results.keys()):
            otf.write(f'{name} {results[name]}\n')


if __name__ == '__main__':
    ps = argparse.ArgumentParser(description='Evaluation script')
    ps.add_argument('gold-file', help='Gold predictions')
    ps.add_argument('pred-dir', help='A directory containing prediction files')
    ps.add_argument('output_file', help='A file to write the evaluation results to')
    args = ps.parse_args()
    evaluate(*vars(args).values())

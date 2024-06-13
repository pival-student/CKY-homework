import argparse
import os

OUTPUT_FILE_NAME = 'valentin_pickard.txt'
VISUAL_OUTPUT_FILE_NAME = 'valentin_pickard_viz.txt'


def visualize_parse(sentence_string, parse, output_file):
    """
    Helper function to write to the visualisation file for a parse (Bonus exercise)
    :param sentence_string: The parsed sentence as string
    :param parse: The return value of the CKYParser parse() method
    :param output_file: The file to write to
    """
    if parse:
        # parse_count = 1
        output_file.write('NOT IMPLEMENTED\n\n')
        pass
    else:
        output_file.write(f'{sentence_string}\nParses: 0\n\n')


class CKYParser:
    """This class comprises a CKY parser and some helper methods for the homework assignment"""

    def __init__(self, grammar_path):
        self.start_symbol = None
        self.non_terminals = []
        # use dict for quick non-terminal index lookup
        self.nt_indices = {}
        # store unary and binary rules separately
        self.rules_unary = []
        self.rules_binary = []
        self.load_grammar(grammar_path)
        pass

    def load_grammar(self, fpath):
        """
        Loads the grammar file to initialise parser
        :param fpath: The path to the grammar file
        """
        with open(fpath, 'r', encoding='utf-8') as inf:
            for line in inf:
                line = line.strip()
                if len(line) > 0:
                    if not self.start_symbol:
                        self.start_symbol = line
                        self.non_terminals.append(self.start_symbol)
                    else:
                        split = line.split(' -> ')
                        if len(split) == 2:
                            if split[0] not in self.non_terminals:
                                self.non_terminals.append(split[0])
                            rhs = split[1].split(' ')
                            if len(rhs) == 1:
                                self.rules_unary.append((split[0], rhs[0]))
                            if len(rhs) == 2:
                                self.rules_binary.append((split[0], rhs[0], rhs[1]))
        for idx, nt in enumerate(self.non_terminals):
            self.nt_indices[nt] = idx
        pass

    def parse(self, sentence):
        """
        The actual CKY implementation, according to the wikipedia pseudocode.
        Note that we are using zero-based indexing (unlike the pseudocode)
        :param sentence: The sentence to parse, as a list of words
        :return: The backpointer chart or False if sentence not in language
        """
        n = len(sentence)
        # initialize charts
        par = [[[False for _ in self.non_terminals] for _ in sentence] for _ in sentence]  # called P in pseudocode
        back = [[[[] for _ in self.non_terminals] for _ in sentence] for _ in sentence]
        # initialize bottom row of the chart
        for s, word in enumerate(sentence):
            recognized = False
            for rule in self.rules_unary:
                if word == rule[1]:
                    v = self.nt_indices[rule[0]]
                    par[0][s][v] = True
                    recognized = True
            if not recognized:  # early stop if some word not recognized
                return False
        # actual parse
        for le in range(2, n + 1):  # substring length, called l in pseudocode
            for s in range(n - le + 1):  # substring start (in relation to sentence)
                for p in range(1, le):  # substring partition point (in relation to substring)
                    for rule in self.rules_binary:
                        a = self.nt_indices[rule[0]]
                        b = self.nt_indices[rule[1]]
                        c = self.nt_indices[rule[2]]
                        if par[p - 1][s][b] and par[le - p - 1][s + p][c]:
                            par[le - 1][s][a] = True
                            back[le - 1][s][a].append([p, b, c])
        if par[n - 1][0][0]:
            return back
        else:
            return False

    def process_sentences(self, fpath, out_dir):
        """
        Helper method for processing a sentence file, output is written to two files
        in the specified output directory. Filenames are predefined via constants
        :param fpath: The path to the sentence file
        :param out_dir: The output directory to which the results are written
        """
        # make output directory and parent directories for it if needed
        basedir = os.path.dirname(out_dir)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(fpath, 'r', encoding='utf-8') as inf:
            with open(os.path.join(basedir, OUTPUT_FILE_NAME), 'w', encoding='utf-8') as otf, \
                    open(os.path.join(basedir, VISUAL_OUTPUT_FILE_NAME), 'w', encoding='utf-8') as votf:
                for line in inf:
                    line = line.strip()
                    split = line.split(' ')
                    parse = self.parse(split)
                    if parse:
                        otf.write('1\n')
                    else:
                        otf.write('0\n')
                    visualize_parse(line, parse, votf)  # bonus exercise
        pass


def main(grammar_path, sentences_path, output_dir):
    parser = CKYParser(grammar_path)
    parser.process_sentences(sentences_path, output_dir)


if __name__ == '__main__':
    ps = argparse.ArgumentParser(description='Parses a file of sentences with a provided context-free grammar')
    ps.add_argument('grammar', help='A context-free grammar file')
    ps.add_argument('sentences', help='A file containing one sentence per line')
    ps.add_argument('output_dir', help='A directory to write the parse result file to')
    args = ps.parse_args()
    main(*vars(args).values())

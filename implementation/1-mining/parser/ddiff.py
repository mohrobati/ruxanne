from dictdiffer import diff
import json

class DDiff:

    def __init__(self, before_parsedTree, new_parsedTree):
        self.before_parsedTree = before_parsedTree
        self.new_parsedTree = new_parsedTree
        self.before_block_types = self.__get_block_types(before_parsedTree)
        self.new_block_types = self.__get_block_types(new_parsedTree)
        self.tokens = self.__get_data_info()
        self.curr_path = []
        self.prev_depth = 0
        self.path_ascending = True

    def __get_data_info(self):
        return json.load(open('./scheme/nonTerminals.json'))

    def __reset(self):
        self.curr_path = []
        self.prev_depth = 0
        self.path_ascending = True

    # Transforms tree like diffs to linearized paths
    def __reduce_diff_dfs(self, diff, contents):
        if type(diff) == str:
            if diff in self.tokens:
                self.curr_path.append(diff)
        if type(diff) == list:
            for item in diff:
                self.__reduce_diff_dfs(item, contents)
        if type(diff) == dict:
            for key in diff:
                curr_depth = len(self.curr_path)
                if key in self.tokens:
                    self.curr_path.append(key)
                    curr_depth += 1
                self.__reduce_diff_dfs(diff[key], contents)
                if self.prev_depth > curr_depth:
                    if self.path_ascending:
                        contents.add("-".join(self.curr_path))
                        self.path_ascending = False
                    self.curr_path = self.curr_path[:curr_depth]
                elif self.prev_depth < curr_depth:
                    self.path_ascending = True
                self.prev_depth = curr_depth
        if type(diff) == tuple:
            self.__reduce_diff_dfs(diff[0], contents)
            self.__reduce_diff_dfs(diff[1], contents)

    def __get_block_types(self, parsedTree):
        block_types = set()
        for block in parsedTree:
            for key in list(block.keys()):
                block_types.add(key)
        return block_types
    
    def __get_blocks_with_type(self, parsedTree, t):
        indices = set()
        for idx, block in enumerate(parsedTree):
            for key in list(block.keys()):
                if key == t:
                    indices.add(idx)
        return [parsedTree[i] for i in list(indices)]

    def __get_changed_blocks_contexts(self, ddiffs):
        changed_blocks = set()
        for ddiff in ddiffs:
            if isinstance(ddiff[1], list) and len(ddiff[1]) > 1:
                changed_blocks.add("-".join([str(ddiff[1][0]), str(ddiff[1][1])]))
            elif isinstance(ddiff[1], list):
                changed_blocks.add(str(ddiff[1][0]))
            else:
                changed_blocks.add(ddiff[1])
        return changed_blocks

    # Outputs changed code with it's respective context
    def __get_changed_blocks_with_context(self, ddiffs, c):
        indices = set()
        for idx, ddiff in enumerate(ddiffs):
            if isinstance(ddiff[1], list) and len(ddiff[1]) > 1:
                if c == "-".join([str(ddiff[1][0]), str(ddiff[1][1])]):
                    indices.add(idx)
            elif isinstance(ddiff[1], list):
                if c == str(ddiff[1][0]):
                    indices.add(idx)
            else:
                if c == '':
                    indices.add(idx)
        return [ddiffs[i] for i in list(indices)]

    # The output is the linearized paths (Gets the output of function above)
    def __get_ddiffs_union(self, ddiffs):
        union = set()
        for ddiff in ddiffs:
            for item in ddiff[2]:
                contents = set()
                self.__reduce_diff_dfs(item, contents)
                self.__reset()
                for content in contents:
                    union.add(content)
            if ddiff[1]:
                union.add("-".join(list(filter(lambda x: x in self.tokens, ddiff[1]))))
        return list(union)

    def get_ddiff(self, scope=None):
        output = []
        # To have modified methods
        for t in self.before_block_types.union(self.new_block_types):
            ddiffs = list(diff(self.__get_blocks_with_type(self.before_parsedTree, t), 
                 self.__get_blocks_with_type(self.new_parsedTree, t)))
            for context in self.__get_changed_blocks_contexts(ddiffs):
                if scope:
                    if scope == "" or str(context) == scope:
                        output.append((
                            context,
                            self.__get_ddiffs_union(self.__get_changed_blocks_with_context(ddiffs, context))
                        ))
                else:
                    output.append((
                            context,
                            self.__get_ddiffs_union(self.__get_changed_blocks_with_context(ddiffs, context))
                        ))
        return output

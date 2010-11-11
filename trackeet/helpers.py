
def process_stub(stub):
    """
    process stub and extract tags and comments.

    * a tag is one or two words
    * a comment is more than two words
    * tags and comments are comma separated

    >>> process_stub("tag1, a tag2, this is a comment")
    {'comments': ['this is a comment'], 'tags': ['tag1', 'a tag2']}
    >>> process_stub("tag1, this is a comment, a tag2")
    {'comments': ['this is a comment'], 'tags': ['tag1', 'a tag2']}
    >>> process_stub("this is a comment, tag1, a tag2, this is another comment")
    {'comments': ['this is a comment', 'this is another comment'], 'tags': ['tag1', 'a tag2']}
    >>> process_stub("tag1")
    {'comments': [], 'tags': ['tag1']}
    >>> process_stub("tag1, tag2")
    {'comments': [], 'tags': ['tag1', 'tag2']}
    >>> process_stub("this is a comment")
    {'comments': ['this is a comment'], 'tags': []}
    """
    results = {'tags':[], 'comments':[]}
    lexers = stub.split(',')
    for lexer in lexers:
        lex = lexer.split()
        if len(lex) < 3: # this is a tag
            results['tags'].append(lexer.strip())
        else: # this is a comment
            results['comments'].append(lexer.strip())
    return results


d = {'dict1':
     {'part1':
      {'.wbxml': 'application/vnd.wap.wbxml',
       '.rl': 'application/resource-lists+xml'},
      'part2':
      {'.wsdl': 'application/wsdl+xml',
       '.rs': 'application/rls-services+xml',
       '.xop': 'application/xop+xml',
               '.svg': 'image/svg+xml'}},
     'dict2':
         {'part1':
          {'.dotx': 'application/vnd.openxmlformats-..',
           '.zaz': 'application/vnd.zzazz.deck+xml',
           '.xer': 'application/patch-ops-error+xml'}}}


def demo():
    mime_type = 'image/svg+xml'
    try:
        key_chain = find_mime_type(d, mime_type)
    except KeyError:
        print('Could not find this mime type: {0}'.format(mime_type))
        exit()
    print('Found {0} mime type here: {1}'.format(mime_type, key_chain))
    nested = d
    for key in key_chain:
        nested = nested[key]
    print('Confirmation lookup: {0}'.format(nested))


def find_mime_type(d, mime_type):
    reverse_linked_q = list()
    reverse_linked_q.append((list(), d))
    while reverse_linked_q:
        this_key_chain, this_v = reverse_linked_q.pop()
        # finish search if found the mime type
        if this_v == mime_type:
            return this_key_chain
        # not found. keep searching
        # queue dicts for checking / ignore anything that's not a dict
        try:
            items = this_v.items()
        except AttributeError:
            continue  # this was not a nested dict. ignore it
        for k, v in items:
            reverse_linked_q.append((this_key_chain + [k], v))
    # if we haven't returned by this point, we've exhausted all the contents
    raise KeyError


if __name__ == '__main__':
    demo()

def snake_2_camel_case(snake_case: str) -> str:
    if '.' in snake_case:
        return '.'.join(map(snake_2_camel_case, snake_case.split('.')))
    
    if '_' not in snake_case:
        camel_case = snake_case
    else:
        segs = snake_case.split('_')
        camel_case = segs[0] + ''.join(x.title() for x in segs[1:])
    return camel_case

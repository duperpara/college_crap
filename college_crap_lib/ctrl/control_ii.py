

def rutiruti_jury(li: list) -> list:
    if len(li) <= 1:
        return []
    li_rev = list(reversed(li))
    jury = li[-1]/li_rev[-1]
    jury_li = [jury]
    # if -1 <= jury <= 1:
    new_li = [v1-v2*jury for v1, v2 in zip(li, li_rev)][:-1]
    nxt_jury = rutiruti_jury(new_li)
    if nxt_jury:
        jury_li += nxt_jury
    return jury_li


def eval_rutiruti_jury(li):
    jury_result = rutiruti_jury(li)
    print(f'{jury_result=}')
    if max(jury_result) < 1 and min(jury_result) > -1:
        print(f'Stable!')
    else:
        print('Unstable')


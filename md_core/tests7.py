
import wikitextparser as wtp
text = "{{Ficha de medicamento| Drugscom = {{drugs.com|monograph|alitretinoin}}}}"
parsed = wtp.parse(text)
for n, template in enumerate(parsed.templates, start=1):
    print(f'template {n}:')
    print(template)
    # if not template: continue
    na = template.name
    normal = template.normal_name()
    print(f'normal: {normal}')
    for arg in template.arguments:
        va = arg.value + '\n'
        arg.value = va.strip() + '\n'
        print(va)
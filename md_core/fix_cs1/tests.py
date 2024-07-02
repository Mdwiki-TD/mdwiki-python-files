"""
python3 core8/pwb.py fix_cs1/tests

"""
from newapi import printe
from fix_cs1.fix_p import fix_it


def test():
    text = """
    * <ref name=Stat2022>{{cite journal |last1=Lotterman |first1=S |last2=Sohal |first2=M |title=Ear Foreign Body Removal |date=January 2022 |pmid=29083719}}</ref>
    * {{cite journal|title=Wisdom as a woman of substance : a socioeconomic reading of Proverbs 1-9 and 31:10-31|last=Yoder|first=Christine Roy|lccn=2004042477 }}
    {{استشهاد بدورية محكمة|عنوان=تحسين html الذي يتم إنشاؤه تلقائيًا بواسطة برامج wysiwywyg|صحيفة=|مسار= https://dl.acm.org/doi/10.1145/988672.988720|مؤلف=Spiesser|الأول=Jacqueline|تاريخ=2004-05-17|لغة=en|ناشر=ACM|صفحات=355–364|مؤلف2=Kitchen|الأول2=Les|دوي=10.1145/988672.988720|isbn=978-1-58113-844-3|مسار أرشيف= https://web.archive.org/web/20240313153723/https://dl.acm.org/doi/10.1145/988672.988720|تاريخ أرشيف=2024-03-13}}
    """

    newtext = fix_it(text, site="ar")
    # ---
    printe.showDiff(text, newtext)


if __name__ == "__main__":
    test()

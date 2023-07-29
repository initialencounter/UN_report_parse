from pdfminer.high_level import extract_text

import re

import os


def re_search(reg, texts):
    """
    正则表达式封装
    :param reg: 正则表达式
    :param texts: 要匹配的文本
    :return: 匹配结果
    """
    target = re.search(reg, texts)
    if target:
        return str(target.group(1))
    else:
        return False


def print_result(x, y, z="未匹配到"):
    if x:
        x = x.replace('\n', ' ')
        x = x.replace('...', '')
        print(y + x)
    else:
        print(y + z)


def pdf_parser(file_bytes, debug=False):
    """
    解析 UN 报告的关键消息，返回一个JSON
    :param file_bytes: UN报告文件路径或二进制文件
    :param debug: 调试模式，开启会将文本写入到test.txt文件
    :return: UN 报告的关键信息 JSON
    """
    text = extract_text(file_bytes)
    if debug:
        file_name = 'test.txt'
        if not os.path.exists(file_name):
            os.mknod(file_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(text)

    name = ''
    model = ''
    ref_version2 = ''
    params = ''
    size = ''
    issue_date2 = ''
    un_numbers_pass = '通过'

    if text.find('广东储能检测技术有限公司') > -1:
        name = re_search(r'(?<=样品描述\sSample\sDescription\n\n样品名称\n\n)([\s\S]*?)(?=\n\nSample\sModel)', text)
        un_numbers = re_search(r'(?<=报告编号Report\sNo.: )([\s\S]*?)(?=\n)', text)
        if un_numbers:
            page = re_search(r'(?<=第\s1\s页\s共\s)(.*?)(?=页)', text)
            if page:
                page = int(page) + 1
                un_numbers_counts = text.count(un_numbers)
                if page > un_numbers_counts:
                    un_numbers_pass = False
            else:
                un_numbers_pass = False
        else:
            un_numbers_pass = False

        model = re_search(r'(?<=Sample\sModel:\n\n)([\s\S]*?)(?=\n\n委托单位)', text)

        ref_version = re_search(r'(?<=试验和标准手册)([\s\S]*?)(?=\n)', text)
        if ref_version:
            ref_version2 = ref_version[1:]
        else:
            ref_version2 = None

        params = re_search(r'(?<=End Charge Current\n)([\s\S]*?)(?=额定容量)', text)
        if params:
            params = params.replace(' ', '')
            params = params.replace('\n', ' ')
        else:
            params = None

        size = re_search(r'(?<=\n)(.*?)(?=mm\n)', text)

        issue_date = re_search(r'(?<=签发日期：\nIssue Date:)([\s\S]*?)(?=\s\n广东储能检测技术有限公司)', text)
        if issue_date:
            issue_date2 = issue_date.split('\n')[-1]
        else:
            issue_date2 = None

    elif text.find('深圳市鑫宇环检测有限公司') > 0:
        name = re_search(r'(?<=Model\sName\n\n)([\s\S]*?)(?=\n深圳市鑫宇环检测有限公司)', text)
        un_numbers = re_search(r'(?<=报告编号\sReport\sNo.：)([\s\S]*?)(?=\n)', text)
        if un_numbers:
            page = re_search(r'(?<=第\s1\s页\s共\s)(.*?)(?=页)', text)
            if page:
                page = int(page) + 1
                un_numbers_counts = text.count(un_numbers)
                if page > un_numbers_counts:
                    un_numbers_pass = False
            else:
                un_numbers_pass = False
        else:
            un_numbers_pass = False

        model = re_search(r'(?<=Testing\sLaboratory\n\n)([\s\S]*?)(?=\n\n样品型号)', text)
        if model:
            model = model.split('\n')[-1]

        ref_version = re_search(r'(?<=UN\s"Manual\sof\sTests\sand\sCriteria")([\s\S]*?)(?=Subsection\s38.3)', text)
        if ref_version:
            ref_version2 = ref_version[1:]
        else:
            ref_version2 = ''

        params = re_search(r'(?<=Almost)([\s\S]*?)(?=mAh\n)', text)
        if params:
            params = params.replace(' ', '')
            params = params.replace('\n', ' ')
        else:
            params = ''

        size = "该报告不含尺寸"

        issue_date = re_search(r'(?<=Issued\sDate)([\s\S]*?)(?=\s\n有效性)', text)
        if issue_date:
            issue_date2 = issue_date.split('\n')[-1]
        else:
            issue_date2 = ''

    elif text.find('广东联鼎检测科技有限公司') > 0:
        name = re_search(r'(?<=样品名称)([\s\S]*?)(?=\nTrade Mark/商标)', text)
        un_numbers = re_search(r'(?<=Report\sNo.：)([\s\S]*?)(?=\n)', text)
        if un_numbers:
            page = re_search(r'(?<=Page\s2\sof\s)(.*?)(?=\n)', text)
            if page:
                page = int(page) + 1
                un_numbers_counts = text.count(un_numbers)
                if page > un_numbers_counts:
                    un_numbers_pass = False
            else:
                un_numbers_pass = False
        else:
            un_numbers_pass = False

        model = re_search(r'(?<=Model/Type\sreference/型号\s.............)([\s\S]*?)(?=\s\n)', text)

        ref_version = re_search(r'(?<=Standard\s..............)([\s\S]*?)(?=/Section 38.3)', text)
        if ref_version:
            ref_version2 = ref_version[1:]
        else:
            ref_version2 = ''

        params = re_search(r'(?<=Ratings/规格\s......)([\s\S]*?)(?=\nAddress:)', text)
        if params:
            params = params.replace(' ', '')
            params = params.replace('\n', ' ')
        else:
            params = ''

        size = "该报告不含尺寸"

        issue_date = re_search(r'(?<=Date\sof\sissue\s..................)([\s\S]*?)(?=\s\n)', text)
        if issue_date:
            issue_date2 = issue_date.split('\n')[-1]
        else:
            issue_date2 = ''
    elif text.find('广州三帕认证技术服务有限公司') > 0:
        name = re_search(r'(?<=Sample\sName)([\s\S]*?)(?=\nModel)', text)
        if name:
            name = name.replace('样品名称', '')
        un_numbers = re_search(r'(?<=Report\sNo.：)([\s\S]*?)(?=\n)', text)
        if un_numbers:
            page = re_search(r'(?<=Page\s2\sof\s)(.*?)(?=\spages)', text)
            if page:
                page = int(page) + 1
                un_numbers_counts = text.count(un_numbers)
                if page > un_numbers_counts:
                    un_numbers_pass = False
            else:
                un_numbers_pass = False
        else:
            un_numbers_pass = False

        model = re_search(r'(?<=Model/型号 ..)([\s\S]*?)(?=\s\n)', text)

        ref_version = re_search(r'(?<=Standard/检测标准 ...)([\s\S]*?)(?=/Section 38.3)', text)
        if ref_version:
            ref_version2 = ref_version[1:]
        else:
            ref_version2 = ''

        params = re_search(r'(?<=Ratings/额定参数 ...)([\s\S]*?)(?=\n)', text)
        if params:
            params = params.replace(' ', '')
            params = params.replace('\n', ' ')
        else:
            params = ''

        size = re_search(r'(?<=Dimension/尺寸 .....)([\s\S]*?)(?=\s\n)', text)

        issue_date = re_search(r'(?<=Date\sof\sissue/签发日期 ....)([\s\S]*?)(?=\s\n)', text)
        if issue_date:
            issue_date2 = issue_date.split('\n')[-1]
        else:
            issue_date2 = ''

    print_result(name, "样品名称：\n  ")
    print_result(un_numbers_pass, '编号核对：\n   ', '编号缺失')
    print_result(params, "参数：\n   ")
    print_result(ref_version2, "测试标准:\n   ")
    print_result(issue_date2, "签发日期：\n   ")
    print_result(size, "尺寸：\n    ")
    print_result(model, "型号：\n   ")

    data = {
        "name": name,
        "un_numbers_pass": un_numbers_pass,
        "params": params,
        "ref_version2": ref_version2,
        "issue_date2": issue_date2,
        "size": size,
        "model": model
    }
    return data


if __name__ == '__main__':
    pdf_parser("./src/AGC.pdf")

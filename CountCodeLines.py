#encoding=utf-8

import os
import sys
import os.path


def count_file_lines(file_path):
    "统计文件的有效行数"
    line_count = 0
    # 设置一个标志位，当遇到以"""或者'''开头或者结尾的时候，置为False
    flag = True
    # 使用utf-8格式的编码方式读取文件，如果读取失败，将使用gbk编码方式读取文件
    try:
        fp = open(file_path, "r", encoding="utf-8")
        encoding_type = "utf-8"
        fp.close()
    except:
        encoding_type = "gbk"

    with open(file_path, "r", encoding=encoding_type) as fp:
        for line in fp:
            # 空行不统计
            if line.strip() == "":
                continue
            else:
                # 如果以'''或者"""结尾（比如：aaa"""或者"""bbb），且flag为False，那么不统计该行
                if line.strip().endswith("'''") and flag == False:
                    # 标志以'''结尾的行结束
                    flag = True
                    continue
                if line.strip().endswith('"""') and flag == False:
                    flag = True
                    continue
                # 如果以'''或者"""开头或者结尾，那么不统计
                if flag == False:
                    continue
                # 将"#encoding"或者"#-*-"统计进去
                # if与elif的搭配成的语句块，当匹配到if或者elif语句判断为True的时候，那么不会执行下面elif以及else里面的语句；
                # if...if...if..搭配成的语句块，会一个个去匹配是否满足if里面的语句
                if line.strip().startswith("#encoding") \
                        or line.strip().startswith("#-*-"):
                    line_count += 1
                # 如果同时以'''或者"""开头或者结尾（比如："""aaa"""），那么不统计
                elif line.strip().startswith('"""') and line.strip().endswith('"""') and line.strip() != '"""':
                    continue
                elif line.strip().startswith("'''") and line.strip().endswith("'''") and line.strip() != "'''":
                    continue
                # 如果以“#”号开头的，不统计
                elif line.strip().startswith("#"):
                    continue
                # 如果遇到'''或者"""开头的，将flag置为False
                elif line.strip().startswith("'''") and flag == True:
                    flag = False
                    continue
                elif line.strip().startswith('"""') and flag == True:
                    flag = False
                    continue
                else:
                    line_count += 1
    return line_count


def count_code_lines(path, file_types=[]):
    # 统计所有文件代码行
    if not os.path.exists(path):
        print("您输入的目录或者文件路径不存在")
        return 0
    line_count = 0
    file_lines_dict = {}
    # 判断path是文件还是目录
    if os.path.isfile(path):
        # print("path:",path)
        # 获取文件的类型
        file_type = os.path.splitext(path)[1][1:]
        # print(file_type)
        # print (file_type in file_types)
        # 如果没有输入统计文件的类型，那么自定义文件的类型
        if len(file_types) == 0:
            file_types = ["py", "cpp", "c", "java", "ruby", "ini", "go", \
                          "html", "css", "js", "txt", "vbs", "php",
                          "asp", "sh"]
        # 如果输入的文件在有效的文件类型内，调用count_file_lines函数进行统计
        if file_type in file_types:
            line_count = count_file_lines(path)
        return line_count
    # 当path是目录，使用os.walk遍历所有的文件以及目录
    else:
        # 获取所有文件的绝对路径
        file_path = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path.append(os.path.join(root, file))
        # 遍历file_path中所有的文件
        for f in file_path:
            # 获取文件的类型
            file_type = os.path.splitext(f)[1][1:]
            # 如果没有输入统计文件的类型，那么自定义文件的类型
            if len(file_types) == 0:
                file_types = ["py", "cpp", "c", "java", "ruby", "ini", "go", "html", "css", "js", "txt", "vbs", "php",
                              "asp", "sh"]
            # 如果不存在该类型，遍历下一个
            if file_type not in file_types:
                continue
            # 打印有效的文件绝对路径
            print(f)
            # 调用count_file_lines函数，统计每个文件的行数
            line_num = count_file_lines(f)
            line_count += line_num
            # 使用file_lines_dict存放所遍历的文件以及对应的行数
            file_lines_dict[f] = line_num

        return line_count, file_lines_dict


if __name__ == "__main__":
    # for i in sys.argv:
    #    print (i)
    print(sys.argv)
    # E:\python>python test.py e:\\python\\test1.py py，如果不输入count_path，退出程序
    if len(sys.argv) < 2:
        print("请输入待统计行数的代码绝对路径！")
        sys.exit()
    #获取统计文件的路径
    count_path = sys.argv[1]
    #统计文件类型存放到一个列表中
    file_types = []
    if len(sys.argv) > 2:
        for i in sys.argv[2:]:
            file_types.append(i)

print(count_path, file_types)
# print(count_code_lines(count_path,file_types))
print(count_file_lines("e:\\b.py"))

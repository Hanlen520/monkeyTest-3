# -*- coding: utf-8 -*-
__author__ = 'shikun'
import os
import time
import re
import monkeyConfig
import matplotlibBase




# 得到手机信息
def getPhoneMsg(cmd_log):
    l_list = []
    f = open(cmd_log, "r")
    lines = f.readlines()
    for line in lines:
        line = line.split('=')
        #Android 系统，如anroid 4.0
        if (line[0] == 'ro.build.version.release'):
            l_list.append(line[1])
            #手机名字
        if (line[0]=='ro.product.model'):
            l_list.append(line[1])
            #手机品牌
        if (line[0]=='ro.product.brand'):
            l_list.append(line[1])
    return l_list

#开始脚本测试
def start_monkey(cmd, phone_msg_log, logdir, now1, logcatname):
    # os.remove(phone_msg_log)
    #print "使用Logcat清空Phone中log"
    os.popen("adb logcat -c")
    #print"暂停2秒..."
    print("wait")
    time.sleep(2)
    os.popen(cmd)

    #print"手机截屏"
    os.popen("adb shell screencap -p /sdcard/monkey_run.png")

    #print"拷贝截屏图片至电脑"
    cmd1 = "adb pull /sdcard/monkey_run.png %s" % logdir
    os.popen(cmd1)
    oldname = logdir + "\\" + r"monkey_run.png"
    if os.path.exists(oldname):
        print("file is exist")
        newname = logdir + "\\" + now1 + r"monkey.png"
        os.rename(oldname, newname)
    else:
        print("file isn't exist")

    #print"使用Logcat导出日志"
    # logcatname = logdir + "\\" + now1 + r"logcat.log"
    cmd2 = "adb logcat -d >%s" % logcatname
    os.popen(cmd2)
    #print"导出traces文件"
    tracesname = logdir + "\\" + now1 + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)
######################
#获取error,
# logcatname,
# log_list:version,model,brand
######################
def geterror(log_list, logcatname, remote_path, now1):
    NullPointer = "java.lang.NullPointerException"
    NullPointer_count = 0
    IllegalState = "java.lang.IllegalStateException"
    IllegalState_count = 0
    IllegalArgument = "java.lang.IllegalArgumentException"
    IllegalArgument_count = 0
    ArrayIndexOutOfBounds = "java.lang.ArrayIndexOutOfBoundsException"
    ArrayIndexOutOfBounds_count = 0
    RuntimeException = "java.lang.RuntimeException"
    RuntimeException_count = 0
    SecurityException = "java.lang.SecurityException"
    SecurityException_count = 0
    f = open(logcatname, "r")
    lines = f.readlines()
    errfile = "%s\error.log" % remote_path
    if os.path.exists(errfile):
        os.remove(errfile)
    fr = open(errfile, "a")
    fr.write(log_list[0])
    fr.write("\n")
    fr.write(log_list[1])
    fr.write("\n")
    fr.write(log_list[2])
    fr.write("\n")
    fr.write(now1)
    fr.write("\n")
    count = 0
    for line in lines:
        if re.findall(NullPointer, line):
            NullPointer_count += 1
        if re.findall(IllegalState, line):
            IllegalState_count += 1
        if re.findall(IllegalArgument, line):
            IllegalArgument_count += 1
        if re.findall(ArrayIndexOutOfBounds, line):
            ArrayIndexOutOfBounds_count += 1
        if re.findall(RuntimeException, line):
            RuntimeException_count += 1
        if re.findall(SecurityException, line):
            SecurityException_count += 1

         # 这里的日志文件放到服务器去
        if re.findall(NullPointer, line) or re.findall(IllegalState, line) or re.findall(IllegalArgument, line) or \
                re.findall(ArrayIndexOutOfBounds, line) or re.findall(RuntimeException, line) or re.findall(SecurityException, line):
            a = lines.index(line)
            for var in range(a, a+22):
                # 这个22是表示从找到某个出错的信息开始，打印log22行，这个数据你可以根据自己的需要改。基本上22行能把所有的出错有关的log展现出来了。
                print(lines[var])
                fr.write(lines[var])
            fr.write("\n")
        f.close()
        fr.close()
     # #柱形
    list_arg = [[NullPointer_count, IllegalState_count, IllegalArgument_count, ArrayIndexOutOfBounds_count, RuntimeException_count, SecurityException_count],
                [NullPointer, IllegalState, IllegalArgument, ArrayIndexOutOfBounds, RuntimeException, SecurityException]]
    matplotlibBase.mat_bar(list_arg)
    return count
if __name__ == '__main__':
    ini_file = r"d:\monkey.ini"
    if os.path.isfile(ini_file):
        mc = monkeyConfig.baseReadnin(ini_file)
        os.system('adb shell cat /system/build.prop >'+mc.get_phone_msg_log()) #存放的手机信息
        ll_list = getPhoneMsg(mc.get_phone_msg_log())
        print(ll_list)
        start_monkey(mc.get_cmd(), mc.get_phone_msg_log(), mc.get_logdir(), mc.get_now(), mc.get_logcatname())
        time.sleep(110)
        geterror(ll_list, mc.get_logcatname(), mc.get_remote_path(), mc.now)
    else:
        print(u"配置文件不存在"+ini_file)

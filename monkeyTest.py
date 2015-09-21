__author__ = 'shikun'
import os
import time
import re


packageName = "com.XXXX.app"
logdir = r"d:\jenkins" #留作扩展集成到jenkins
remote_path = r"\\10.21.101.100\build\android" #服务器地址，可以让开发查看
os.system('adb shell cat /system/build.prop >D:\jenkins\phone.text') #存放的手机信息
f = r"D:\jenkins\phone.text" #存放的手机信息
now1 = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
#print"开始执行Monkey命令"
monkeylogname = logdir + "\\" + now1 + "monkey.log"
print(monkeylogname)
cmd = "adb shell monkey -p " + packageName + " -s 500 --ignore-timeouts --monitor-native-crashes -v -v 10000 >>%s" % monkeylogname
logcatname = logdir + "\\" + now1 + r"logcat.log"

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
def start_monkey(cmd):
    ll_list = getPhoneMsg(f)
    print(ll_list)
    os.remove(f)
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
    print("gai ming")
    oldname = logdir + "\\" + r"monkey_run.png"
    if os.path.exists(oldname):
        print("file is exist")
    else:
        print("file isn't exist")
    newname = logdir + "\\" + now1 + r"monkey.png"
    os.rename(oldname, newname)
    #print"使用Logcat导出日志"
    # logcatname = logdir + "\\" + now1 + r"logcat.log"
    cmd2 = "adb logcat -d >%s" % logcatname
    os.popen(cmd2)
    #print"导出traces文件"
    tracesname = logdir + "\\" + now1 + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)

    time.sleep(2)
    geterror(ll_list)

######################
#获取error,
# logcatname,
# log_list:version,model,brand
######################
def geterror(log_list):
    NullPointer = "java.lang.NullPointerException"
    IllegalState = "java.lang.IllegalStateException"
    IllegalArgument = "java.lang.IllegalArgumentException"
    ArrayIndexOutOfBounds = "java.lang.ArrayIndexOutOfBoundsException"
    RuntimeException = "java.lang.RuntimeException"
    SecurityException = "java.lang.SecurityException"
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
        if re.findall(NullPointer, line) or re.findall(IllegalState, line) or re.findall(IllegalArgument, line) or \
                re.findall(ArrayIndexOutOfBounds, line) or re.findall(RuntimeException, line) or re.findall(SecurityException, line):
                a = lines.index(line)
                count += 1
                for var in range(a, a+22):
                    # 这个22是表示从找到某个出错的信息开始，打印log22行，这个数据你可以根据自己的需要改。基本上22行能把所有的出错有关的log展现出来了。
                    print(lines[var])
                    fr.write(lines[var])
                fr.write("\n")
        f.close()
        fr.close()
    print(u"异常总数为：" + str(count))
    return count
if __name__ == '__main__':
    start_monkey(cmd)

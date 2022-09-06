import os
import smtplib
import sys
import time
from email.utils import formataddr
import socket

import pytest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf.GlobalConfig import GlobalConfig
from libs.Mq import MyMq

sys.path.append(GlobalConfig.ROOT_DIR)

mail_host = "smtp.exmail.qq.com"
mail_user = "qa@haochezhu.club"
mail_pass = "123"
# 收件人
mailto_list = ["123"]
report_file = f".{os.sep}report.html"
# 邮件内url
time_str = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]
link = f"http://{ip}:10086/gd_aep_html_{time_str}/index.html"


def write_html_head(report_html):
    """
    定义html文件的格式
    """
    report_html.write("<!DOCTYPE html>\n")
    report_html.write("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n")
    report_html.write("<style type=\"text/css\">\n")
    report_html.write("<!--\n")
    report_html.write("body{margin:0; font-family:Tahoma;Simsun;font-size:12px;}\n")
    report_html.write("table{border:1px #E1E1E1 solid;}\n")
    report_html.write("td{border:1px #E1E1E1 solid;}\n")
    report_html.write("p{font-size:14px;color:#F00}\n")
    report_html.write(".title {font-size: 14px; COLOR: #FFFFFF; font-family:times new roman;}\n")
    report_html.write(".desc {font-size: 14px; COLOR: #000000; font-family:times new roman;}\n")
    report_html.write("-->\n")
    report_html.write("</style>\n")
    report_html.write("<br>")


def write_html_link(report_html, link):
    """
    添加报告url
    """
    report_html.write(
        '<head><center><font face=\"Microsoft YaHei\" size=5 color=0xF0F0F>电商接口自动化报告详情: <a href="' + link + '">' +
        link + '</a></font></center></head>')
    report_html.write("<br>")
    report_html.write("</body>")
    report_html.write("</html>")


def write_html_total_table(report_html, case_info, project):
    rate = int(case_info["passed"]) / int(case_info["total"])
    report_html.write("<head><center><font face=\"Microsoft YaHei\" size=5 color=0xF0F0F>接口自动化结果汇总</font></center"
                      "></head>\n")
    report_html.write("<body><table cellpadding=\"0\" cellspacing=\"0\" align=\"center\"\n>")
    report_html.write("<tr bgcolor=#034579 align=center class=title><td width=\"160\">产品线</td><td width=\"170\">模块"
                      "</td><td width=\"110\">case验证总数</td><td width=\"110\">case验证成功数</td><td width=\"110\">case"
                      "验证失败数</td><td width=\"110\">case验证成功率</td><td width=\"110\">case运行时间(秒)</td></tr>\n")
    report_html.write(
        "<tr align=center bgcolor=#FFFFFF class=desc><td><B>" + project + "</B></td><td>" + "汇总" + "</td><td>" + str(
            case_info["total"]) + "</td><td>" + str(case_info["passed"]) + "</td><td style=\"color:red;\">" + str(
            case_info["failed"]) + "</td><td style=\"color:green;\"><B>" + str(
            "%.2f%%" % (rate * 100)) + "</B></td><td>" + str(case_info["time"]) + "</td></tr>\n")
    report_html.write("</table>\n")
    report_html.write("<br>")


def send_mail(to_list, sub, file_path):
    """
    发送邮件
    """
    with open(file_path, "r", encoding="utf-8") as f1:
        data = f1.read()
    msg = MIMEMultipart()
    text_msg = MIMEText(data, 'html', 'utf-8')
    msg.attach(text_msg)

    msg['Subject'] = sub
    msg['From'] = formataddr(("质量保证", mail_user))
    msg['To'] = ";".join(to_list)

    try:
        server = smtplib.SMTP_SSL(host=mail_host, port=465)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        raise e


if __name__ == '__main__':

    cmd_list = []
    # 0:文件本身 1:环境选择  2:-m参数  3:优先级参数  4:收件人
    count = len(sys.argv)
    if count > 1:
        env = sys.argv[1]
        if env not in GlobalConfig.ENV_LIST:
            print("执行环境选择错误!!!")
            exit()
        elif env != "default":
            GlobalConfig.MAIN_ENV = True
            GlobalConfig.ENV = env
        else:
            GlobalConfig.ENV = "uat"
        if count > 2 and sys.argv[2]:
            cmd_list.append("-m")
            cmd_list.append(sys.argv[2])
        if count > 3 and sys.argv[3]:
            cmd_list.append("--allure-severities")
            cmd_list.append(sys.argv[3])
        if count > 4 and sys.argv[4]:
            mailto_list += sys.argv[4].split(",")
    os.system("rm -rf report/*")
    pytest.main(cmd_list)
    time.sleep(1)
    os.system(f"allure generate report/ -o /auto_test/report/gd_aep_html_{time_str} --clean")
    report_html = open(report_file, "w", encoding="utf-8")
    write_html_head(report_html)
    write_html_total_table(report_html, GlobalConfig.RESULT_DICT, "电商")
    write_html_link(report_html, link)
    report_html.close()
    send_mail(mailto_list, "电商接口自动化", report_file)
    # 手动释放mq
    MyMq().__del__()
    sys.exit(0)



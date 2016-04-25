# coding:utf-8
from django.shortcuts import render, HttpResponse
from web_chat import  models
import json
import Queue
import time
from django.contrib.auth.decorators import login_required
# Create your views here.
GLOBAL_GROUP_MQ = {

}
GLOBAL_USER_MQ = {

}


@login_required()
def chatroom(request):

    return render(request, 'web_chats/web_chat.html')


@login_required()
def contacts(request):
    contact_dic = {
        # 'contact_list' : [],
        # 'group_list' : []
    }
    # 将数据库读取到的联系人和群组信息添加到字典中
    cont = request.user.userprofile.qq_friends.select_related().values('id', 'name')
    contact_dic['contact_list'] = list(cont)
    groups = request.user.userprofile.qqgroups_set.select_related().values('id', 'name', 'max_menbers_nums')
    contact_dic['group_list'] = list(groups)

    return HttpResponse(json.dumps(contact_dic))


@login_required()
def new_msg(request):

    if request.method == "POST":

        data = json.loads(request.POST.get('data'))
        send_to = data['to']
        msg_from = data['from']
        w = time.localtime()
        n_time = time.strftime('%Y-%m-%d %H:%M:%S', w)
        data['time'] = n_time
        contact_type = data['contact_type']
        if contact_type == 'group_contact':
            group_obj = models.QQGroups.objects.get(id=send_to)
            for member in group_obj.members.select_related():
                if str(member.id) not in GLOBAL_GROUP_MQ:
                    GLOBAL_GROUP_MQ[str(member.id)] = Queue.Queue()
                if str(member.id) != msg_from:
                    GLOBAL_GROUP_MQ[str(member.id)].put(data)
        else:
            if send_to not in GLOBAL_USER_MQ:
                GLOBAL_USER_MQ[send_to] = Queue.Queue()
            GLOBAL_USER_MQ[send_to].put(data)

        # q_size = GLOBAL_USER_MQ[send_to].qsize()
        return HttpResponse("No qszie")
    else:
        print "request.GET----->", request.GET.get('contact_type')
        user_id = str(request.user.userprofile.id)
        msg_list = []
        print GLOBAL_USER_MQ
        if user_id in GLOBAL_USER_MQ:     # 如果用户在消息字典里
            print "hhe"
            msg_nums = GLOBAL_USER_MQ[user_id].qsize()   # msg nums
            if msg_nums == 0:
                try:
                    print "\033[41;1m No new msg \033[0m"
                    msg_list.append(GLOBAL_USER_MQ[user_id].get(timeout=60))  # 向信息列表中添加数据，超时为15秒
                except Exception as e:
                    print "error:",e
                    print "\033[41;1m Time out or new msg... \033[0m"
            for i in range(msg_nums):      # 循环消息字典中的数据，并添加到消息列表中
                msg_list.append(GLOBAL_USER_MQ[user_id].get())
        else:
            GLOBAL_USER_MQ[user_id] = Queue.Queue()
        return HttpResponse(json.dumps(msg_list))
        return HttpResponse('OOOK')



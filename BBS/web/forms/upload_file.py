# coding:utf-8

import os


def handle_upload_file(request, f):

    file_name = f.name    # 文件名
    img_upload_path = "static/imgs"    # 图片上传的路径
    user_path = "%s/%s" % (img_upload_path, request.user.userprofile.id)  # 每个用户上传的路径

    if not os.path.exists(user_path):  # 判断是否有此目录，没有则创建
        os.mkdir(user_path)
    with open("%s/%s" % (user_path, file_name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return "/static/imgs/%s/%s" % (request.user.userprofile.id, file_name)

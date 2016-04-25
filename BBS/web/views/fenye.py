# coding:utf-8


class Pager(object):
    def __init__(self, current_page):
        self.current_page = int(current_page)

    @property
    def start(self):
        return (self.current_page-1)*10

    @property
    def end(self):
        return self.current_page*10

    def page_str(self, all_item, base_url):

        # 获得所有页面的整数

        all_page, div = divmod(all_item, 10)
        print "--------all page", all_page,div
        if div > 0:
            all_page += 1
        print "all page dvi count---------->", all_page

        # 定义一个列表 用来保存拼接的分页A标签
        pager_list = []
        start = self.current_page - 5     # 使当前页一直处于分页的中间位置
        end = self.current_page + 6

        # 当总页数小于11
        if all_page <= 11:    # 开始为1  结束为总页数
            start = 1
            end = all_page
            print "all page dvi count----end------>", all_page, end
        # 当总页数大于11
        else:
            if self.current_page <= 6:  # 当前页小于等于6
                start = 1               # 规定开始为1 避免出现0 或者负值
                end = 12
            else:                       # 当前页大于6时
                start = self.current_page - 5     # 为了使当前页保持在中间位置 -5
                end = self.current_page + 6       # 同理为了使当前页保持在中间位置 +5
                if self.current_page + 6 > all_page:   # 如果当前页+6大于了总页数
                    start = all_page - 11               # 为使当前页在中间 开始应总页数-11
                    end = all_page + 1                  # 结束总页数+1 大一个才会取到最后一个值
                    print "all page dvi count---------->", all_page
        # 根据开始 结尾来拼接A标签
        for i in range(start, end+1):
            print "This is i---------------->", i
            print "---------start and end", start, end
            if i == self.current_page:   # 使当前页添加格外样式
                temp = '<a class="fenpage-middle" href="%s%d">%d</a>' % (base_url, i, i,)
            else:
                temp = '<a  href="%s%d">%d</a>' % (base_url, i, i,)
            pager_list.append(temp)   # 追加到列表中

        # 只有当前页大于1时才会使上一页点击有效
        if self.current_page > 1:
            pre_page = '<a href="%s%d">上一页</a>' % (base_url, self.current_page-1)
        else:
            pre_page = '<a href="javascript:void(0);">上一页</a>'

        # 当前页大于或等于总页数 下一页的标签就会失效
        if self.current_page >= all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href="%s%d">下一页</a>' % (base_url, self.current_page+1)

        pager_list.insert(0, pre_page)  # 将上一页插入到列表的最开始
        pager_list.append(next_page)    # 下一页追加到最后
        return "".join(pager_list)      # 将列表中的所有A标签字符串拼接成一个大的字符串


# def userlist(request):
#
#     current_page = request.GET.get('page', 1)    # 获取前端页面点击的当前页
#     page_obj = Pager(current_page)             # 创建分页对象
#     data_obj = models.FenPata.objects.all()[page_obj.start: page_obj.end]   # 从数据库中获取设计的每页显示数据的条数
#
#     all_item = models.FenPata.objects.all().count()    # 获取数据库中所有数据的总条数
#     pager_str = page_obj.page_str(all_item, "/user_list/?page=")     # 根据总的条数来拼接前端需要的标签字符串
#
#     return render(request, 'user_list.html', {'result': data_obj, 'page_str': pager_str})

class memdata:
    def __init__(self,path):
        self.file_addrs=self._get_file_addrs(path)
        news_ids = []
        for id in self.file_addrs:
            if id not in news_ids:
                news_ids.append(id)
        self.file_addrs=news_ids
        self.handled_info=self._handle()

    def _get_file_addrs(self,path):
        result=list()
        for i in open(path, "r").readlines():
            i=i.split()[1].replace("\n","")
            int_i=int(i,16)
            result.append((i,int_i))
        return result

    def _handle(self):
        result=list()
        i = 0
        while i<len(self.file_addrs):
            x_start=self.file_addrs[i]
            x_pre=x_start
            j=1
            for xx in self.file_addrs[i+1:]:
                if xx[1]-x_pre[1]!=0 and xx[1]-x_pre[1]!=1:
                    if x_pre[1]-x_start[1]+1!=1:
                        result.append((x_start[0],x_pre[1]-x_start[1]+1))
                        # print((x_start[0],x_pre[1]-x_start[1]+1))
                    break
                else:
                    j+=1
                x_pre=xx
            i+=j
        return result





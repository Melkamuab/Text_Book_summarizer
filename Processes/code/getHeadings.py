from django.contrib import messages
"""
USE:
headings=Headings(request, extract.doc_text, extract.working_toc, extract.page_diff, extract.font_styles)
error, heading_para=headings.main()
"""

class Headings:
    def __init__(self, request, doc_text, working_toc, page_diff, font_styles):
        self.request=request
        self.doc_text   =doc_text
        self.working_toc= working_toc
        self.page_diff  =page_diff
        self.font_styles=font_styles

    def similar(self, title, t1):
        t1=t1.strip()
        titles = title.split(' ')
        texts  = t1.split(' ')
        count=0
        for text in texts.copy():
            if(text in titles):
                titles.remove(text)
                texts.remove(text)
                count+=1
            else:
                count-=1
                texts.remove(text)
        return count

    def getToC(self, index):
        text = self.toc[index]
        return text

    def locate_heading(self, transit, lvl=-1):
        transit.sort(key=self.similarity_sort, reverse=True)
        block_index = transit[0][1]
        return block_index

    def change_style(self):
        index=0
        for page_index,page_text in enumerate(self.doc_text):
            head_para=[]
            block_index = 0
            while block_index < len(page_text):
                block_text = page_text[block_index]
                if(index<len(self.heading_identified)):
                    if(self.heading_identified [index][2]==page_index):
                        b_indexes = self.heading_identified[index][-1]
                        if(len(b_indexes) == 1):
                            if(self.heading_identified[index][-1][0]==block_index):
                                value=(block_text[0],'heading_'+str(self.heading_identified[index][0]))
                                head_para.append(value)
                                index+=1
                        else:
                            if(self.heading_identified[index][-1][0]==block_index):
                                text = self.heading_identified[index][1]
                                for b_index in b_indexes:
                                    if b_index < len(block_text):
                                        text += str(block_text[b_index])
                                        value=(text,'heading_'+str(self.heading_identified[index][0]))
                                        head_para.append(value)
                                        index+=1
                                        block_index += len(b_indexes)
                                        continue
                    else:
                        head_para.append((block_text[0],'para'))
                else:
                    head_para.append((block_text[0],'para'))
                block_index += 1
            self.heading_para.append(head_para)

    def similarity_sort(self,value):
        return value[0]

    def heading_text(self):
        precise_heading = []
        for headings in self.heading_identified:
            heading_text = headings[1]
            pno = headings[2]
            b_index = headings[3]
            compare = []
            block_no = len(self.doc_text[pno])
            for i in (-1,0,1):
                compare.extend(self.heading_compare(headings, i))


            precise_heading.append(compare)

        for i,heading in enumerate(precise_heading):
            heading.sort(key=lambda a:a[0] ,reverse=True)
            _, b_indexes, heading_text = heading[1]
            self.heading_identified[i][3] = b_indexes
            self.heading_identified[i][1]= heading_text

    def heading_compare(self, heading_toc, step, block_index, page):
        heading_text = heading_toc[1]
        pno = heading_toc[2]
        b_index = block_index
        compare = []
        block_size = len(page)
        if(b_index + step< block_size and b_index+step>=0):
            b_indexes = [b_index]
            doc_text = page[b_index]
            text = doc_text[0]
            if step>0:
                b_indexes.append(b_index + step)
                doc_text = page[b_index+step]
                text += doc_text[0]
            similarity = self.similar(heading_text, text)
            compare.append((similarity, b_indexes, text))
        return compare

    def fix_headings(self):
        working_toc = self.working_toc.copy()
        self.working_toc.append("the end")
        length=len(self.working_toc)-1
        self.heading_identified=working_toc[0:length-1].copy()
        for i,heading in enumerate(self.heading_identified.copy()):
            title=heading[1]
            if(i==length-1):
                break
            pno=heading[3]['page']-self.page_diff
            page=self.doc_text[pno]
            compare=[]
            for j,block in enumerate(page):
                text=block[0]
                size=block[1]
                block_indexes = [j]
                compare_multi=[]
                for step in (0,1):
                    compare_multi.extend(self.heading_compare(heading, step, j, page))
                compare_multi.sort(key = lambda a:a[0], reverse= True)
                value = compare_multi[0]
                value = list(value)
                value.append(title)
                compare.append(value)
            compare.sort(key = lambda a:int(a[0]), reverse= True)
            block_indexes = compare[0][1]
            text = compare[0][3]
            similarity = compare[0][0]
            self.heading_identified[i].append(block_indexes)
            self.heading_identified[i][2]=self.heading_identified[i][3]['page']-self.page_diff
            self.heading_identified[i][1]=text

    def main(self):
        self.heading_para= []
        self.font_styles= list(self.font_styles)
        self.font_styles.sort(reverse=True)
        self.fix_headings()
        #self.heading_text()
        self.change_style()
        try:
            self.error=False
        except Exception:
            messages.warning(self.request,"Your PDF doesnot have valid table of content")
            self.error=True
        return self.error,self.heading_para


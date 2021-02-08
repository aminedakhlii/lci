from docx import Document

class Doc():

    def __init__(self, document):
        self.document = Document(document)


    def replace(self, old , new):
        for p in self.document.paragraphs:
            if old in p.text:
                inline = p.runs
                for i in range(len(inline)):
                        if old in inline[i].text:
                            text = inline[i].text.replace(old , new)
                            inline[i].text = text
            print(p.text)
    def saveDoc(self, path):
        self.document.save(path)

if __name__=='__main__':
    document = Doc('certifs.docx')
    document.replace('22.10.2018' , 'hi')
    document.replace('Business 1' , '')

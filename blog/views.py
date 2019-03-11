from django.shortcuts import render
from django.http import HttpResponse, Http404
import os, re
from lxml import html, etree
#import cgi, html
import time
from django.templatetags.static import static

# Create your views here.

#notebook scripts (load remote or local)
LOCAL_NOTEBOOK = False
scripts = [
    '/static/blog/js/nb/require.min.js',
    '/static/blog/js/nb/jquery.min.js',
    '/static/blog/js/MathJax/MathJax.js?config=TeX-AMS_HTML',
]

PWD = os.getcwd()

def readFile(path):
    f = open(path, "r")
    string = f.read();
    f.close()
    return string

class fileObj:
    def __init__(self,fileName):
        try:
            self.fileName = fileName
            self.data = readFile(fileName)
        except:
            raise Http404("File does not exist")

    def replace(self,scripts):
        #r = re.findall('<script src="(.*?)"></script>',self.data,re.DOTALL)
        #r = re.sub('<script src="(.*?)"></script>',self.data,re.DOTALL)
        #for i in r:
        #    print(i)
        #print(r)
        intervals = [[0,0]]
        for match in re.finditer('<script src="(.*?)"></script>',self.data,re.DOTALL):
            #print(match.group())
            start=match.start() 
            end=match.end()    
            intervals.append([start,end]) 
        intervals.append([len(self.data),len(self.data)])

        new_string = ""
        last = []
        i = 0
        for interval in intervals:
            #print(interval)
            if (interval != [0,0]):
                print(i)
                text = self.data[last[1]:interval[0]]
                #src = self.data[interval[0]:interval[1]]i

                new_string += text

                if(i <= 2):
                    src = scripts[i]
                    new_string += '<script src="'+src+'"></script>'

                i += 1

            last = interval

        self.data = new_string


   

TOPICS = ""

#generate topics menu from index.html
def topics(data):
    global TOPICS
    topics = ""

    #create root HtmlElement instance
    doc = html.fromstring(data)

    links = doc.xpath('//a[@name]')
    for link in links:
        name = link.get('name')
        a = '<a class="dropdown-item" href="/#'+ name + '">' + name + '</a>\n'
        topics += a 

    TOPICS = topics        

#init topics
index = PWD + '/blog/templates/blog/data/index.html' 
myfile = fileObj(index)
file_str = myfile.data
topics(file_str)

def index(request):
    global TOPICS

    return render(request, 'blog/data/index.html', {'topics':TOPICS})


def detail(request):
    '''
    file.htm         => template with iframe + file.html (notebook.html)
    /nb/...file.html => notebook.html (remove starting mark '/nb/')
    file.html        => syntax color (google prettify)
    '''
    global TOPICS

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    #remove final '/'
    #print("request.path",request.path)
    lastChar = request.path[ len(request.path)-1] 
    if lastChar == '/':
        path = request.path[:len(request.path)-1]
    else:
        path = request.path

    dirs = path.split("/")
    name = (dirs[len(dirs)-1])

    #Example:
    #/nb/1/test_latex.html
    #['', 'nb', '1', 'test_latex.html']

    #starting 'nb' is just a mark for notebook: render straight notebook html file for iframe
    if(dirs[1] == 'nb'):
        #erasing starting "nb" from path
        realPath = '/'.join(dirs[2:]) 
        fileName = PWD + '/blog/templates/blog/data/' + realPath
        #print(">>>",fileName)
        myfile = fileObj(fileName)
        if LOCAL_NOTEBOOK:
            myfile.replace(scripts)
        notebookStr = myfile.data
        return HttpResponse(notebookStr)
    
    #file.htm : 
    if re.findall("(.*).htm$",name):
        notebookFile = "/nb"+request.path+"l"
        #return HttpResponse(notebookFile)
        return render(request, 'blog/data'+request.path, {'src':notebookFile,'color':'False','topics':TOPICS})
    
    #file.html 
    if re.findall("(.*).html$",name):
        return render(request, 'blog/data'+request.path, {'color':'True','topics':TOPICS})

    return HttpResponse("not found")
    #raise Http404("not found")

#remove raw "notebooks" from site map
#when list include file.htm and file.html, keep only file.htm
#remove css, txt
def filterList(listOfDirs):
    #print(listOfDirs)

    for item1 in listOfDirs:
        for item2 in listOfDirs:
            if(item1 == item2+"l"):
                #print(item2)
                listOfDirs.remove(item1)

    #for item in listOfDirs:
    #    if (re.findall(".*.html?",item) == []):
    #        print(item)
    #        #listOfDirs.remove(item)

    for item in listOfDirs:
        if (re.findall(".*.css",item) != []):
            listOfDirs.remove(item)

    for item in listOfDirs:
        if (re.findall(".*.txt",item) != []):
            listOfDirs.remove(item)


    return listOfDirs

string = ""

def traverse_dir(dir):

    global string
    string += '<ul>\n'

    #for item in os.listdir(dir):
    for item in filterList(os.listdir(dir)):

        #exclude debug folder
        if(item != "debug"):

            fullpath = os.path.join(dir, item)

            if os.path.isdir(fullpath):
                string += ('<li>%s</li>\n' % item)
            else:
                startStr = PWD + "/blog/templates/blog/data"
                #remove startStr
                relativePath = fullpath[len(startStr):] 
                string += ('<li><a href="%s">%s</a></li>\n' % (relativePath,item))

            if os.path.isdir(fullpath):
                if os.listdir(fullpath) != []:
                    traverse_dir(fullpath)

    string += '</ul>\n'

def site_map(request):
    traverse_dir(PWD + "/blog/templates/blog/data")
    return render(request, 'blog/site_map.html', {'fileList':string,'topics':TOPICS})

import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

an1={}
an2={}
an3={}
sl1=''
sl2=''
sl3=''
slovo=''
count=0


@app.route('/')
def form():
    f=open('C:\\Users\\1\\Desktop\\data.txt', 'a', encoding="UTF-8")
    stats = url_for('stats')
    jsones = url_for('jsones')
    search = url_for('search')
    
    global an1, an2, an3
    
    if request.args:
        name=request.args['name']
        age=request.args['age']
        town=request.args['town']
        answ1 = request.args['answ1']
        answ2 = request.args['answ2']
        answ3 = request.args['answ3']
        if answ1!='':
            an1['договор']=answ1
        if answ2!='':
            an2['апостроф']=answ2
        if answ3!='':
            an3['баловать']=answ3

        global sl1, sl2, sl3
        sl1=answ1
        sl2=answ2
        sl3=answ3
        
        f.write(name+'\t'+age+'\t'+town+'\t'+answ1+'\t'+answ2+'\t'+answ3+'\n')
            
        return render_template('question.html', answ1=answ1, answ2=answ2, answ3=answ3, stats=stats, jsones=jsones, search=search)           
    return render_template('question.html', jsones=jsones, stats=stats, search=search)

@app.route('/stats')
def stats():
    anketa = url_for('form')
    jsones = url_for('jsones')
    search = url_for('search')
    global sl1, sl2, sl3, count
    f=open('C:\\Users\\1\\Desktop\\data.txt', 'r', encoding="UTF-8")
    for line in f:
        count+=1
    
    i=0
    if sl1!='договОр':
        i+=1
    if sl2!='апострОф':
        i+=1
    if sl3!='бАловать':
        i+=1

    return render_template('stats.html', i=i, count=count, anketa=anketa, jsones=jsones, search=search)

@app.route('/json')
def jsones():
    stats = url_for('stats')
    anketa = url_for('form')
    search = url_for('search')
    
    d=dict(name=[], age=[], town=[], answ1=[], answ2=[], answ3=[])
    f=open('C:\\Users\\1\\Desktop\\data.txt', 'r', encoding="UTF-8")

    for line in f:
        arr=line.split('\t')
        d['name'].append(arr[0])
        d['age'].append(arr[1])
        d['town'].append(arr[2])
        d['answ1'].append(arr[3])
        d['answ2'].append(arr[4])
        d['answ3'].append(arr[5])
    f.close()
    result=json.dumps(d, sort_keys = True, indent = 4, ensure_ascii = False)
    
    return render_template('jsones.html', result=result, anketa=anketa, stats=stats, search=search)

@app.route('/search')
def search():
    anketa = url_for('form')
    stats = url_for('stats')
    jsones = url_for('jsones')
    if request.args:
        global slovo
        slovo=request.args['slovo']
        return redirect('results')
    return render_template('search.html', anketa=anketa, stats=stats, jsones=jsones, slovo=slovo)

@app.route('/results')
def results():
    anketa = url_for('form')
    stats = url_for('stats')
    jsones = url_for('jsones')
    search = url_for('search')
    global slovo
    mis1=0
    mis2=0
    mis3=0
    f=open('C:\\Users\\1\\Desktop\\data.txt', 'r', encoding="UTF-8")
    for line in f:
        for word in line:
            if 'дОговoр' in line:
                mis1 += 1
            if 'апОстроф' in line:
                mis2 += 1
            if 'баловАть' in line:
                mis3 += 1
    if slovo=='договор':
        n=mis1
    elif slovo=='апостроф':
        n=mis2
    elif slovo=='баловать':
        n=mis3

    return render_template('results.html', anketa=anketa, stats=stats, jsones=jsones, search=search, slovo=slovo, n=n)
        
        
if __name__ == '__main__':
    app.run(debug=True)

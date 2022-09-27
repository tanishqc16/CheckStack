from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np

df = pickle.load(open('df.pkl','rb'))
game = pickle.load(open('game.pkl','rb'))
webp = pickle.load(open('webp.pkl','rb'))
appp = pickle.load(open('app.pkl','rb'))
block = pickle.load(open('block.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ml')
def ml():
    return render_template('ml.html')

@app.route('/suggest_ml',methods=['post'])
def suggest_ml():
    py = int(request.form.get('py'))
    r = int(request.form.get('r'))
    lib = int(request.form.get('lib'))
    math = int(request.form.get('math'))

    tempdf = df[(df.pyskill <= py) | (df.rustskill <= r)]

    if (lib == 0 & math < 5):
        tempdf = tempdf[(df.avg < 7)]
    elif (lib == 1 & math < 5):
        tempdf = tempdf[(df.avg >= 7) & (df.avg <= 8)]
    elif (lib == 0 & math >= 5):
        tempdf = tempdf[(df.avg >= 8) & (df.avg <= 9)]
    else:
        tempdf = tempdf[(df.avg >= 9) & (df.avg <= 10)]

    if tempdf.empty:
        tempdf = df[(df.avg < 7)]

    tempdf.sort_values(by=['popularity'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)
    arr = tempdf.to_numpy()

    return render_template('ml.html',data=arr)


@app.route('/blockchain')
def blockchain():
    return render_template('blockchain.html')\

@app.route('/suggest_blockchain',methods=['post'])
def suggest_blockchain():
    spec = int(request.form.get('spec'))
    js = int(request.form.get('js'))
    py = int(request.form.get('py'))
    go = int(request.form.get('go'))
    cpp = int(request.form.get('cpp'))
    rust = int(request.form.get('rust'))
    hcs = int(request.form.get('hcs'))
    time = int(request.form.get('time'))
    scale = int(request.form.get('scale'))

    js = js + 2
    py = py + 2
    rust = rust + 2
    hcs = hcs + 2
    cpp = cpp + 2
    go = go + 2

    resultArr=[]

    if (spec == 0):
        # maxSkill = max(js, py, rust)
        tempdf = block.query('Specification=="SmartContracts"')

        tempdf = tempdf[(tempdf.Time2Learn <= time)
                        & (tempdf.SkillLvlJS <= js)
                        & (tempdf.SkillLvlPy <= py)
                        & (tempdf.SkillLvlRust <= rust)
                        & (tempdf.SkillLvlHCss <= hcs)
                        & (tempdf.Scalability >= scale)]

        tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
        tempdf.reset_index(inplace=True, drop=True)
        # rec1 = tempdf.loc[0,:]

        if (tempdf.empty):
            rec1 = block[(block.Name == "Atra") & (block.Specification == "SmartContracts")]
        else:
            rec1 = tempdf.head(1)

        rec1.reset_index(inplace=True, drop=True)
        comp1 = rec1.loc[0, "Compatibility1"]
        comp2 = rec1.loc[0, "Compatibility2"]

        # second rec
        tempdf = block.query('Specification=="Frontend"')
        tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]

        tempdf = tempdf[(tempdf.Time2Learn <= time)
                        & (tempdf.SkillLvlJS <= js)
                        & (tempdf.SkillLvlPy <= py)
                        & (tempdf.SkillLvlRust <= rust)
                        & (tempdf.SkillLvlHCss <= hcs)
                        & (tempdf.Scalability >= scale)]

        tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
        tempdf.reset_index(inplace=True, drop=True)
        # rec2 = tempdf.loc[0,:]

        if (tempdf.empty):
            rec2 = block[(block.Name == "WordPressFront") & (block.Specification == "Frontend")]
        else:
            rec2 = tempdf.head(1)

        rec2.reset_index(inplace=True, drop=True)
        comp1 = rec2.loc[0, "Compatibility1"]
        comp2 = rec2.loc[0, "Compatibility2"]

        # Third rec
        tempdf = block.query('Specification=="Backend"')

        tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]

        tempdf = tempdf[(tempdf.Time2Learn <= time)
                        & (tempdf.SkillLvlJS <= js)
                        & (tempdf.SkillLvlPy <= py)
                        & (tempdf.SkillLvlRust <= rust)
                        & (tempdf.SkillLvlHCss <= hcs)
                        & (tempdf.Scalability >= scale)]

        tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
        tempdf.reset_index(inplace=True, drop=True)
        # rec3 = tempdf.loc[0,:]
        rec3 = tempdf.head(1)

        # print("Recommendations are:")
        # print(rec1)
        # print(rec2)
        # print(rec3)

        array = [rec1, rec2, rec3]
        result = pd.concat(array)
        resultArr = result.to_numpy()

    elif (spec == 1):
        tempdf = block.query('Specification=="Core"')
        tempdf = tempdf[(tempdf.Time2Learn <= time)
                        & (tempdf.SkillLvlCpp <= cpp)
                        & (tempdf.SkillLvlGo <= go)
                        & (tempdf.SkillLvlRust <= rust)
                        & (tempdf.Scalability >= scale)]
        tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
        tempdf.reset_index(inplace=True, drop=True)
        # rec = tempdf.loc[0,"Name"]
        rec1 = tempdf.head(1)
        array = [rec1]
        result = pd.concat(array)
        resultArr = result.to_numpy()

    print(resultArr)
    return render_template('blockchain.html', data=resultArr)

@app.route('/gamedev')
def gamedev():
    return render_template('gamedev.html')

@app.route('/suggest_gamedev',methods=['post'])
def suggest_gamedev():
    eng = int(request.form.get('eng'))
    code = int(request.form.get('code'))
    js = int(request.form.get('js'))
    cpp = int(request.form.get('cpp'))
    py = int(request.form.get('py'))
    cs = int(request.form.get('cs'))
    time = int(request.form.get('time'))
    scale = int(request.form.get('scale'))


    resultArr=[]



    if (code == 1):
        tempdf = game.query('Code==1')
        if (eng == 1):
            tempdf = tempdf.query('Specification=="Engine"')
            tempdf = tempdf[(tempdf.Time2Learn <= time)
                            & (tempdf.SkillLvlJS <= js + 2)
                            & (tempdf.SkillLvlPy <= py + 2)
                            & (tempdf.SkillLvlCpp <= cpp + 2)
                            & (tempdf.SkillLvlCs <= cs + 2)
                            & (tempdf.Scalability >= scale - 2)]

            tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
            tempdf.reset_index(inplace=True, drop=True)
            # rec = tempdf.loc[0,"Name"]
            rec = tempdf.head(1)
            array = [rec]
            result = pd.concat(array)
            resultArr = result.to_numpy()


        elif (eng == 0):
            tempdf = tempdf.query('Specification=="Library"')
            tempdf = tempdf[(tempdf.Time2Learn <= time)
                            & (tempdf.SkillLvlJS <= js + 2)
                            & (tempdf.SkillLvlPy <= py + 2)
                            & (tempdf.SkillLvlCpp <= cpp + 2)
                            & (tempdf.SkillLvlCs <= cs + 2)
                            & (tempdf.Scalability >= scale - 2)]
            tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
            tempdf.reset_index(inplace=True, drop=True)
            # rec = tempdf.loc[0,"Name"]
            rec = tempdf.head(1)
            array = [rec]
            result = pd.concat(array)
            resultArr = result.to_numpy()


    elif (code == 0):
        tempdf = game.query('Code==0')

        tempdf = tempdf[(tempdf.Time2Learn <= time) & (tempdf.Scalability >= scale)]
        tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
        tempdf.reset_index(inplace=True, drop=True)
        # rec = tempdf.loc[0,"Name"]
        rec = tempdf.head(1)
        array = [rec]
        result = pd.concat(array)
        resultArr = result.to_numpy()

    print(resultArr)
    return render_template('gamedev.html', data=resultArr)

@app.route('/web')
def web():
    return render_template('web.html')

@app.route('/suggest_web',methods=['post'])
def suggest_web():
    js = int(request.form.get('js'))
    py = int(request.form.get('py'))
    hcs = int(request.form.get('hcs'))
    time = int(request.form.get('time'))
    scale = int(request.form.get('scale'))

    js = js + 2
    py = py + 2
    hcs = hcs + 2

    resultArr=[]

    tempdf = webp.query('Specification=="Frontend"')

    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js))
                    & (tempdf.SkillLvlPy <= (py))
                    & (tempdf.SkillLvlHCss <= (hcs))
                    & (tempdf.Scalability >= (scale))]

    tempdf.sort_values(by=['Scalability'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)
    rec1 = tempdf

    if (rec1.empty):
        rec1 = webp[(webp.Name == "Wordpress") & (webp.Specification == "Frontend")]

    # rec1=tempdf.loc[0,"Name"]
    else:
        rec1 = tempdf.head(1)

    print(rec1)

    comp1 = tempdf.loc[0, "Compatibility1"]
    comp2 = tempdf.loc[0, "Compatibility2"]

    # second rec
    tempdf = webp.query('Specification=="Backend"')
    tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]

    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js))
                    & (tempdf.SkillLvlPy <= (py))
                    & (tempdf.SkillLvlHCss <= (hcs))
                    & (tempdf.Scalability >= (scale))]

    tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)

    # if (tempdf.isnull):
    #   rec2 = tempdf.loc[0,"Name"]

    # rec2 = tempdf.loc[0,"Name"]
    rec2 = tempdf
    if (rec2.empty):
        rec2 = webp[(webp.Name == "Wordpress") & (webp.Specification == "Backend")]
    else:
        rec2 = tempdf.head(1)

    # if tempdf is empty then run the following 2 statements
    comp1 = tempdf.loc[0, "Compatibility1"]
    comp2 = tempdf.loc[0, "Compatibility2"]

    # Third rec
    tempdf = webp.query('Specification=="Database"')

    tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]

    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js))
                    & (tempdf.SkillLvlPy <= (py))
                    & (tempdf.SkillLvlHCss <= (hcs))
                    & (tempdf.Scalability >= (scale))]

    tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)
    rec = tempdf
    # rec3 = tempdf.loc[0,"Name"]
    rec3 = tempdf.head(1)

    # print("Recommendations are:")
    # print(rec1)
    # print(rec2)
    # print(rec3)

    if (rec1.empty and rec2.empty and rec3.empty):
        rec1 = webp.query('Name=="WordPress"')
        array = [rec1]
        result = pd.concat(array)
        resultArr = result.to_numpy()
    else:
        array = [rec1, rec2, rec3]
        result = pd.concat(array)
        resultArr = result.to_numpy()

    print(resultArr)

    return render_template('web.html', data=resultArr)

@app.route('/appdev')
def appdev():
    return render_template('appdev.html')

@app.route('/suggest_appdev',methods=['post'])
def suggest_appdev():
    java = int(request.form.get('java'))
    js = int(request.form.get('js'))
    cpp = int(request.form.get('cpp'))
    dart = int(request.form.get('dart'))
    sql = int(request.form.get('sql'))
    time = int(request.form.get('time'))
    scale = int(request.form.get('scale'))

    tempdf = appp.query('Specification=="Frontend"')

    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js + 1))
                    & (tempdf.SkillLvlJava <= (java + 1))
                    & (tempdf.SkillLvlCpp <= (cpp + 1))
                    & (tempdf.SkillLvlSql <= (sql + 1))
                    & (tempdf.SkillLvlDart <= (dart + 1))
                    & (tempdf.Scalability >= (scale + 1))]

    tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)

    tempdf.reset_index(inplace=True, drop=True)
    rec1 = tempdf
    if (rec1.empty):
        rec1 = appp[(appp.Name == "Wordpress") & (appp.Specification == "Frontend")]
    else:
        rec1 = tempdf.head(1)
    # print(tempdf)
    comp1 = tempdf.loc[0, "Compatibility1"]
    comp2 = tempdf.loc[0, "Compatibility2"]

    # second rec
    tempdf = appp.query('Specification=="Backend"')
    tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]
    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js + 1))
                    & (tempdf.SkillLvlJava <= (java + 1))
                    & (tempdf.SkillLvlCpp <= (cpp + 1))
                    & (tempdf.SkillLvlSql <= (sql + 1))
                    & (tempdf.SkillLvlDart <= (dart + 1))
                    & (tempdf.Scalability >= (scale + 1))]

    tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)

    rec2 = tempdf
    if (tempdf.empty):
        rec2 = appp[(appp.Name == "GoodBarber") & (appp.Specification == "Frontend")]
    else:
        rec2 = tempdf.head(1)

    comp1 = tempdf.loc[0, "Compatibility1"]
    comp2 = tempdf.loc[0, "Compatibility2"]

    # Third rec
    tempdf = appp.query('Specification=="Database"')

    tempdf = tempdf[(tempdf.Name == comp1) | (tempdf.Name == comp2)]

    tempdf = tempdf[(tempdf.Time2Learn <= time)
                    & (tempdf.SkillLvlJS <= (js + 1))
                    & (tempdf.SkillLvlJava <= (java + 1))
                    & (tempdf.SkillLvlCpp <= (cpp + 1))
                    & (tempdf.SkillLvlSql <= (sql + 1))
                    & (tempdf.SkillLvlDart <= (dart + 1))
                    & (tempdf.Scalability >= (scale + 1))]

    tempdf.sort_values(by=['Popularity'], axis=0, ascending=False, inplace=True)
    tempdf.reset_index(inplace=True, drop=True)
    rec3 = tempdf.head(1)
    if (rec1.empty and rec2.empty and rec3.empty):
        rec1 = appp.query('Name=="GoodBarber"')
        array = [rec1]
        result = pd.concat(array)
        resultArr = result.to_numpy()
        print(result)
    else:
        array = [rec1, rec2, rec3]
        result = pd.concat(array)
        resultArr = result.to_numpy()
        print(result)

    return render_template('appdev.html', data=resultArr)

if __name__ == '__main__':
    app.run(debug=True)
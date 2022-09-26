from flask import Flask,render_template,request
import pickle
df = pickle.load(open('df.pkl','rb'))


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

    print(arr)

    return render_template('ml.html',data=arr)


@app.route('/blockchain')
def blockchain():
    return render_template('blockchain.html')

@app.route('/gamedev')
def gamedev():
    return render_template('gamedev.html')

@app.route('/web')
def web():
    return render_template('web.html')

@app.route('/appdev')
def appdev():
    return render_template('appdev.html')


if __name__ == '__main__':
    app.run(debug=True)
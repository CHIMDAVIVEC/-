from model import Isolines, TechParams, EconomicParams, ElectroParams, Optimal, Max
from flask import Flask, render_template, request
from compute import *
import sys

app = Flask(__name__)

try:
    template_name = sys.argv[1]
except IndexError:
    template_name = 'view'

@app.route('/', methods=['GET', 'POST'])
def index():
    iso = Isolines(request.form)
    tech = TechParams(request.form)
    econom = EconomicParams(request.form)
    electro = ElectroParams(request.form)
    opt = Optimal(request.form)
    maxl = Max(request.form)
    if request.method == 'POST' and iso.validate() and tech.validate() and econom.validate() and electro.validate():
        econom.c_u.data = econom.c_u.data / 60 / 8 / 20
        econom.c_z.data = econom.c_z.data / 60 / 8 / 20
        d = tech.d.data
        K = tech.K.data
        Z = round(iso.Z.data)
        if (request.form.getlist('q') == [u'val1']):
            q1 = 1
            q2 = 0
            q3 = 0
        elif(request.form.getlist('q') == [u'val2']):
            q1 = 0
            q2 = 1
            q3 = 0
        elif(request.form.getlist('q') == [u'val3']):
            q1 = 1
            q2 = 1
            q3 = 0
        
        no = N_opt(d, K, econom, electro, q1, q2, q3)
        So = S(no, d, K)
        Vp = V(no, d)
        Smp = Sm(no, d, K)
        Lp = L(no, So, d, K)
        Tp = T(Lp, Smp)
        Qp = Q(no, So, d, K, econom, electro, q1, q2, q3)

        nm = N_max(d, K, econom, electro, q1, q2, q3)
        Som = S(nm, d, K)
        Vpm = V(nm, d)
        Smpm = Sm(nm, d, K)
        Lpm = L(nm, Som, d, K)
        Tpm = T(Lpm, Smpm)
        Qpm = Q(nm, Som, d, K, econom, electro, q1, q2, q3)

        opt.n.data = round(no)
        opt.So.data = round(So, 3)
        opt.V.data = round(Vp)
        opt.Sm.data = round(Smp)
        opt.L.data = round(Lp)
        opt.T.data = round(Tp)
        opt.Q.data = round(Qp)

        maxl.n.data = round(nm)
        maxl.So.data = round(Som, 3)
        maxl.V.data = round(Vpm)
        maxl.Sm.data = round(Smpm)
        maxl.L.data = round(Lpm)
        maxl.T.data = round(Tpm)
        maxl.Q.data = round(Qpm)

        if (request.form.get('L') and not request.form.get('Q')):
            l = Graphic_L(no, So, d, K, Z, econom, electro, q1, q2, q3)
            pl.xlabel('Частота вращения n [Об/Мин]')
            pl.ylabel('Подача на оборот So [мм/Об]')
            if not os.path.isdir('static'):
                os.mkdir('static')
            else:
                for filename in glob.glob(os.path.join('static', '*.png')):
                    os.remove(filename)
            graphic = os.path.join('static', str(time.time()) + '.png')
            pl.savefig(graphic)
            graph = graphic
            pl.clf()
            pl.cla()
        elif (request.form.get('Q') and not request.form.get('L')):
            q = Graphic_Q(Qp, So, d, K, Z, econom, electro, q1, q2, q3)
            pl.xlabel('Частота вращения n [Об/Мин]')
            pl.ylabel('Подача на оборот So [мм/Об]')
            if not os.path.isdir('static'):
                os.mkdir('static')
            else:
                for filename in glob.glob(os.path.join('static', '*.png')):
                    os.remove(filename)
            graphic = os.path.join('static', str(time.time()) + '.png')
            pl.savefig(graphic)
            graph = graphic
            pl.clf()
            pl.cla()
        elif (request.form.get('L') and request.form.get('Q')):
            l = Graphic_L(no, So, d, K, Z, econom, electro, q1, q2, q3)
            q = Graphic_Q(Qp, So, d, K, Z, econom, electro, q1, q2, q3)
            pl.xlabel('Частота вращения n [Об/Мин]')
            pl.ylabel('Подача на оборот So [мм/Об]')
            if not os.path.isdir('static'):
                os.mkdir('static')
            else:
                for filename in glob.glob(os.path.join('static', '*.png')):
                    os.remove(filename)
            graphic = os.path.join('static', str(time.time()) + '.png')
            pl.savefig(graphic)
            graph = graphic
            pl.clf()
            pl.cla()
        else:
            graph = None
    else:
        graph = None

    return render_template(template_name + '.html', iso=iso, tech=tech, econom=econom, electro=electro, graph=graph, opt=opt, maxl=maxl)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
from app import app,db
from flask import render_template,request, url_for,redirect
from app.models import Auto, Jornal
from datetime import datetime, timedelta

@app.route('/', methods=['POST', 'GET'])
def index():
    # Получаем все записи из таблицы Auto
    auto_list = Auto.query.all()

    context = {
        'auto_list':auto_list,
        }
        
    return render_template('index.html', **context)


@app.route('/auto_detail/<int:auto_id>', methods=['POST', 'GET'])

def auto_detail(auto_id):
    
    auto = Auto.query.get(auto_id)
    
    jornal_list = Jornal.query.filter_by(auto_id = auto_id).all()


            
    check_transmission = None
    check_status = None

    if auto.transmission == True:
        check_transmission = 'Автомат'
    
    elif auto.transmission == False:
        check_transmission = 'Механика'
    

    
    if auto.status == True:
        
        check_status = 'Свободен'
    
    else:
        check_status = 'Занят'

    if request.method == 'POST':

        if request.form.get("delete"):
            db.session.delete(auto)
            for jornal_el in jornal_list:
                db.session.delete(jornal_el)
            db.session.commit()
            
            return redirect(url_for('index'))
            
   

        if request.form.get("change"):
            new_name = request.form['new_name']
            new_description = request.form['new_description']
            new_price = request.form['new_price']
            new_transmission = request.form['new_transmission']
            new_img_url1 = request.form['new_img_url1']
            new_img_url2 = request.form['new_img_url2']
            new_img_url3 = request.form['new_img_url3']
            new_img_url4 = request.form['new_img_url4']

            if  new_name:
                auto.name =  request.form['new_name']

            if  new_description:
                auto.description =  request.form['new_description']
                
            if  new_price:
                auto.price =  request.form['new_price']

            if  new_transmission:
                auto.transmission =  int(request.form['new_transmission'])
                
            if  new_img_url1:
                auto.img_url1 =  request.form['new_img_url1']
            
            if  new_img_url2:
                auto.img_url2 =  request.form['new_img_url2']
            
            if  new_img_url3:
                auto.img_url3 =  request.form['new_img_url3']  
            
            if  new_img_url4:
                auto.img_url4 =  request.form['new_img_url4']


            db.session.commit()
            
            if auto.transmission == True:
                check_transmission = 'Автомат'
        
            else:
                check_transmission = 'Механика'
            
            if auto.status == True:
                check_status = 'Свободен'
        
            else:
                check_status = 'Занят'

            
            
        if request.form.get("rent"):
            if request.method == 'POST':
                if auto.status == True:
                    check_status ='Занят'
                    Auto.query.filter_by(id = auto_id).update({"status":0})                   
                    db.session.add(Jornal(auto_id = auto_id,rent_start = datetime.now()+timedelta(hours=3)))
                    db.session.commit()
                    

        if request.form.get("free"):    
            if request.method == 'POST': 
                if auto.status == False:
                    check_status ='Свободен'
                    Auto.query.filter_by(id = auto_id).update({"status":1})
                    for jornal in jornal_list:
                        if jornal.rent_end == None:
                           jornal.rent_end =  datetime.now() + timedelta(hours=3)
                           count_date_sec = (jornal.rent_end-jornal.rent_start).seconds
                           count_date = divmod(count_date_sec,60)
                           cost = auto.price*count_date[0] +  auto.price/60*count_date[1]
                           jornal.cost = cost 
                           db.session.commit()
                           

    context = {
        'id' : auto.id,
        'name' : auto.name,
        'description' : auto.description,
        'price' : auto.price,
        'transmission' : check_transmission,
        'img_url1' : auto.img_url1,
        'img_url2' : auto.img_url2,
        'img_url3' : auto.img_url3,
        'img_url4' : auto.img_url4,
        'status' : check_status,
        'jornal_list' : jornal_list,
        }    
    return render_template('auto_detail.html', **context)

@app.route('/create_auto', methods = ['POST','GET'])
def create_auto():

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = str(request.form['price'])
        transmission = int(request.form['transmission'])
        
        if ',' in price:
            price = price.replace(',','.')

        float_price = float(price)
        

        db.session.add(Auto(name = name,description = description, price = float_price, transmission = transmission))
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_auto.html')  


@app.route('/rental_log', methods = ['POST','GET'])
def rental_log():
    
    total_list = db.session.query (Auto.img_url1, Auto.name,Jornal.rent_id,Jornal.rent_start,Jornal.rent_end,Jornal.cost).outerjoin(Jornal, Auto.id == Jornal.auto_id).all()
    rental_obj = db.session.query(Auto.img_url1, Auto.name, db.func.count(Jornal.rent_id).label('rent_count'), db.func.sum(Jornal.cost).label('rent_cost')).outerjoin(Jornal, Auto.id == Jornal.auto_id ).group_by(Auto.name).all()
    
    list_el = []
    for row in rental_obj:
        el = row._asdict()
        list_el.append(el)


    rental_dict={}


    for element in total_list:
        if (element.rent_start and element.rent_end) is None:
            pass
        else:
            if element.name in rental_dict:
                rental_dict[element.name] += int(((element.rent_end-element.rent_start).total_seconds()))/ 60
            else:
                rental_dict[element.name] = int(((element.rent_end-element.rent_start).total_seconds()))/ 60
    context = {
        'list_el': list_el,
        'rental_dict': rental_dict,
        }    
    return render_template('rental_log.html', **context)

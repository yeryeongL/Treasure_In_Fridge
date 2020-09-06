from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request



app = Flask(__name__)

client = MongoClient('localhost',27017)
db = client.myproject
@app.route('/')
def login():
    return render_template('login.html')
@app.route ('/page_1')
def page_1():
    return render_template('page_1.html')

@app.route('/page_2')
def page_2():
    return render_template('page_2.html')

@app.route('/page_3')
def page_3():
    return render_template('page_3.html')

@app.route('/login',methods=['POST'])
def name_input():

    name_val = request.form['name']

    db.LoginName.insert_one({'name': name_val})


    return jsonify({'result':'success','msg':'이름데이터전송에 성공했습니다'})

@app.route('/login',methods=['GET'])
def get_name():
    names = list(db.LoginName.find({},{'_id': False}))
    name = names[0]['name']

    return jsonify({'result': 'success', 'name': name})


@app.route ('/fridge', methods=['POST'])
def write_ingredient():
    ing_val = request.form['ingredient']
    amount_val=request.form['amount']
    expiration_year_val = request.form['expiration_year']
    expiration_month_val = request.form['expiration_month']
    expiration_date_val=request.form['expiration_date']

    db.ingredient.insert_one({'ingredient':ing_val,'amount':amount_val,'expiration_year':expiration_year_val,
                              'expiration_month':expiration_month_val,'expiration_date':expiration_date_val})

    return jsonify({'result':'success','msg':'재료데이터전송에 성공했습니다'})

@app.route('/fridge',methods=['GET'])
def show_ingredient():
    ingredients = list(db.ingredient.find({},{'_id':False})) #어떻게 하면 result 내림차순이 가능한지 result?
    return jsonify({'result':'success','ingredients':ingredients})

@app.route('/fridge/ToRecipe',methods=['POST'])
def To_recipe():

    ing_val = request.form['ingredient']

    return jsonify({'result': 'success', 'ingredient': ing_val})


@app.route('/fridge/delete',methods=['POST'])
def delete_ing():
    ing_receive = request.form['ingredient']
    db.ingredient.delete_one({'ingredient': ing_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '성공적으로 삭제되었습니다!'})


@app.route('/fridge/edit',methods=['POST'])
def edit_ing():
    ingredient = request.form['ingredient']
    amount = request.form['amount']
    expiration_year_val = request.form['expiration_year']
    expiration_month_val = request.form['expiration_month']
    expiration_date_val = request.form['expiration_date']
    db.ingredient.update({'ingredient': ingredient},
                         {'$set': {'amount': amount, 'expiration_year':expiration_year_val,'expiration_month':expiration_month_val,
                                   'expiration_date':expiration_date_val}})

    return jsonify({'result': 'success', 'msg': '메세지 변경에 성공하였습니다'})

@app.route('/fridge/show', methods=['GET'])
def show_recipes():

    ingredient=request.args.get('ingredient')
    recipe_all = list(db.recipe.find({'ingredients':ingredient}, {'_id':False}))

    # recipe_all=list(db.users.find({"ingredients":{"$in":["ingredient"]}},{'_id':False}))

    return jsonify({'result': 'success', 'recipe_all': recipe_all})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
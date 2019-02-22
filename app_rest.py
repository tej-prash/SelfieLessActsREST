from flask import Flask
from flask import request
import json
from flask import Response,render_template
import psycopg2 as psql
import datetime
import os
from werkzeug import secure_filename
from datetime import datetime
from collections import OrderedDict
import urllib.parse
import re
app=Flask(__name__)

app.config['UPLOAD_FOLDER']=os.path.dirname(os.path.realpath(__file__))+"/images/"
conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
cursor=conn.cursor()

# @app.route("/")
# def main():

#     cursor.execute("SELECT * FROM categories;")
#     data = cursor.fetchall()

#     if(cursor.rowcount>0):

#         return render_template("selfielessacts.html",data=data)

#     return render_template("selfielessacts.html")


# @app.route('/category/<name>')
# def category(name):
#     cursor.execute("SELECT * FROM acts where category='"+name+"';")
#     data = cursor.fetchall()

#     if(cursor.rowcount>0):
#         return render_template("category.html",data=data,category=name)
#     return render_template("category.html")

# @app.route('/upvote/<category>/<id>')
# def upvote(category,id):
#      query="SELECT upvotes FROM acts where act_id='"+str(id)+"';"

#      cursor.execute(query)
#      res=cursor.fetchone()

#      print("here ",res[0])

#      # if(cursor.rowcount>0):
#      query="UPDATE acts SET upvotes="+str(int(res[0])+1)+" where act_id="+"'"+str(id)+"'"+";"
#      cursor.execute(query)

#      print("done")


#      return render_template("category.html")




# @app.route("/actSubmit",methods=['POST'])
# def actSubmit():
#      cursor=conn.cursor()

#      description=request.form['description']
#      category=request.form['category'].lower()
#      upvotes=0
#      query="SELECT COUNT(*) FROM acts;"
#      #Get unique act id
#      cursor.execute(query)
#      res=cursor.fetchone()
#      act_id=0
#      if res is None:
#          act_id=0
#      act_id=int(res[0])+1
#      #Name of the tag containing the upload button is file
#      img=request.files['file']
#      imgurl=img_path+str(act_id)+".png"

#      img.save(imgurl)
#      # img.save(secure_filename(img.filename))
#      #timestamp=datetime.datetime.fromtimestamp(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
#      timestamp=datetime.datetime.now()

#      cursor=conn.cursor()

#      query="SELECT * FROM categories;"

#      cursor.execute(query)
#      res=cursor.fetchall()

#      if(cursor.rowcount>0):
#          if(category in [str(i[0]) for i in res]):
#              query="SELECT num_acts from categories where category="+"'"+str(category)+"'"+";"
#              cursor.execute(query)
#              res=cursor.fetchone();
#              res=int(res[0])+1
#              query="UPDATE CATEGORIES SET num_acts="+str(res)+" where category="+"'"+str(category)+"'"+";"
#              res=cursor.execute(query)

#          else:
#             query="INSERT into categories(category,num_acts) values("+"'"+str(category)+"'"+","+"1);"
#             cursor.execute(query)

#      else:
#         query="INSERT into categories(category,num_acts) values("+"'"+str(category)+"'"+","+"1);"
#         cursor.execute(query)



#      query="INSERT INTO acts values(%s,%s,%s,%s,%s,%s);"



#      try:
#          cursor.execute(query,(act_id,category,timestamp,description,upvotes,imgurl))
#          conn.commit()
#          conn.close()

#          return render_template("selfielessacts.html")
#      except Exception as e:
#          conn.commit()
#          conn.close()
#          return json.dumps({'message':'Failed to execute query'})

##################################################################################################################
@app.route("/api/v1/users",methods=["POST"])
def add_user():
    if(request.method=='POST'):
        data=request.json
        try:
            username=data['username']
            password=data['password'].lower()
        except:
            return Response("{}",status=400,mimetype='application/json')

        #if(not re.match("^[a-fA-F0-9]{40}$",password)):
            #NOt SHA 1 hashed
            #return Response("{}",status=400,mimetype='application/json')
        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from users;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()

        if(username in [i[0] for i in res]):
            return Response("{}",status=400,mimetype='application/json')

        flag=True
        for i in list(password):
            if(i not in "0123456789abcdef"):
                flag=False
                break

        if(flag==False or len(password)!=40):
            return Response("{}",status=400,mimetype='application/json')


        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query='INSERT INTO users VALUES('+"'"+str(username)+"'"+",'"+str(password)+"');"
        cursor.execute(query)
        conn.commit()
        conn.close()


        return Response("{}",status=201,mimetype='application/json')


    else:
        return Response("{}",status=405,mimetype='application/json')


@app.route("/api/v1/users/<name>",methods=['DELETE'])
def remove_user(name):
    if(request.method=='DELETE'):
        name=urllib.parse.unquote(name)
        if(name!=""):

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="Select * from users;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()




            if(name not in [i[0] for i in res]):

                return Response("{}",status=400,mimetype='application/json')



            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="DELETE from users where user_name="+"'"+name+"';"
            cursor.execute(query)
            conn.commit()
            conn.close()





            return Response("{}",status=200,mimetype='application/json')

        else:

            return Response("{}",status=400,mimetype='application/json')

    else:
        return Response("{}",status=405,mimetype='application/json')


# list al categories
@app.route("/api/v1/categories",methods=['POST','GET'])
def list_categories():

    if(request.method=='GET'):

        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

    #get categories from DB along with the number of acts for every category
        query="Select * from categories;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()

        d=dict()

        if(cursor.rowcount>0):


            for i in res:
                d[str(i[0])]=int(i[1])

            return Response(json.dumps(d),status=200,mimetype='application/json')

        else:
            return Response("{}",status=204,mimetype='application/json')

    elif(request.method=='POST'):

        data=request.json

        if(len(data)==1):

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="Select * from categories;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()


            if(data[0] not in [i[0] for i in res]):
                conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
                cursor=conn.cursor()

                query='INSERT INTO categories VALUES('+"'"+str(data[0])+"'"+','+str(0)+');'

                print(query)

                cursor.execute(query)
                conn.commit()
                conn.close()

                return Response("{}",status=201,mimetype='application/json')

            else:
                return Response("{}",status=400,mimetype='application/json')

        else:
                return Response("{}",status=400,mimetype='application/json')

    else:
        return Response("{}",status=405,mimetype='application/json')




@app.route("/api/v1/categories/<name>",methods=['DELETE'])
def remove_category(name):
    if(request.method=='DELETE'):
        name=urllib.parse.unquote(name)
        if(name!=""):

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="Select * from categories;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()

            print(name)


            if(name not in [i[0] for i in res]):

                return Response("{}",status=400,mimetype='application/json')



            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="DELETE from categories where category="+"'"+name+"';"
            cursor.execute(query)
            conn.commit()
            conn.close()





            return Response("{}",status=200,mimetype='application/json')

        else:

            return Response("{}",status=400,mimetype='application/json')

    else:
        return Response("{}",status=405,mimetype='application/json')


# List acts for a given category

# @app.route("/api/v1/categories/<categoryname>/acts",methods=['GET'])
# def list_acts(categoryname):
#     if(request.method=='GET'):
#         print("here##################################")

#         conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
#         cursor=conn.cursor()
#         query="Select * from categories;"
#         cursor.execute(query)
#         res=cursor.fetchall()
#         conn.commit()
#         conn.close()


#         if(str(categoryname) not in [str(i[0]) for i in res]):
#             return Response("{}",status=204,mimetype='application/json')


#         conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
#         cursor=conn.cursor()
#         query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
#         cursor.execute(query)
#         res=cursor.fetchone();
#         res=int(res[0])
#         conn.commit()
#         conn.close()


#         if(res>100):
#             return Response("{}",status=413,mimetype='application/json')

#         # if(res==0):
#         #     return Response("{}",status=204,mimetype='application/json')



#         conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
#         cursor=conn.cursor()
#         query="SELECT act_id,username,time_stamp,caption,upvotes,base64  from acts where category="+"'"+str(categoryname)+"'"+";"
#         cursor.execute(query)
#         res=cursor.fetchall()
#         conn.commit()
#         conn.close()

#         l=[]

#         for i in res:
#             d=OrderedDict()
#             d["actId"]=i[0]
#             d["username"]=i[1]
#             d["timestamp"]=i[2]
#             d["caption"]=i[3]
#             d["upvotes"]=i[4]
#             d["imageB64"]=i[5]
#             l.append(d)

#         # print(l)

#         return Response(json.dumps(l),status=200,mimetype='application/json')



#     else:
#         return Response("{}",status=405,mimetype='application/json')



# List acts for a given category
# @app.route("/api/v1/categories/<categoryname>/acts",methods=['GET'])
@app.route("/api/v1/categories/<categoryname>/acts",methods=['GET'])
def list_num_acts_range(categoryname):
    startrange = request.args.get('start')
    endrange = request.args.get('end')
    categoryname=urllib.parse.unquote(categoryname)
    print(startrange,endrange)
    if(startrange==None and endrange==None):
        if(request.method=='GET'):


            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="Select * from categories;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()


            if(str(categoryname) not in [str(i[0]) for i in res]):
                return Response("{}",status=204,mimetype='application/json')


            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
            cursor.execute(query)
            res=cursor.fetchone();
            res=int(res[0])
            conn.commit()
            conn.close()


            if(res>100):
                return Response("{}",status=413,mimetype='application/json')

            if(res==0):
                return Response("{}",status=200,mimetype='application/json')



            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="SELECT act_id,username,time_stamp,caption,upvotes,base64  from acts where category="+"'"+str(categoryname)+"'"+"ORDER BY time_stamp DESC;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()

            l=[]
            #if res==[]:
            #    return Response("{}",status=204,mimetype='application/json')
            for i in res:
                print("act",i)
                d=OrderedDict()
                d["actId"]=i[0]
                d["username"]=i[1]
                d["timestamp"]=str(datetime.strftime((i[2]),"%d-%m-%Y:%S-%M-%H"))
                d["caption"]=i[3]
                d["upvotes"]=i[4]
                d["imageB64"]=i[5]
                l.append(d)

            # print(l)

            return Response(json.dumps(l),status=200,mimetype='application/json')



        else:
            return Response("{}",status=405,mimetype='application/json')

    else:
        if(request.method=='GET'):
            startrange=int(startrange)
            endrange=int(endrange)
            print("startrange is ",startrange)
            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="Select * from categories;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()


            if(str(categoryname) not in [str(i[0]) for i in res]):
                return Response("{}",status=204,mimetype='application/json')

            if(int(endrange)-int(startrange)+1 > 100 ):
                return Response("{}",status=413,mimetype='application/json')



            # conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            # cursor=conn.cursor()
            # query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
            # cursor.execute(query)
            # res=cursor.fetchone();
            # res=int(res[0])
            # conn.commit()
            # conn.close()


            # if(res>100):
            #     return Response("{}",status=413,mimetype='application/json')

            # if(res==0):
            #     return Response("{}",status=204,mimetype='application/json')



            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="SELECT act_id,username,time_stamp,caption,upvotes,base64  from acts where category="+"'"+str(categoryname)+"'"+" ORDER BY time_stamp DESC;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()

            l=[]

            for i in res:
                d=OrderedDict()
                d["actId"]=i[0]
                d["username"]=i[1]
                d["timestamp"]=str(datetime.strftime((i[2]),"%d-%m-%Y:%S-%M-%H"))
                d["caption"]=i[3]
                d["upvotes"]=i[4]
                d["imageB64"]=i[5]
                l.append(d)

            print(l)
            # print(startrange,endrange)
            # print(l[int(startrange):int(endrange)+1])

            if(startrange<=0 or endrange<=0 ):
                return Response("{}",status=204,mimetype='application/json')

            if(startrange > len(l) or endrange > len(l) ):
                return Response("{}",status=204,mimetype='application/json')

            try:

                return Response(json.dumps(l[int(startrange)-1:int(endrange)]),status=200,mimetype='application/json')
            except:
                return Response("{}",status=400,mimetype='application/json')



        else:
            return Response("{}",status=405,mimetype='application/json')




# list number of acts for a given category
@app.route("/api/v1/categories/<categoryname>/acts/size",methods=['GET'])
def list_num_acts(categoryname):
    if(request.method=='GET'):
        categoryname=urllib.parse.unquote(categoryname)
        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from categories;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()


        if(str(categoryname) not in [str(i[0]) for i in res]):
            return Response("{}",status=204,mimetype='application/json')


        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()
        query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
        cursor.execute(query)
        res=cursor.fetchone();
        res=int(res[0])
        conn.commit()
        conn.close()



        return Response(json.dumps([res]),status=200,mimetype='application/json')



    else:
        return Response("{}",status=405,mimetype='application/json')






@app.route("/api/v1/acts/upvote",methods=['POST'])
def act_upvote():

    if(request.method=='POST'):

        data=request.json
        try:

            actid=str(data[0])

        except:

            return Response("{}",status=400,mimetype='application/json')


        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from acts;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()


        if(str(actid) not in [str(i[0]) for i in res]):
            return Response("{}",status=400,mimetype='application/json')



        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()
        query="SELECT upvotes FROM acts where act_id='"+str(actid)+"';"
        cursor.execute(query)
        res=cursor.fetchone()
        conn.commit()
        conn.close()


        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()
        query="UPDATE acts SET upvotes="+str(int(res[0])+1)+" where act_id="+"'"+str(actid)+"'"+";"
        cursor.execute(query)
        conn.commit()
        conn.close()


        return Response("{}",status=200,mimetype='application/json')

    else:


        return Response("{}",status=405,mimetype='application/json')



@app.route("/api/v1/acts",methods=['POST'])
def upload_act():
    if(request.method=='POST'):

        data=request.json

        try:
            actid=data['actId']
            username=data['username']
            timestamp=data['timestamp']
            caption=data['caption']
            categoryname=data['categoryName']
            img=data['imgB64']
        except:
            return Response("{}",status=400,mimetype='application/json')

        try:
            upvotes=data['upvotes']
        except:
            pass

        try:
            if(str(upvotes)!=""):
                return Response("{}",status=400,mimetype='application/json')
        except:
            pass





        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from acts;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()


        if(str(actid) in [str(i[0]) for i in res]):
            return Response("{}",status=400,mimetype='application/json')




        try:
            datetime.strptime(str(timestamp), '%d-%m-%Y:%S-%M-%H')
        except ValueError:
            print("date problem")
            return Response("{}",status=400,mimetype='application/json')


        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from categories;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()


        if(str(categoryname) not in [str(i[0]) for i in res]):
            return Response("{}",status=400,mimetype='application/json')



        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="Select * from users;"
        cursor.execute(query)
        res=cursor.fetchall()
        conn.commit()
        conn.close()


        if(str(username) not in [str(i[0]) for i in res]):
            return Response("{}",status=400,mimetype='application/json')



        flag=True
        for i in list(img):
            if(i not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="):
                flag=False
                break

        if(flag==False):
            return Response("{}",status=400,mimetype='application/json')




        timestamp=datetime.strptime(timestamp,"%d-%m-%Y:%S-%M-%H")
        timestamp=datetime.strftime(timestamp,"%Y-%m-%d %H:%M:%S")
        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="INSERT INTO acts(act_id,category,time_stamp,caption,username,base64) VALUES("+"'"+str(actid)+"','"+str(categoryname)+"','"+str(timestamp)+"','"+str(caption)+"','"+str(username)+"','"+str(img)+"');"
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
        except:
            print("Error executing SQL query:",query)
            return Response("{}",status=400,mimetype='application/json')
        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()
        query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
        cursor.execute(query)
        res=cursor.fetchone();
        res=int(res[0])+1
        conn.commit()
        conn.close()

        conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
        cursor=conn.cursor()

        query="UPDATE CATEGORIES SET num_acts="+str(res)+" where category="+"'"+str(categoryname)+"'"+";"
        res=cursor.execute(query)
        conn.commit()
        conn.close()

        return Response("{}",status=201,mimetype='application/json')


    else:
        return Response("{}",status=405,mimetype='application/json')


@app.route("/api/v1/acts/<actid>",methods=['DELETE'])
def remove_act(actid):
    if(request.method=='DELETE'):

        if(actid!=""):

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="Select * from acts;"
            cursor.execute(query)
            res=cursor.fetchall()
            conn.commit()
            conn.close()




            if(str(actid) not in [str(i[0]) for i in res]):

                return Response("{}",status=400,mimetype='application/json')



            # conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            # cursor=conn.cursor()

            # query="DELETE from acts where act_id="+"'"+str(actid)+"';"
            # cursor.execute(query)
            # conn.commit()
            # conn.close()


            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="SELECT category from acts where act_id='"+str(actid)+"';"

            print(query);
            cursor.execute(query)
            res=cursor.fetchone()
            categoryname=str(res[0])
            print(categoryname)
            conn.commit()
            conn.close()

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="DELETE from acts where act_id="+"'"+str(actid)+"';"
            cursor.execute(query)
            conn.commit()
            conn.close()



            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()
            query="SELECT num_acts from categories where category="+"'"+str(categoryname)+"'"+";"
            cursor.execute(query)
            res=cursor.fetchone();
            res=int(res[0])-1
            conn.commit()
            conn.close()

            conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
            cursor=conn.cursor()

            query="UPDATE CATEGORIES SET num_acts="+str(res)+" where category="+"'"+str(categoryname)+"'"+";"
            res=cursor.execute(query)
            conn.commit()
            conn.close()

            return Response("{}",status=200,mimetype='application/json')

        else:

            return Response("{}",status=400,mimetype='application/json')

    else:
        return Response("{}",status=405,mimetype='application/json')






@app.route("/api/numActs",methods=['GET'])
def numActs():
    conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
    cursor=conn.cursor()
    query="SELECT COUNT(*) FROM ACTS;"
    cursor.execute(query)
    conn.commit()
    #conn.close()
    if(cursor.rowcount==0):
        return Response("{}",status=204,mimetype="application/json")
    res=cursor.fetchone()[0]
    d=dict()
    d["numActs"]=str(res)
    conn.close()
    return Response(json.dumps(d),status=200,mimetype="application/json")




if __name__=='__main__':
    conn=psql.connect("dbname=selfielessacts user=postgres password=postgres")
    cursor=conn.cursor()
    img_path=os.path.dirname(os.path.realpath(__file__))+"/images/"
    app.run(debug=True,host="0.0.0.0")

# '192.168.0.105'
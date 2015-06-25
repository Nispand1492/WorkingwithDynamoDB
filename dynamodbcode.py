__author__ = 'Nispand'


import csv
import json
import sys
import bottle
from boto.dynamodb2.fields import HashKey, RangeKey , KeysOnlyIndex ,GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.items import Item
from bottle import route, request, response, template, HTTPResponse
import boto

fieldnames=["Lang","segment_id","contract_id","plan_id","contract_year","tier_level","tier_type_desc","sentences_sort_order","category_code"]

@bottle.route('/')
def main():
    return  template('Query_page',name="hello")

@bottle.route('/process_query')
def process_query():
    categoty_code = request.GET.get('category_code')
    par1 = request.GET.get('par1')
    par2 = request.GET.get('par2')
    plan_id = request.GET.get('plan_id')
    print categoty_code
    print par1
    print par2
    print plan_id
    if plan_id == None:
        data = fun_for_cat_code(categoty_code,par1)

    elif categoty_code == None :
        fun_for_planid_only(plan_id)

    else:
        fun_for_catandplan(categoty_code,par1,par2,plan_id)

    ans = " "
    for x in data:
        ans = ans + str(x[0]) + "|" + str(x[1]) + "|"+ str(x[2])+"|"+ str(x[3])+"|"+ str(x[4])+"|"+ str(x[5])+"|"+ str(x[6])+"|"+ str(x[7])
        ans = ans + "======================================================================================================================================"
    return template('Display_data',details = ans)

def fun_for_cat_code(cat_code,par1):
    if par1 == 'grt':
        data = tb.query_2(category_code__gt = cat_code)
        print data
    elif par1 == 'less':
        data = tb.query_2(category_code__lt = cat_code)
        print data
    elif par1 == 'equal':
        data = tb.query_2(category_code__eq = cat_code)
        print data
    elif par1 == 'lte':
        data = tb.query_2(category_code__lte = cat_code)
        print data
    elif par1 == 'gte':
        data = tb.query_2(category_code__gt = cat_code)
        print data
    return data

def fun_for_planid_only(planid):
    data = tb.query_2(plan_id__eq = planid)
    print data
    return data

def fun_for_catandplan(cat_code,par1,par2,plan_id):
    if par1 == 'grt':
        data = tb.query_2(category_code__gt = cat_code,plan_id__eq = plan_id)
        print data
    elif par1 == 'less':
        data = tb.query_2(category_code__lt = cat_code,plan_id__eq = plan_id)
        print data
    elif par1 == 'equal':
        data = tb.query_2(category_code__eq = cat_code,plan_id__eq = plan_id)
        print data
    elif par1 == 'lte':
        data = tb.query_2(category_code__lte = cat_code,plan_id__eq = plan_id)
        print data
    elif par1 == 'gte':
        data = tb.query_2(category_code__gte = cat_code,plan_id__eq = plan_id)
        print data


def convert(filename):
    csv_filename = filename
    print "Opening CSV file: ",csv_filename
    f=open(csv_filename, 'r')
    csv_reader = csv.reader(f)
    csv_reader.next()
    dict = {}
    import pdb
    #pdb.set_trace()
    for row in csv_reader:
            for i in xrange(len(row)):
                dict[fieldnames[i]] = row[i]
                print "Data Inserted in dynamo"
            try:
                tb.put_item(dict)
            except Exception as e:
                print "Item Already in Dynamo"
    return "Success"


conn = boto.dynamodb2.connect_to_region('us-west-2a')
tb = Table('Assign5',connection=conn)
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080, debug=True)
#ans = convert("nispand.csv")
#print ans





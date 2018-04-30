teststr = "'dbip':'127.0.01','dbport':3306,'dbuser':'root','dbpwd':'123456','dbname':'py_test','dbchar':'utf8'"
teststr = "{" + teststr + "}"
print type(teststr)
a = eval(teststr)
print type(a)
print a
if a.has_key('dbip') :
    print type(a['dbip'])
    print a['dbip']

if a.has_key('dbport'):
    print type(a['dbport'])
    print a['dbport']

print a['aa']
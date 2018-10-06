from functools import reduce
import operator

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def subtract(*args):
    
    ints = [int(x) for x in args]
    
    try:
        total = ints[0]
        for i in ints[1:]:
            total -= i
            body = "Your total for subtraction is: {}".format(total)
    except (ValueError, TypeError):
        body = "Unable to calculate a sum; please provide integers."
        
    return body

def multiply(*args):
    
    prod_list = []
    for i in args:
        prod_list.append(int(i))        

    try:
        total = reduce(operator.mul, prod_list, 1)
        body = "Your total for multiplication is: {}".format(total)
    except (ValueError, TypeError):
        body = "Unable to calculate a product; please provide integers"
        
    return body

def divide(*args):
    
    div_list = []
    for i in args:
        div_list.append(int(i))    

    try:
        total = div_list[0] / div_list[1]
        body = "Your total for division is: {}".format(total)
    except (ValueError, TypeError):
        body = "Unable to calculate a product; please provide integers"
        
    return body

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    #sum = "0"
    
    ints = [int(x) for x in args]
    
    try:
        total = sum(ints)
        body = "Your total for addition is: {}".format(total)
    except (ValueError, TypeError):
        body = "Unable to calculate a sum; please provide integers."

    return body

def index():
    
    body = ['<h1>Calcuator Instructions</h1>',
            '<h2>Open your browsers and point it to "localhost:8080", and follow the below instructions</h2><br>', '<ul>']
    item_template = '<li>{}</li><br>'
    bullets = ['To perform addition, append "/add" to the end of the URL, and then append the 2 numbers to add using this formatted example; "localhost:8080/add/10/20".', 'To perform one of [subtract, multiply, divide], use the same form as for addition, replacing "add" with "subtract, multiply, or divide".']
    for item in bullets:
        body.append(item_template.format(item))
    body.append('</ul>')
    return '\n'.join(body)

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    #print('resolve_path called with: ', path)
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
#    func = add
#    args = ['25', '32']

#    return func, args

    funcs = {'': index,
             'add': add,
             'multiply': multiply,
             'subtract': subtract,
             'divide': divide}
        
    path = path.strip('/').split('/')
    #print('path now is: ', path)
    
    func_name = path[0]
    
    if func_name == 'favicon.ico':
        func_name = ''
    #print('func_name: ', func_name)
    args = path[1:]
    #print(args)
    
    try:
        print(funcs[func_name])
        func = funcs[func_name]
        
    except KeyError:
        raise NameError
        
    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    import traceback
    headers = [('Content-type', 'text/html')]
    
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        #print(func, args)
        body = func(*args)
        #print(body)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>NotFound</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        #print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

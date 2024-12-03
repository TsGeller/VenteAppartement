import xmlrpc.client


email='56081@etu.he2b.be'
key= '4b731fe7e5f9ece18e3bfdf5652ce37d326aa0b5'
url = 'http://localhost:8069'
db = 'dev01'

def authentificate(name):
    
    try: 
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, email, key, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        
        id = models.execute_kw(db, uid, key, 'res.partner', 'search', [[['name', '=', name]]])
            
        if len(id) == 0:
            return [False, False]
        else:
            return [id, key]
    except:
        return [False, False]

    
 


def searchAppartement(key_):

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, email, key_, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    appartements = models.execute_kw(db, uid, key_, 'realtor.appartement', 'search_read', [[]])
    
   
    for appartement in appartements:

        try:
            idProduit= appartement.get('product_id')                
            ids= models.execute_kw(db, uid, key_, 'product.template','search', [[['id', '=',idProduit]]]) 
            nameProduct= models.execute_kw(db, uid, key_, 'product.template', 'read', [ids], {'fields': ['name']})  
            ids = models.execute_kw(db, uid, key_, 'stock.inventory.line', 'search', [[['product_id', '=', nameProduct[0].get('name')]]])
            check1= models.execute_kw(db, uid, key_, 'stock.inventory.line', 'read', [ids], {'fields': ['product_qty']})

            appartement['product_qty'] = check1[0].get('product_qty')
        except:
            appartement['product_qty'] = 0
                                   
    
    return appartements


def search(id, key_):

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, email, key_, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    appartement = models.execute_kw(db, uid, key_, 'realtor.appartement', 'search_read', [[['id', '=', id]]])
    try:
        idProduit= appartement[0].get('product_id')                
        ids= models.execute_kw(db, uid, key_, 'product.template','search', [[['id', '=',idProduit]]]) 
        nameProduct= models.execute_kw(db, uid, key_, 'product.template', 'read', [ids], {'fields': ['name']})  
        ids = models.execute_kw(db, uid, key_, 'stock.inventory.line', 'search', [[['product_id', '=', nameProduct[0].get('name')]]])
        check1= models.execute_kw(db, uid, key_, 'stock.inventory.line', 'read', [ids], {'fields': ['product_qty']})

        appartement[0]['product_qty'] = check1[0].get('product_qty')
    except:
        appartement[0]['product_qty'] = 0
   

    return appartement[0]




def makeOffer(appart_id, res_id, price, key_):

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, email, key_, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    try:
        models.execute_kw(db, uid, key_, 'realtor.offer', 'create', [{'appartement_id': appart_id, 'buyer_id': res_id[0], 'price': price}])
        return True
    except:
        return False
   


def register(name):
    
    try: 
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, email, key, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        models.execute_kw(db, uid, key, 'res.partner', 'create', [{'name': name}])

        return key

    except:
        return False
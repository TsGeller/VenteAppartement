import xmlrpc.client
print("Début du client d'appel vers ODOO")
print("---------------------------------")

url = 'http://localhost:8069'
db = 'dev01'
username = "g12345@he2b.be"# input("Entrez votre nom d'utilisateur: ")
password =  "odoo" #input("Entrez votre mot de passe: ")
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
hasRight = models.execute_kw(db, uid, password, 'realtor.appartement', 'check_access_rights', [
                             'read'], {'raise_exception': False})
if hasRight:
    print("L'utilisateur a le droit de voir les appartements")
    value = 'O'
    while value != 'no':
        appartementAsk = input("Entrez le nom de l'appartement: ")
        appartements = models.execute_kw(db, uid, password, 'realtor.appartement', 'search_read', [[]])
        
        trouve = False  
        for appartement in appartements:                  
            if (appartementAsk == appartement.get('name')):
                print("Appartement", appartement.get('name'))
                print("Description", appartement.get('description'))
                print("Disponible date", appartement.get('disponible_date'))
                print("Price", appartement.get('price'))
                print("Surface", appartement.get('surface'))
                print("Garden surface", appartement.get('garden_surface'))
                print("Total surface", appartement.get('total_surface'))
                print("Nom De l'acheteur ayant fait la meilleur offre ", appartement.get('buyer_name'))   
                print("Nombre d'offres faite : ", len(appartement.get('best_offer_ids'))) 
                try:
                    idOffer= appartement.get('best_offer_ids')                                
                    ids= models.execute_kw(db, uid, password, 'realtor.offer','search', [[['id', '=',idOffer[0]]]]) 
                    check1= models.execute_kw(db, uid, password, 'realtor.offer', 'read', [ids], {'fields': ['price']})
                    print("La meilleur offre faite", check1[0].get('price'))
                    
                    
                except:
                    print("Aucune offre n'a été faite")
                                   
                try:
                    idProduit= appartement.get('product_id')                
                    ids= models.execute_kw(db, uid, password, 'product.template','search', [[['id', '=',idProduit]]]) 
                    #print(ids) print l'id du product
                    nameProduct= models.execute_kw(db, uid, password, 'product.template', 'read', [ids], {'fields': ['name']})                
                    #print(nameProduct[0].get('name')) recupere le nom du produit associe à l'id
                    ids = models.execute_kw(db, uid, password, 'stock.inventory.line', 'search', [[['product_id', '=', nameProduct[0].get('name')]]])
                    #print(ids) recupere dans le stock l'id du produit via son nom 
                    check1= models.execute_kw(db, uid, password, 'stock.inventory.line', 'read', [ids], {'fields': ['product_qty']})
                    #print(check1[0].get('product_qty')) recupere la quantite du prudct dans le stock via l'id ci dessus
                    print("Quantity Product : ",check1[0].get('product_qty'))
                except:
                    print("Aucun stock n'a été trouvé")                                
                print("-------------------------------------------------")
                trouve=True
        if(trouve==False):
            print("L'appartement n'existe pas")
        while(1):
            value= input("Voulez-vous voir un autre Appartmement? (yes/no): ")
            if(value=='yes' or value=='no'):
                break
            


else:
    print("L'utilisateur n'a pas le droit de voir les appartements")

print("Fin du client d'appel vers ODOO")




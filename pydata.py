from pyDatalog import pyDatalog
pyDatalog.create_terms("X,tipoTerreno,Sole,Pioggia,Sabbioso,Breccioso,Terroso,Fangoso,Erboso,Alberato,Roccioso,modo"
                       ",APiedi,InBici,InMotoCross,attraversabileApiedi,attraversabileInbici,percorso,attraversabileInmoto,tipoPercorso,Passeggiata,Avventura,Panoramico")
pyDatalog.clear()
+ tipoTerreno("Sole", "Terroso")
+ tipoTerreno("Sole", "Sabbioso")
+ tipoTerreno("Sole", "Breccioso")
+ tipoTerreno("Sole", "Erboso")
+ tipoTerreno("Sole", "Alberato")
+ tipoTerreno("Sole", "Roccioso")

+ tipoTerreno("Pioggia", "Breccioso")
+ tipoTerreno("Pioggia", "Roccioso")
+ tipoTerreno("Pioggia", "Fangoso")
+ tipoTerreno("Pioggia", "Alberato")
+ tipoTerreno("Pioggia", "Erboso")

+ modo("APiedi", "Terroso")
+ modo("APiedi", "Erboso")
+ modo("APiedi", "Breccioso")
+ modo("APiedi", "Sabbioso")
+ modo("APiedi", "Alberato")

+ modo("InBici", "Sabbioso")
+ modo("InBici", "Terroso")
+ modo("InBici", "Breccioso")
+ modo("InBici", "Erboso")
+ modo("InBici", "Alberato")

+ modo("InMotoCross", "Fangoso")
+ modo("InMotoCross", "Sabbioso")
+ modo("InMotoCross", "Erboso")
+ modo("InMotoCross", "Breccioso")
+ modo("InMotoCross", "Roccioso")
+ modo("InMotoCross", "Terroso")

+tipoPercorso("Passeggiata", "APiedi")
+tipoPercorso("Panoramico", "InBici")
+tipoPercorso("Avventura", "InMotoCross")

attraversabileApiedi(X) <= (tipoTerreno("Sole", X) & modo("APiedi", X))
attraversabileInbici(X) <= ((tipoTerreno("Sole", X) or (tipoTerreno("Pioggia", X))) & modo("InBici", X))
attraversabileInmoto(X) <= (modo("InMotoCross", X))




#percorso(X)<=(tipoPercorso("Panoramico",X) and modo(X,"Terroso"))
def query(x:list) -> list:
    return (tipoTerreno(x[0],X)& modo(x[1],X))

def querytype(x) -> list:
    return tipoPercorso(x,X)


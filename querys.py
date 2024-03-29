import sqlite3

class bdquery():

		def __init__(self):
			self.conexion = sqlite3.connect('D:/Dropbox/bd.db')
			
			
			

		def cargapedido (self,Numpedido,registro,cantidad,ini,fin,dispoini,dispofin,estado,fechapedido,serie):
			cur=self.conexion.cursor()
			cur.execute("INSERT INTO pedidos (num_pedido,rncyfs,cantidad,inicio,fin,disponibleinicio,disponiblefin,estado,fecha_pedido,serie) values (?,?,?,?,?,?,?,?,?,?)",[Numpedido,registro,cantidad,ini,fin,dispoini,dispofin,estado,fechapedido,serie])
			self.conexion.commit()
			cur.close()
			
		def cargasubepedido (self,numpedido,inicio,fin,cantidad,variedad,especie,camp,kg,categoria,registro,fechasubpedido):
			cur=self.conexion.cursor()
			cur.execute("INSERT INTO subpedidos (num_pedido,num_reg,cantidad,inicio,fin,kg,variedad,especie,categoria,camp,fecha_subpedido) values (?,?,?,?,?,?,?,?,?,?,?)",[numpedido,registro,cantidad,inicio,fin,kg,variedad,especie,categoria,camp,fechasubpedido])
			self.conexion.commit()
			cur.close()
			
		def recuperabd(): #recuperar numero de pedido y rango general
			#self.conexion.execute("select numpedido,inicio,final from Datos")
			pass
		
		def actualizabd(self,inicio,fin,numpedido): #actualizar numero de pedido y rango general
			pass
			
		def traeultimopedido(self):
			cur =self.conexion.cursor()
			cur.execute("SELECT MAX(numpedido) from Datos")
			dato =cur.fetchone()
			cur.close()
			
			
			return dato
			
		def incrementanpedido(self,numpedido):
			
			cur=self.conexion.cursor()
			cur.execute("UPDATE Datos SET numpedido= (?) WHERE indice = 1",[numpedido])
			self.conexion.commit()
			cur.close()
		
		def recuperarango(self,indice):
			cur= self.conexion.cursor()
			cur.execute('''SELECT inicial, final FROM Datos where indice = ?''',[(indice)])
			rango=cur.fetchone()
			cur.close()
			return rango
				
		def actualizarangoenbd(self,inicio,final,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE Datos SET inicial = (?) where indice=?",[inicio,indice])
			cur.execute("UPDATE Datos SET final = (?) where indice=?",[final,indice])
			self.conexion.commit()
			cur.close()
			
		def verpedido(self,rncyfs):
			cur=self.conexion.cursor()
			cur.execute('''select num_pedido,disponibleinicio || "-" || disponiblefin,(disponiblefin-disponibleinicio+1)Stock, serie from pedidos
			where rncyfs =? and Stock !=0 order by disponibleinicio''',[rncyfs])
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
			
			
		def getpedido(self,numpedido):
			cur=self.conexion.cursor()
			cur.execute("SELECT * FROM pedidos WHERE num_pedido =?",[numpedido])
			listapedidos=cur.fetchone()
			self.conexion.commit()
			cur.close()
			return listapedidos
		
		def getpedidos(self):
			cur=self.conexion.cursor()
			cur.execute('''SELECT a.razon_social,cantidad,inicio ||"-" || fin,serie,num_pedido,fecha_pedido FROM pedidos p INNER JOIN asociados a on a.num_reg = p.rncyfs ORDER BY num_pedido DESC LIMIT 5''')
			listapedidos=cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listapedidos
			
		def actualizaremanente(self,numpedido,inicioremanente):
			cur=self.conexion.cursor()
			cur.execute("UPDATE pedidos SET disponibleinicio = (?) WHERE num_pedido = (?)",([inicioremanente,numpedido]))
			self.conexion.commit()
			cur.close()
			
		def actualizaestado(self,numpedido,estado):
			cur=self.conexion.cursor()
			cur.execute("UPDATE pedidos SET estado = (?) WHERE num_pedido = (?)",([estado,numpedido]))
			self.conexion.commit()
			cur.close()
			
			
		def traerasociados(self):
			cur=self.conexion.cursor()
			cur.execute(''' select razon_social from asociados order by razon_social''')
			listado=cur.fetchall()
			self.conexion.commit()
			cur.close
			return listado
			
		def traerasociadosFILTRO(self,nombre):
			cur=self.conexion.cursor()
			cur.execute(''' select razon_social from asociados where razon_social LIKE ? order by razon_social''',([nombre]))
			listado=cur.fetchall()
			self.conexion.commit()
			cur.close
			return listado
			
		def getrncyfs(self,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social = (?)''',[nombre])
			registro=cur.fetchone()
			self.conexion.commit()
			cur.close
			return registro
			
			
			
		def listaxregistro(self,campo,radiobutton):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||"-"|| p.fin,estado,IFNULL(s.cantidad,0),IFNULL(s.inicio|| "-" || s.fin,"SIN USAR"),
			IFNULL((p.fin-s.fin),p.cantidad),IFNULL(kg,"N/D"),IFNULL(variedad,"N/D"),IFNULL(especie,"N/D"),IFNULL(categoria,"N/D"),IFNULL(camp,"N/D"),IFNULL(fecha_subpedido,"N/D")
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE rncyfs=? and estado LIKE ? order by s.inicio''',[campo,radiobutton])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaxregistrofecha(self,campo,radiobutton,fecha_desde,fecha_hasta):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||"-"|| p.fin,estado,IFNULL(s.cantidad,0),IFNULL(s.inicio|| "-" || s.fin,"SIN USAR"),
			IFNULL((p.fin-s.fin),p.cantidad),IFNULL(kg,"N/D"),IFNULL(variedad,"N/D"),IFNULL(especie,"N/D"),IFNULL(categoria,"N/D"),IFNULL(camp,"N/D"),IFNULL(fecha_subpedido,"N/D")
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE rncyfs=? and estado LIKE ? and fecha_subpedido >= ? and fecha_subpedido <= ? order by s.inicio''',[campo,radiobutton,fecha_desde,fecha_hasta])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaxpedido(self,campo,radiobutton):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||"-"|| p.fin,estado,IFNULL(s.cantidad,0),IFNULL(s.inicio|| "-" || s.fin,"SIN USAR"),
			IFNULL((p.fin-s.fin),p.cantidad),IFNULL(kg,"N/D"),IFNULL(variedad,"N/D"),IFNULL(especie,"N/D"),IFNULL(categoria,"N/D"),IFNULL(camp,"N/D"),IFNULL(fecha_subpedido,"N/D")
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE p.num_pedido=? and estado LIKE ? order by s.inicio''',[campo,radiobutton])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
		def listaxpedidofecha(self,campo,radiobutton,fecha_desde,fecha_hasta):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||"-"|| p.fin,estado,IFNULL(s.cantidad,0),IFNULL(s.inicio|| "-" || s.fin,"SIN USAR"),
			IFNULL((p.fin-s.fin),p.cantidad),IFNULL(kg,"N/D"),IFNULL(variedad,"N/D"),IFNULL(especie,"N/D"),IFNULL(categoria,"N/D"),IFNULL(camp,"N/D"),IFNULL(fecha_subpedido,"N/D")
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido
			WHERE p.num_pedido=? and estado LIKE ? and fecha_subpedido >= ? and fecha_subpedido <= ? order by s.inicio''',[campo,radiobutton,fecha_desde,fecha_hasta])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
		def listaraexcell(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(s.cantidad)Cantidad_Solicitada,s.inicio|| "-" || s.fin,variedad,especie,categoria,kg
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE p.num_pedido=? order by s.inicio''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
		
		def listaraexcellall(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,(s.cantidad)Cantidad_Solicitada,s.inicio|| "-" || s.fin,variedad,especie,categoria,kg
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE p.rncyfs=? order by s.inicio''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
			
			
		def listaxtodo(self,campo):
			cur=self.conexion.cursor()
			cur.execute('''select p.num_pedido,rncyfs,p.cantidad,p.inicio,p.fin,estado,disponibleinicio,disponiblefin,
			s.inicio,s.fin,s.dav,variedad,especie,categoria,camp from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido WHERE rncyfs=?''',[campo])
			listado=cur.fetchall()
			self.conexion.commit
			cur.close()
			return listado
			
			
		def listarrendicion(self,desde,hasta,registro,especie,cultivar,categoria,camp):
			cur=self.conexion.cursor()
			cur.execute(''' select s.inicio||" - "||s.fin,s.cantidad,s.num_reg,a.razon_social,kg,especie,variedad,categoria,camp,fecha_subpedido,s.num_pedido
			from subpedidos s
			inner join asociados a
			on a.num_reg = s.num_reg
			where fecha_subpedido >= ? and fecha_subpedido <= ? and s.num_reg LIKE ? 
			and especie LIKE ? and variedad LIKE ? and categoria LIKE ? and camp LIKE ? order by s.inicio''',([desde,hasta,registro,especie,cultivar,categoria,camp]))
			listado = cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listado
			
		def listarrendicionsolopedidos(self,desde,hasta,registro):
			cur=self.conexion.cursor()
			cur.execute(''' select inicio||" - "||fin,cantidad,p.rncyfs,a.razon_social,fecha_pedido,num_pedido from pedidos p
			inner join asociados a on a.num_reg = p.rncyfs where fecha_pedido >= ? and fecha_pedido <= ? and p.rncyfs LIKE ? 
			order by inicio''',([desde,hasta,registro]))
			listado = cur.fetchall()
			self.conexion.commit()
			cur.close()
			return listado
			
		def insertarenlocker(self,numpedido,locker,fechaingreso,estado):
			cur=self.conexion.cursor()
			cur.execute(''' insert into lockers (num_pedido,num_locker,fecha_ingreso,estado) values (?,?,?,?)''',([numpedido,locker,fechaingreso,estado]))
			self.conexion.commit()
			cur.close()
			
			
		def definircantidadlockers(self,num,estado):
			cur=self.conexion.cursor()
			cur.execute ('''insert into lockers (num_locker,estado) values (?,?)''',([num,estado]))
			self.conexion.commit()
			cur.close()
			
		def recuperalockers(self):
			cur=self.conexion.cursor()
			cur.execute('''select num_locker from lockers where estado ="Disponible" order by num_locker''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def modificalocker(self,locker,pedido,fecha):
			cur=self.conexion.cursor()
			cur.execute("UPDATE lockers SET num_pedido = ? WHERE num_locker =?",[pedido,locker])
			cur.execute("UPDATE lockers SET fecha_ingreso = ? WHERE num_locker =?",[fecha,locker])
			cur.execute("UPDATE lockers SET estado = ? WHERE num_locker =?",["Ocupado",locker])
			self.conexion.commit()
			cur.close()
			
		def liberalocker(self,locker):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE lockers SET estado = "Disponible",num_pedido="",fecha_ingreso="" WHERE num_locker =?''',[locker])
				
			self.conexion.commit()
			cur.close()
			
			
			
		def verlockers(self):
			cur=self.conexion.cursor()
			cur.execute('''SELECT num_locker,l.num_pedido,disponibleinicio||" - "||disponiblefin,disponiblefin-disponibleinicio+1 cantidad,p.rncyfs,razon_social
			from lockers l inner join pedidos p inner join asociados a on p.num_pedido=l.num_pedido and a.num_reg =p.rncyfs order by num_locker''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def verlockers_filtrado(self,asociado):
			cur=self.conexion.cursor()
			cur.execute('''SELECT num_locker,l.num_pedido,disponibleinicio||" - "||disponiblefin,disponiblefin-disponibleinicio+1 cantidad,p.rncyfs,razon_social
			from lockers l inner join pedidos p inner join asociados a on p.num_pedido=l.num_pedido and a.num_reg =p.rncyfs where razon_social LIKE ? order by num_locker''',([asociado]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def altaasociado(self,reg,razonsocial):
			cur= self.conexion.cursor()
			cur.execute(''' insert into asociados (num_reg,razon_social) values (?,?)''',([reg,razonsocial]))
			self.conexion.commit()
			cur.close()
			
		def altagestion(self,reg,tipo,estado,fecha,cantidad):
			cur= self.conexion.cursor()
			cur.execute(''' insert into gestiones (num_reg,tipo,estado,fecha_inicio,cantidad) values (?,?,?,?,?)''',([reg,tipo,estado,fecha,cantidad]))
			self.conexion.commit()
			cur.close()
			
			
		def altarotulo(self,registro,especie,tipo,cantidad,estado,categoria,fecha,gestion):
			cur= self.conexion.cursor()
			cur.execute(''' insert into rotulos (num_reg,especie,tipo,cantidad,estado,categoria,fecha_impresion,gestion) values (?,?,?,?,?,?,?,?)''',([registro,especie,tipo,cantidad,estado,categoria,fecha,gestion]))
			self.conexion.commit()
			cur.close()
			
		def traerotulos(self,estado,tipo,especie,razon):
			cur=self.conexion.cursor()
			cur.execute('''select indice, fecha_impresion,estado,cantidad,a.razon_social,especie,categoria,tipo from rotulos r
			inner join asociados a on a.num_reg=r.num_reg where estado LIKE ? and tipo LIKE ? and especie like ? and a.razon_social LIKE ? order by indice DESC''',([estado,tipo,especie,razon]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traerotulosFecha(self,estado,tipo,especie,inicio,fin):
			cur=self.conexion.cursor()
			cur.execute('''select indice, fecha_impresion,estado,cantidad,a.razon_social,especie,categoria,tipo from rotulos r
			inner join asociados a on a.num_reg=r.num_reg where estado LIKE ? and tipo LIKE ? and especie like ? and fecha_impresion >= ? and fecha_impresion <=? order by indice DESC''',([estado,tipo,especie,inicio,fin]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traenombre(self,registro):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social from asociados where num_reg=?''',([registro]))
			self.conexion.commit()
			asociado=cur.fetchone()
			cur.close()
			return asociado
			
		def traerncyfs(self,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social=?''',([nombre]))
			self.conexion.commit()
			asociado=cur.fetchone()
			cur.close()
			return asociado
			
			
		def traergestiones(self,estado,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,estado,cantidad,(JulianDay(date()) - JulianDay(fecha_inicio)) demora,tipo,fecha_inicio, indice from gestiones g
			inner join asociados a on a.num_reg = g.num_reg where estado LIKE ? and razon_social LIKE ? order by demora ASC ''',([estado, nombre]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		
		def traergestionesActivas(self,estado,nombre):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social,estado,cantidad,(JulianDay(date()) - JulianDay(fecha_inicio)) demora,tipo,fecha_inicio, indice from gestiones g
			inner join asociados a on a.num_reg = g.num_reg where estado LIKE ? and estado != "FINALIZADO"  and razon_social LIKE ? order by demora ASC ''',([estado, nombre]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traenotas(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select IFNULL(observaciones,"") from gestiones where indice=?''',([indice]))
			self.conexion.commit()
			obs=cur.fetchone()
			return obs
			
		def updategestion(self,indice,estado):
			cur=self.conexion.cursor()
			cur.execute("UPDATE gestiones SET estado = (?) WHERE indice = (?)",([estado,indice]))
			self.conexion.commit()
			cur.close()
		def insertarnota(self,indice,obs):
			cur=self.conexion.cursor()
			cur.execute("UPDATE gestiones SET observaciones = (?) WHERE indice = (?)",([obs,indice]))
			self.conexion.commit()
			cur.close()
			
			
			
		def definirestadorotulo(self,estado,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE rotulos SET estado = (?) WHERE indice = (?)",([estado,indice]))
			self.conexion.commit()
			cur.close()
		
		def modificarCantidadImpresion(self,indice,cant):
			cur=self.conexion.cursor()
			cur.execute("UPDATE rotulos SET cantidad = (?) WHERE indice = (?)",([cant,indice]))
			self.conexion.commit()
			cur.close()
			
			
		def nuevorango(self,inicio,fin,cantidad,serie):
			cur= self.conexion.cursor()
			cur.execute(''' insert into rangos_disponibles (inicio,fin,cantidad,serie,estado) values (?,?,?,?,?)''',([inicio,fin,cantidad,serie,"DISPONIBLE"]))
			self.conexion.commit()
			cur.close()
			
		def traerangos(self,estado,serie):
			cur=self.conexion.cursor()
			cur.execute('''select inicio,fin,cantidad,serie,estado from rangos_disponibles where estado LIKE ? and serie=?order by inicio''',([estado,serie]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def definirrango(self,inicio,fin,indice):
			cur=self.conexion.cursor()
			cur.execute("UPDATE Datos SET (inicial,final) = (?,?) WHERE indice = (?)",([inicio,fin,indice]))
			cur.execute('''UPDATE rangos_disponibles SET (estado) = "EN USO" WHERE inicio = (?)''',([inicio]))
			self.conexion.commit()
			cur.close()
		
		def cancelarrango(self,inicio):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE rangos_disponibles SET (estado) = "TERMINADO" WHERE inicio = (?)''',([inicio]))
			self.conexion.commit()
			cur.close()
			
		def busquedaxrotulo(self,rotulo):
			cur=self.conexion.cursor()
			cur.execute(''' select p.num_pedido,(p.cantidad)Cantidad_Original,p.inicio ||"-"|| p.fin,estado,IFNULL(s.cantidad,0),IFNULL(s.inicio|| "-" || s.fin,"SIN USAR"),
			IFNULL((p.fin-s.fin),p.cantidad),IFNULL(kg,"N/D"),IFNULL(variedad,"N/D"),IFNULL(especie,"N/D"),IFNULL(categoria,"N/D"),IFNULL(camp,"N/D"),IFNULL(fecha_subpedido,"N/D")
			from pedidos p left join subpedidos s on p.num_pedido = s.num_pedido 
			WHERE ? BETWEEN p.inicio AND p.fin''',([rotulo]))
			self.conexion.commit()
			pedido=cur.fetchall()
			cur.close()
			return pedido
				
		def validarasociado(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select count(*) from asociados where num_reg =?''',[(reg)])
			self.conexion.commit()
			result=cur.fetchone()
			cur.close()
			return result
		
		def borrargestion(self,indice):
			cur=self.conexion.cursor()
			cur.execute(''' delete from gestiones where indice =?''',([indice]))
			self.conexion.commit()
			cur.close()
			
		def borrarimpresion(self,indice):
			cur=self.conexion.cursor()
			cur.execute(''' delete from rotulos where indice =?''',([indice]))
			self.conexion.commit()
			cur.close()
			
		def traerazonsocial(self,numpedido):
			cur=self.conexion.cursor()
			cur.execute('''select razon_social from asociados a
			inner join pedidos p on p.rncyfs = a.num_reg
			where num_pedido = ?''',([numpedido]))
			self.conexion.commit()
			razon=cur.fetchone()
			cur.close()
			return razon
			
		def getstock(self):
			cur=self.conexion.cursor()
			cur.execute('''select denominacion, cantidad from stock_rotulos''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def subpedidosporfecha(self,reg):
			cur=self.conexion.cursor()
			cur.execute('''select sum(cantidad),especie,fecha_subpedido from subpedidos where num_reg = ? group by fecha_subpedido ORDER BY fecha_subpedido DESC''',reg)
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def recuperastock(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select cantidad from stock_rotulos where indice=?''',([indice]))
			self.conexion.commit()
			cantidad=cur.fetchone()
			cur.close()
			return cantidad
			
		def actualizar_stock(self,cantidad,indice):
			cur=self.conexion.cursor()
			cur.execute('''UPDATE stock_rotulos SET (cantidad)= (?) WHERE (indice) =(?)''',([cantidad,indice]))
			self.conexion.commit()
			cur.close()
			
		def traerregistro(self,asociado):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg from asociados where razon_social =?''',([asociado]))
			self.conexion.commit()
			registro=cur.fetchone()
			cur.close()
			return registro
			
		def insertarEnvio(self,fecha_envio,registro,cantidad,tipo,rotulos,fecha_emision,bultos,estado,especie,detalle,obs):
			cur= self.conexion.cursor()
			cur.execute(''' insert into envios (fecha_envio,num_reg,cantidad,tipo,r,subpedido_fecha,bultos,estado,especie,detalle,obs) values (?,?,?,?,?,?,?,?,?,?,?)''',([fecha_envio,registro,cantidad,tipo,rotulos,fecha_emision,bultos,estado,especie,detalle,obs]))
			self.conexion.commit()
			cur.close()
			
		def getEnvios(self,registro):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id,tipo,detalle,obs from envios where num_reg = ? order by fecha_envio DESC''',registro)
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
		def getEnvios_ALL(self):
			cur=self.conexion.cursor()
			cur.execute('''select num_reg,fecha_envio,estado,cantidad,bultos,r,subpedido_fecha,id,tipo,detalle,obs from envios order by fecha_envio DESC''')
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
		def traeIndiceGestion(self):
			cur=self.conexion.cursor()
			cur.execute('''select max(indice)+1 from gestiones''')
			self.conexion.commit()
			gestion=cur.fetchone()
			cur.close()
			return gestion
			
		def traerIDgestion(self,indice):
			cur=self.conexion.cursor()
			cur.execute('''select gestion from rotulos where indice=?''',([indice]))
			self.conexion.commit()
			indice=cur.fetchone()
			cur.close()
			return indice
			
		def traeSubpedido(self,num_pedido,fechaSub):
			cur=self.conexion.cursor()
			cur.execute('''select * from subpedidos where num_pedido =? and fecha_subpedido=? order by inicio''',([num_pedido,fechaSub]))
			self.conexion.commit()
			listado=cur.fetchall()
			cur.close()
			return listado
			
			
		def traeRangoInicial(self,num_pedido,fechaSub):
			cur=self.conexion.cursor()
			cur.execute('''select min(inicio) from subpedidos where num_pedido =? and fecha_subpedido=? order by inicio''',([num_pedido,fechaSub]))
			self.conexion.commit()
			inicial=cur.fetchone()
			cur.close()
			return inicial
			
		
			
			
	
			
			

		






#conexion a base de datos
		#conexion = sqlite3.connect('bd.db')
		#cursor= conexion.cursor()
		#conexion.execute("INSERT INTO pedidos (num_pedido,rncyfs,cantidad,inicio,fin) values (?,?,?,?,?)",[Numpedido,registro,cantidad,Rango[0],Rango[0]+cantidad-1])
		#conexion.commit()
		#conexion.close()
		
		#q= bdquery()
		#q.cargabd(Numpedido,registro,cantidad,Rango[0],Rango[0]+cantidad-1)

import MySQLdb
import time
import datetime
def connection():
		db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		user="root",         # your username
		passwd="lex001",  # your password
		db="stocks")
		return db

def runQuerry(db,querry):
	cur = db.cursor()
	cur.execute(querry)	
	db.commit()
	data=cur.fetchall()
	cur.close()
	return data



def mysql_send_data(website_time,ticker,price,volume,opening,P_E,beta,earnings,dividents,p_growth,market_cap,news):
#"""ticker="DRYS"#str
#price=2.5#float
#volume=2564#int
#opening=2.4#float
#P_E=12#float
#earnings=12457#int
#dividents=0.6#
#p_growth=2.5#float
#market_cap=1054#int
#news="Http://www.google.com"#char"""
	db=connection()
	#querry="INSERT INTO 'info' ('website_time', 'ticker', 'price', 'volume', 'opening', 'P_E', 'earnings', 'dividents', 'p_growth', 'market_cap', 'news') VALUES (%s,%f,%i,%f,%f,%i,%f,%f,%i,%s )"%(ticker, price, volume, opening, P_E, earnings, dividents, p_growth, market_cap, news)
	#querry="""INSERT INTO `info` (`count`, `ticker`, `price`, `volume`, `opening`, `P_E`, `earnings`, `dividents`, `p_growth`, `market_cap`, `news`, `time_stamp`) VALUES (NULL, '"DRYS"', '2.5', '1000454', '2.6', '1.2', '534561', '0.3', '1.2', '16464', '"www.google.com"', CURRENT_TIMESTAMP)"""
	querry="""INSERT INTO `info` (`count`,`time`, `ticker`, `opening`, `price`, `volume`, `P_E`, `beta`, `p_growth`, `earnings`, `dividents`, `market_cap`, `news`, `time_stamp`) VALUES (NULL,'"""+website_time+"""' ,'"""+ticker+"""', '"""+str(opening)+"""', '"""+str(price)+"""', '"""+str(volume)+"""', '"""+str(P_E)+"""', '"""+str(beta)+"""', '"""+str(p_growth)+"""', '"""+str(earnings)+"""', '"""+str(dividents)+"""', '"""+str(market_cap)+"""', '"""+news+"""', CURRENT_TIMESTAMP)"""
	#print(querry)
	runQuerry(connection(),querry)
	db.close()

def mysql_send_data_table(table,count,website_time,ticker,opening,price,volume,P_E,beta,p_growth,earnings,dividents,market_cap,news,uploaded_date):
	print(table)
	#print(price)
	db=connection()
	querry="""INSERT INTO `"""+table+"""` (`count`,`id_count`,`time`, `ticker`, `opening`, `price`, `volume`, `P_E`, `beta`, `p_growth`, `earnings`, `dividents`, `market_cap`, `news`, `uploaded_date`,`time_stamp`) VALUES (NULL,'"""+str(count)+"""','"""+str(website_time)+"""' ,'"""+ticker+"""', '"""+str(opening)+"""', '"""+str(price)+"""', '"""+str(volume)+"""', '"""+str(P_E)+"""', '"""+str(beta)+"""', '"""+str(earnings)+"""', '"""+str(dividents)+"""', '"""+str(p_growth)+"""', '"""+str(market_cap)+"""', '"""+news+"""', '"""+str(uploaded_date)+"""', CURRENT_TIMESTAMP)"""
	#kk[0],kk[1],"14:02:23",kk[3],kk[4],kk[5],kk[6],kk[7],kk[8],kk[9],kk[10],kk[11],kk[12],kk[13]
	#print(querry)
	runQuerry(connection(),querry)
	db.close()

	
def mysql_read_data(table='info',date='2017-11-30',column='time_stamp'):
	db=connection()	
	
	#querry="""INSERT INTO `info` (`count`,`time`, `ticker`, `opening`, `price`, `volume`, `P_E`, `p_growth`, `earnings`, `dividents`, `market_cap`, `news`, `time_stamp`) VALUES (NULL,'"""+website_time+"""' ,'"""+ticker+"""', '"""+str(opening)+"""', '"""+str(price)+"""', '"""+str(volume)+"""', '"""+str(P_E)+"""', '"""+str(p_growth)+"""', '"""+str(earnings)+"""', '"""+str(dividents)+"""', '"""+str(market_cap)+"""', '"""+news+"""', CURRENT_TIMESTAMP)"""
	#querry="""select * from  """+table+"""  where time_stamp like '%"""+date+"""%' and ticker = 'AAL'"""
	querry="""select * from  """+table+"""  where """+column+""" like '%"""+date+"""%'"""
	print(querry)
	data = runQuerry(connection(),querry)
	#print (data)
	db.close()
	return data

def mysql_delete(table='info_vld',date='1-1-1'):
	db=connection()
	querry="""delete  from """+table+"""  where uploaded_date like '%"""+date+"""%'"""
	print(querry)
	k=input("Are you sure ?")
	data = runQuerry(connection(),querry)
	db.close()
	return data
#k=mysql_read_data(table='info')
#kk=('info_vld',)+k[0]
# mysql_send_data_table(kk[0],kk[1],(datetime.datetime.min+kk[2]).time(),kk[3],kk[4],kk[5],kk[6],kk[7],kk[8],kk[9],kk[10],kk[11],kk[12],kk[13])

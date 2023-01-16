# -*- coding: utf-8 -*-

"""
Пайтон3-Библиотека простого клиента к облачной кассе Ферма ОФД.Ру
OFD.Ru Ferma client python3 library class. 
FedorFL
ffl.public@gmail.com
+79219869856

"""
import string
import random

from pprint import pprint

import base64

from datetime import datetime
from logging import getLogger

import dateutil.parser

#import traceback
#import logging
#logger = logging.getLogger(__name__)

from random import choices
from string import hexdigits

from requests import post as wPost

import simplejson

#import qrcode
#import pyqrcode
import segno

import io
import base64

#-----------------------------------------------------------------------

"""
wChequeTest.py
5.2. Тестовое API Ferma
Для того чтобы пробить чеки на тестовой кассе Ferma, используйте домен 66) ferma-test.ofd.ru, для кассы версии ФФД 1.1 используйте следующие данные:

Логин - fermatest1;
Пароль - Hjsf3321klsadfAA;
для кассы версии ФФД 1.2:

Логин - fermatest2;
Пароль - Go2999483Mb.
Логин и пароль используются в API-запросе для получения кода авторизации (AuthToken).


"""


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


class wOFDRULib:
	
	AuthToken = None
	wTest = False
	wDbg = False
	
	wRcpInn = "0123456789"
	
	
	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------
	
	
	def __init__(self, wRcpInn = None, wTest=None, wDbg=None):
		
		if wRcpInn:
			self.wRcpInn = wRcpInn
			
		if wTest:
			self.wTest = wTest
		
		if wDbg:
			self.wDbg = wDbg
	
	
	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------


	def wSetInn(self, wRcpInn=None):
		
		if wRcpInn:
			
			self.wRcpInn = wRcpInn
			
			return True
			
		return None


	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------


	def wSetWDbg(self, wDbg):
		
		self.wDbg = wDbg
			
		return True


	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------


	def wSetWTest(self, wTest):
		
		self.wTest = wTest
		
		return True
		

	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------

	
	def wCreateToken(self):
		
		wHeaders = {
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'wMMEAgent',
		}
		
		wUri = 'https://ferma.ofd.ru/api/Authorization/CreateAuthToken'
		
		if self.wTest:
			wUri = 'https://ferma-test.ofd.ru/api/Authorization/CreateAuthToken'
		
		wResp = None
		
		#------
		
		wResp = wPost(
			
			wUri,
			
			#'https://ferma.ofd.ru/api/Authorization/CreateAuthToken',
			#'https://212.46.217.15/eis-app/eis-rs/businessPaymentService/getQrCode', 
			
			headers=wHeaders,
			
			verify=False, 
			
			json={
			
			"Login":"fermatest2",
			"Password":"Go2999483Mb",
			
			},

		)

		#------
		
		if self.wDbg:
			
			pprint(wResp)
			pprint(wResp.content)
			pprint(simplejson.loads(wResp.content))
		
		#------
		
		wData = None

		if wResp and wResp.ok:
			
			try: 
				wData = simplejson.loads(wResp.content)
			except:
				pass
		
		#------
		
		if isinstance(wData, dict) and \
			'Data' in wData and \
			'Status' in wData and \
			wData['Status'] == 'Success' and \
			'AuthToken' in wData['Data'] :
			
			self.AuthToken = wData['Data']['AuthToken']
			
			return wData['Data']['AuthToken']
		
		#------
		
		return None


	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------


	def wGetStatus(self, wChkReceiptId=None, wChkInvoiceId=None, wChkAuthToken=None):

		if not wChkAuthToken:
			
			if self.AuthToken:
				
				wChkAuthToken = self.AuthToken
				
			else:
				
				wChkAuthToken = self.wCreateToken()
				
				#return None
		
		#------
		
		wHeaders = {
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'wMMEAgent',
		}
		
		wUri = "https://ferma.ofd.ru/api/kkt/cloud/status?AuthToken={Code1}".format(Code1 = wChkAuthToken)
		
		if self.wTest:
			wUri = "https://ferma-test.ofd.ru/api/kkt/cloud/status?AuthToken={Code1}".format(Code1 = wChkAuthToken)
		
		wResp = None
		
		#------
		
		if wChkReceiptId:
		
			wResp = wPost(
				
				wUri, 
				
				headers=wHeaders,
				
				verify=False, 
				
				json={
					'Request': {
						'ReceiptId': wChkReceiptId,
					}
				},

			)
			
		elif wChkInvoiceId: 
			
			wResp = wPost(
				
				wUri, 
				
				headers=wHeaders,
				
				verify=False, 
				
				json={
					'Request': {
						'InvoiceId': wChkInvoiceId,
					}
				},

			)
			
		else:
			
			return None
		
		#------
		
		if wResp and wResp.ok:
			
			wData = None
			
			try:
				wData = simplejson.loads(wResp.content)
			except:
				pass
			
			if isinstance(wData, dict) and \
				'Data' in wData and \
				'Status' in wData and \
				wData['Status'] == 'Success':
			
					return wData['Data']
		
		#------
		
		return None


	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------


	def wGetList(self, wListReceiptId=None, wListDtFrom=None, wListDtTo=None, wListAuthToken=None):

		if not wListAuthToken:
			
			if self.AuthToken:
				
				wListAuthToken = self.AuthToken
			
			else:
				
				wListAuthToken = self.wCreateToken()
				
				#return None
		
		#------
		
		wHeaders = {
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'wMMEAgent',
		}
		
		wUri = "https://ferma.ofd.ru/api/kkt/cloud/list2?AuthToken={Code1}".format(Code1 = wListAuthToken)
		
		if self.wTest:
			wUri = "https://ferma-test.ofd.ru/api/kkt/cloud/list2?AuthToken={Code1}".format(Code1 = wListAuthToken)

		#------
		
		wDataPreJS = {
			'Request': {
				#"StartDateLocal": "2020-01-24T14:13:24",
				#'StartDateLocal': wListDtFrom,
				#"EndDateLocal": "2020-01-24T14:13:24"
				#'EndDateLocal': wListDtTo,
			}
		}
		
		if wListReceiptId:
			wDataPreJS['Request']['ReceiptId'] = wListReceiptId
		
		if wListDtFrom:
			wDataPreJS['Request']['StartDateLocal'] = wListDtFrom
		
		if wListDtTo:
			wDataPreJS['Request']['EndDateLocal'] = wListDtTo
		
		#------
		
		wResp = None
		
		wResp = wPost(
			
			wUri, 
			
			headers=wHeaders,
			
			verify=False, 
			
			json=wDataPreJS,

		)
		
		#------
		
		if wResp and wResp.ok:
		
			try:
				wData = simplejson.loads(wResp.content)
			except:
				pass
			
			if isinstance(wData, dict) and \
				'Data' in wData and \
				'Status' in wData and \
				wData['Status'] == 'Success':
			
					return wData['Data']
		
		#------	
		
		return None
		

	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------
	
	
	def wReciptRegister(self, wRcpLabel, wRcpAmountRub, wRcpInvoiceId=None, wRcpAuthToken=None):
		
		if not wRcpAuthToken:
			
			if self.AuthToken:
				
				wRcpAuthToken = self.AuthToken
			
			else:
				
				wRcpAuthToken = self.wCreateToken()
				
				#return None
		
		#------
		
		if not wRcpInvoiceId:
			
			wRnd = ''.join(random.choices(string.ascii_uppercase +
										 string.digits, k=28))
			
			wRcpInvoiceId = "wRcpt"+wRnd
			
		#------
		
		wRcpInn = self.wRcpInn
		
		wHeaders = {
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'wMMEAgent',
		}
		
		wUri = "https://ferma.ofd.ru/api/kkt/cloud/receipt?AuthToken={Code1}".format(Code1 = wRcpAuthToken)
		
		if self.wTest:
			wUri = "https://ferma-test.ofd.ru/api/kkt/cloud/receipt?AuthToken={Code1}".format(Code1 = wRcpAuthToken)

		#------

		wResp = None
		
		wResp = wPost(
			
			wUri, 
			
			headers=wHeaders,
			
			verify=False, 
			
			json={
				'Request': {
					'Inn': wRcpInn,
					'Type': 'Income',
					'InvoiceId': wRcpInvoiceId,
					'CustomerReceipt': {
						
						 "TaxationSystem": "Common",
						 #"Email": "example@ya.ru",
						 #"Phone": "+79000000001",
						 "PaymentType": 1, #Признак предмета расчета для всего чека. 1 – безналичными; 4 – иная форма оплаты.;
						 "Items": [
							 {
							 "Label": wRcpLabel,
							 "Price": wRcpAmountRub, #Цена товарной позиции в рублях
							 "Quantity": 1.0,
							 "Amount": wRcpAmountRub, #Общая стоимость товара в товарной позиции в рублях. Правила округления для стоимости товара зависят от типа кассы.
							 "Vat": "VatNo", #Вид вычисляемого НДС. 
											#«VatNo» — налог на добавленную стоимость без НДС;
											#«Vat10» — налог на добавленную стоимость (НДС) 10%;
											#«Vat18» — НДС 18%;
											#«Vat20» — НДС 20% 24);
											#«Vat0» — НДС 0%;
											#«CalculatedVat10110» «CalculatedVat20120 «CalculatedVat18118»
							 "MarkingCode": None,
							 "PaymentMethod": 1, #Признак способа расчета: - 1 — предоплата 100%; - 1 — предоплата 100%; - 7 — оплата в кредит.- 4 — полный расчет; 
							 }
						 ],
						
					},
					'PaymentItems': None,
					#'PaymentItems': { #Суммы по типам оплат
					#	'PaymentType': 1, #1 – безналичными
					#	'Sum': wRcpAmount, #Сумма по типу, в рублях
					#}
					'CustomUserProperty': None, #Наименование дополнительного реквизита пользователя с учетом особенностей сферы деятельности, в которой осуществляются расчеты
				}
			},

		)

		#------
		
		if self.wDbg:
			
			pprint(wResp)
			pprint(wResp.content)
			pprint(simplejson.loads(wResp.content))
			"""
			(b'{"Status":"Success","Data":{"ReceiptId":"957ef779-8ade-491d-8c57-98b363ab604'
			29bd861f-aa7a-4a63-8385-b82a02febe3e
			"""
		
		#------
		
		if wResp and wResp.ok:
			
			try:
				wData = simplejson.loads(wResp.content)
			except:
				pass
			
			if isinstance(wData, dict) and \
				'Data' in wData and \
				'Status' in wData and \
				wData['Status'] == 'Success' and \
				'ReceiptId' in wData['Data']:
					
					return wData['Data']['ReceiptId']
		
		#------	
		
		return None
	
	
	#-----------------------------------------------------------------------
	#-----------------------------------------------------------------------
		
	
	def wReciptQRLink(self, wReciptData, wResulType=None, wRcpAuthToken=None):
		
		if not wRcpAuthToken:
			
			if self.AuthToken:
				
				wRcpAuthToken = self.AuthToken
			
			else:
				
				wRcpAuthToken = self.wCreateToken()
				
				#return None
		
		#------
		
		if not isinstance(wReciptData, dict): #if by 'ReceiptId'
			
			wReciptData = self.wGetList(wReciptData)[0]
		
		#------
		
		if self.wDbg:
			
			pprint(wReciptData)
		
		#------
		
		if isinstance(wReciptData, dict) and \
			'InvoiceId' in wReciptData and \
			'Receipt' in wReciptData:
				
				wRcptDTUTC = dateutil.parser.isoparse(wReciptData['ReceiptDateUtc'])
				wTimePiece = wRcptDTUTC.strftime("%Y%m%dT%H%M")
				
				wTotalSum = wReciptData['Receipt']['cashboxInfoHolder']['totalSum']
				wTotalSum = "{:.2f}".format(float(wTotalSum))
				
				wFN = wReciptData['Receipt']['cashboxInfoHolder']['FN']
				
				wFDN = wReciptData['Receipt']['cashboxInfoHolder']['FDN']
				
				wFP = wReciptData['Receipt']['cashboxInfoHolder']['FPD']
				
				wLink = "t={0[wTimePiece]}&s={0[wTotalSum]}&fn={0[wFN]}&i={0[wFDN]}&fp={0[wFP]}&n=1".format({
					'wTimePiece': wTimePiece,
					'wTotalSum': wTotalSum,
					'wFN': wFN,
					'wFDN': wFDN,
					'wFP': wFP,
				})
				
				if not wResulType:
					
					return wLink
				
				elif wResulType == 'web':
					
					wQRImg = segno.make(wLink)
					wQRImg = wQRImg.png_data_uri()
					
					wLink = wQRImg
				
				elif wResulType == 'bytes':
					
					wQRImg = segno.make(wLink)
					
					wBBuff = io.BytesIO()
					wQRImg.save(wBBuff, kind='png')
					
					wBBuff.seek(0)
					
					wLink = wBBuff.getvalue()
					#wLink = base64.b64encode(s.getvalue()).decode("ascii")

				
				return wLink
		
		return None


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

#wToken = wRecipt = wRcptStatus = wRcptList = wRcptQRLink = wRcptQRBin = None

#wOFDRU = wOFDRULib(wRcpInn = "0123456789", wTest=True, wDbg=True)
#wToken = wOFDRU.wCreateToken()
#wRecipt = wOFDRU.wReciptRegister('Оплата моечной программы Питер Lt', 290.00)
#wRcptStatus = wOFDRU.wGetStatus('29bd861f-aa7a-4a63-8385-b82a02febe3e')
#wRcptList = wOFDRU.wGetList('29bd861f-aa7a-4a63-8385-b82a02febe3e')
#wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e')
#wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e')
#wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e', wResulType='web')
#wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e', wResulType='bytes')

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


#pprint(wToken)
#'99f5dbdc-2427-4837-a801-53d9f7039323'

#pprint(wRecipt)
#(b'{"Status":"Success","Data":{"ReceiptId":"957ef779-8ade-491d-8c57-98b363ab604'

#pprint(wRcptStatus)
"""
{'Device': {'DeviceId': 7825,
            'DeviceType': 'Эфир Pro ФС',
            'FDN': '19158',
            'FN': '9999078902009656',
            'FPD': '1261762727',
            'OfdReceiptUrl': 'https://check-demo.ofd.ru/rec/9999078902009656/19158/1261762727',
            'RNM': '0000000001015454',
            'ReceiptNumInShift': 152,
            'ShiftNumber': 208,
            'ZN': '9934666226'},
 'ModifiedDateTimeIso': '2023-01-16T17:46:25+03:00[Europe/Moscow]',
 'ModifiedDateUtc': '2023-01-16T17:46:25',
 'ReceiptDateTimeIso': '2023-01-16T17:46:25+03:00[Europe/Moscow]',
 'ReceiptDateUtc': '2023-01-16T17:46:25',
 'ReceiptId': '29bd861f-aa7a-4a63-8385-b82a02febe3e',
 'StatusCode': 2,
 'StatusMessage': 'Чек передан в ОФД',
 'StatusName': 'CONFIRMED'}
"""

#pprint(wRcptList)
"""
[{'InvoiceId': 'wRcpt2S5B1UX3EHGGBIWMTN3CAZLLE3G1',
  'ModifiedDateTimeIso': '2023-01-16T17:46:25+03:00[Europe/Moscow]',
  'ModifiedDateUtc': '2023-01-16T17:46:25',
  'Receipt': {'CustomerReceipt': {'Email': 'noreply@ofd.ru',
                                  'Items': [{'Amount': 290,
                                             'Label': 'Оплата моечной '
                                                      'программы Питер Lt',
                                             'PaymentMethod': 1,
                                             'PaymentType': 0,
                                             'Price': 290,
                                             'Quantity': 1,
                                             'Vat': 'VatNo'}],
                                  'KktFA': False,
                                  'PaymentType': 1,
                                  'TaxationSystem': 'Common'},
              'DoNotInheritPaymentAgentInfo': False,
              'Inn': '0123456789',
              'InvoiceId': 'wRcpt2S5B1UX3EHGGBIWMTN3CAZLLE3G1',
              'OneOfReceiptItemsContainsPaymentInfo': False,
              'Type': 'Income',
              'cashboxInfoHolder': {'DeviceId': 7825,
                                    'FDN': '19158',
                                    'FN': '9999078902009656',
                                    'FPD': '1261762727',
                                    'RNM': '0000000001015454',
                                    'ZN': '9934666226',
                                    'checkNumInShift': '152',
                                    'modelTypeId': 790,
                                    'shiftNum': '208',
                                    'totalSum': 290.0}},
  'ReceiptDateTimeIso': '2023-01-16T17:46:25+03:00[Europe/Moscow]',
  'ReceiptDateUtc': '2023-01-16T17:46:25',
  'ReceiptId': '29bd861f-aa7a-4a63-8385-b82a02febe3e',
  'StatusCode': 2,
  'StatusMessage': 'CONFIRMED',
  'StatusName': 'Чек передан в ОФД'}]

"""

#pprint(wRcptQRLink)
#t=20230116T1746&s=290.00&fn=9999078902009656&i=19158&fp=1261762727&n=1

"""
wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e', wResulType='web')
'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApAQAAAACAGz1bAAAA40lEQVR42mP4DwINDFipD7JxR9gbGL5ffS36vYHhS3worziQClRMBVHRd84Cqe+XuLcC5T6IhoYAVf7/cYcfpM9pcdH6Boa/phFnjjcw/LraalTfwPDpeX7v/QaGf5wKxfZA3utbB4ByP1rUt+1vYPit9Hzi9QaGPwKG9UC5D7/jQHLfeXk3xjcwfF3tP/k8UN9FxXp1oL7CoAaQ3MG12+cD5baWrQGa+d15ZYI+0PYPYdPdQW7pPcoPFLx7fXo40J1hKwuAcl+C6q7LA6lgfoP3QLkL79cAtX8QESjux+F3CAUA2+udLZgr4QAAAAAASUVORK5CYII='

"""

"""
wRcptQRLink = wOFDRU.wReciptQRLink('29bd861f-aa7a-4a63-8385-b82a02febe3e', wResulType='bytes')
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00)\x00\x00\x00)'
 b'\x01\x00\x00\x00\x00\x80\x1b=[\x00\x00\x00\xe3IDATx\xdac\xf8\x0f\x02\r'
 b'\x0cX\xa9\x0f\xb2qG\xd8\x1b\x18\xbe_}-\xfa\xbd\x81\xe1K|(\xaf8\x90\nTL\x05'
 b'Q\xd1w\xce\x02\xa9\xef\x97\xb8\xb7\x02\xe5>\x88\x86\x86\x00U\xfe\xff'
 b'q\x87\x1f\xa4\xcfiq\xd1\xfa\x06\x86\xbf\xa6\x11g\x8e70\xfc\xba\xdajT\xdf'
 b'\xc0\xf0\xe9y~\xef\xfd\x06\x86\x7f\x9c\n\xc5\xf6@\xde\xeb[\x07\x80r?Z\xd4'
 b'\xb7\xedo`\xf8\xad\xf4|\xe2\xf5\x06\x86?\x02\x86\xf5@\xb9\x0f\xbf\xe3@r\xdf'
 b'yy7\xc670|]\xed?\xf9<P\xdfE\xc5zu\xa0\xbe\xc2\xa0\x06\x90\xdc\xc1\xb5\xdb'
 b'\xe7\x03\xe5\xb6\x96\xad\x01\x9a\xf9\xddye\x82>\xd0\xf6\x0fa\xd3\xddAn\xe9='
 b'\xca\x0f\x14\xbc{}z8\xd0\x9da+\x0b\x80r_\x82\xea\xae\xcb\x03\xa9`~'
 b'\x83\xf7@\xb9\x0b\xef\xd7\x00\xb5\x7f\x10\x11(\xee\xc7\xe1w\x08\x05\x00'
 b'\xdb\xeb\x9d-\x98+\xe1\x00\x00\x00\x00\x00IEND\xaeB`\x82')

"""

#if wToken:	
#	pass

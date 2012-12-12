# -*- coding: latin1 -*- 
import cherrypy
from bs4 import BeautifulSoup
from time import strftime
from shutil import rmtree
from urllib.parse import unquote
import urllib.request
import webbrowser
import os
import sys
 
class WelcomePage:

	#pagina inicial
	def index(self):
		arq = open('c:/py/pi4/index.html', 'r', encoding='latin1')
		tela = arq.read()
		tela = tela.encode('latin-1').decode('utf-8')
		arq.close()
		return tela
	index.exposed = True
	
	#pagina de "carregando"
	def carregando(self, hdnValidacao=None, txtPesquisa=None, btnPesquisar=None):
		arq = open('c:/py/pi4/carregando.html', 'r', encoding='latin1')
		tela = arq.read()
		tela = tela.encode('latin-1').decode('utf-8')
		tela = tela.replace('::site::', str(txtPesquisa))
		arq.close()
		return tela
	carregando.exposed = True
    
	#pagina de resultado
	def resultado(self, hdnTxtSite=None, hdnTxtInicio=None, hdnTxtFim=None, hdnTxtTipoCategorizacao=None, hdnTxtCategoria=None, hdnTxtLinksInternos=None, hdnTxtLinksExternos=None, hdnDiretorio=None, hdnTxtCaminhoImagens=None, hdnTxtCaminhoArquivos=None, hdnTxtPalavras=None):
		# Organiza em ordem alfabetica e retira links duplicados
		def trataArray(seq):
			seq.sort()
			noDupes = []
			[noDupes.append(i) for i in seq if not noDupes.count(i)]
			return noDupes
		
		arq = open('c:/py/pi4/resultado.html', 'r', encoding='latin1')
		tela = arq.read()
		
		# ------- LINKS INTERNOS -------
		hdnTxtLinksInternos = unquote(hdnTxtLinksInternos)
		aux_links_internos_categorias = []
		links_internos_categorias = ""
		links_internos = ""
		links = hdnTxtLinksInternos.split('<##>')
		
		for contador in range(len(links)-1):
			link = links[contador].split("<#>")
			if link[1] == "":
				link[1] = "Não Classificado"
			aux_links_internos_categorias.append(link[1])
			links_internos = links_internos + '<div class="item_' + link[1].replace(" ", "_") + '" style="display:none"><a href="' + link[0] + '" target="_blank">' + link[0] + '</a></div>'
		
		aux_links_internos_categorias = trataArray(aux_links_internos_categorias)
		for contador in range(len(aux_links_internos_categorias)):
			if aux_links_internos_categorias[contador].replace(" ", "_") == "":
				aux_links_internos_categorias[contador] = "Não classificado"
			links_internos_categorias = links_internos_categorias + '<div id="' + aux_links_internos_categorias[contador].replace(" ", "_") + '" style="margin: 8px 0 0 8px; cursor: pointer; text-decoration: underline;" onclick="javascript: abrirLista(this);">' + aux_links_internos_categorias[contador] + '</div>'
			if contador == len(aux_links_internos_categorias) - 1:
				break;
		# ------------------------------
		# ------- LINKS EXTERNOS -------
		hdnTxtLinksExternos = unquote(hdnTxtLinksExternos)
		aux_links_externos_categorias = []
		links_externos_categorias = ""
		links_externos = ""
		links = hdnTxtLinksExternos.split('<##>')
		
		for contador in range(len(links)-1):
			link = links[contador].split("<#>")
			aux_links_externos_categorias.append(link[1])
			links_externos = links_externos + '<div class="item_' + link[1].replace(" ", "_") + '" style="display:none"><a href="' + link[0] + '" target="_blank">' + link[0] + '</a></div>'
		
		aux_links_externos_categorias = trataArray(aux_links_externos_categorias)
		for contador in range(len(aux_links_externos_categorias)):
			if aux_links_externos_categorias[contador].replace(" ", "_") == "":
				aux_links_externos_categorias[contador] = "Não classificado"
			links_externos_categorias = links_externos_categorias + '<div id="' + aux_links_externos_categorias[contador].replace(" ", "_") + '" style="margin: 8px 0 0 8px; cursor: pointer; text-decoration: underline;" onclick="javascript: abrirLista(this);">' + aux_links_externos_categorias[contador] + '</div>'
			if contador == len(aux_links_externos_categorias) - 1:
				break;
		# ------------------------------
		# ---------- IMAGENS -----------
		hdnTxtCaminhoImagens = unquote(hdnTxtCaminhoImagens)
		imagens = hdnTxtCaminhoImagens.split('<#>')
		
		imagem_pequena = ""
		imagem_grande = ""
		
		for contador in range(len(imagens)-1):
			imagem = imagens[contador]
			imagem_pequena = imagem_pequena + '<div id="imagem_' + str(contador) + '" onclick="javascript: abrirFotos(this);" style="float:left;"><img src="' + imagem + '" width="100px" height="100px"></div>'
			imagem_grande = imagem_grande + '<img class="foto_item_imagem_' + str(contador) + '" style="width:80%; height:80%; display:none" src="' + imagem + '"/>'
		# ------------------------------
		# ---------- ARQUIVOS ----------
		aux_arquivos = ""
		hdnTxtCaminhoArquivos = unquote(hdnTxtCaminhoArquivos)
		arquivos = hdnTxtCaminhoArquivos.split('<#>')
		
		for contador in range(len(arquivos)-1):
			arquivo = arquivos[contador].split('<##>')
			aux_arquivos = aux_arquivos + '<div><a href="' + arquivo[0] + '" target="_blank">' + arquivo[1] + '</a></div>'
		# ------------------------------
		
		# -----> URL DECODE + COLOCAR NA PÁGINA <-----
		tela = tela.encode('latin-1').decode('utf-8')
		tela = tela.replace('::site::', str(unquote(hdnTxtSite)))
		tela = tela.replace('::inicio::', str(unquote(hdnTxtInicio)))
		tela = tela.replace('::termino::', str(unquote(hdnTxtFim)))
		tela = tela.replace('::metodo::', str(unquote(hdnTxtTipoCategorizacao)))
		tela = tela.replace('::classificacao::', str(unquote(hdnTxtCategoria)))
		
		tela = tela.replace('::palavras_decisivas::', str(unquote(hdnTxtPalavras)))
		
		tela = tela.replace('::internos_categorias::', str(links_internos_categorias))
		tela = tela.replace('::internos_links::', str(links_internos))
		
		tela = tela.replace('::externos_categorias::', str(links_externos_categorias))
		tela = tela.replace('::externos_links::', str(links_externos))
		
		tela = tela.replace('::imagem_pequena::', str(imagem_pequena))
		tela = tela.replace('::imagem_grande::', str(imagem_grande))
		
		tela = tela.replace('::arquivos::', str(aux_arquivos))
		# -----> /URL DECODE <-----
		
		arq.close()
		return tela
	resultado.exposed = True
	
	#pagina de erro na URL
	def erro(self, hdnTxtSite=None):
		arq = open('c:/py/pi4/erro.html', 'r', encoding='latin1')
		tela = arq.read()
		tela = tela.encode('latin-1').decode('utf-8')
		tela = tela.replace('::site::', str(hdnTxtSite))
		arq.close()
		return tela
	erro.exposed = True
	
	#inicio do crawler
	def inicio(self, hdnTxtPesquisa=None):
	
		def numeroImagem():
			arq = open('c:/py/pi4/conf_imagem.txt', 'r')
			numero = arq.read()
			arq.close()
			arq = open('c:/py/pi4/conf_imagem.txt', 'w')
			arq.write(str(int(numero) + 1))
			arq.close()
			return numero
			
		# Organiza em ordem alfabetica e retira links duplicados
		def trataArray(seq):
			seq.sort()
			noDupes = []
			[noDupes.append(i) for i in seq if not noDupes.count(i)]
			return noDupes

		# Adiciona um texto em um arquivo
		def escreveArq(caminho, texto, modo):
			try:
				arq = open(caminho, modo, encoding='latin1')
				arq.write(texto)
				arq.close()
				return True
			except:
				return False

		# Faz a leitura do arquivo de configuracao das categorias		
		def leituraConf(conf):
			arq = open(conf,"r", encoding='latin1')
			categorias = []
			contador = 0
			while True:
				line = arq.readline()
				if not line:
					break
				else:
					if(line != ''):
						if line[:1] == '@':
							categorias.append([line[1:].strip().upper(), 0, [], []])
							contador += 1
						else:
							categorias[contador - 1][2].append(line.strip().lower())
			#Nome da categoria / Quantidade de palavras chaves / Lista de palavras / Lista de links
			return categorias
			
		def leituraHtmlBase(html_base):
			html = ""
			arq = open(html_base,"r", encoding='latin1')
			while True:
				line = arq.readline()
				if not line:
					break
				else:
					if(line != ''):
						html += line
			return html

		#Extrai a extensao do arquivo passado, se nao for um arquivo, ate primeiro ponto encontrado de tras para frente
		def extraiExtensao(texto):
			extensao = ""
			aux = ""
			contador = 1
			while contador <= len(texto):
				aux = texto[len(texto) - contador]
				if aux != ".":
					extensao = str(aux) + str(extensao)
					contador = contador + 1
				else:
					break
			return extensao
			
		def trataUrlLink(url, link):
			final = ""
			if link:
				link = link.strip()
				url = url.strip()
				if link != "#":
					if link[:7] != "http://" and link[:8] != "https://":
						if url[-4:] == ".php" or url[-5:] == ".html" or url[-4:] == ".htm" or url[-4:] == ".asp" or url[-4:] == ".jsp":
							aux = ""
							contador = 1
							while contador <= len(url):
								aux = url[len(url) - contador]
								if aux == "/":
									if link[:1] != "/":
										final += url[:(1-contador)] + link
									else:
										final += url[:(1-contador)] + link[1:]
									break
								else:
									contador = contador + 1
						else:
							final = url
							if final[-1:] == "/":
								if link[:1] != "/":
									final += link
								else:
									final += link[1:]
							else:
								if link[:1] != "/":
									final += "/" + link
								else:
									final += link
					else:
						final = link
			return final
			
		def categorizarPagina(soup, lista_categorias):
			meta_keywords_encontrado = False
			keywords = ""
			
			quantidade_1 = 0
			quantidade_2 = 0
			quantidade_3 = 0
			retorno = []
			retorno.append("") #Tipo de categorizacao
			retorno.append(0)  #Quantidade de palavras-chaves encontradas (principal)
			retorno.append("") #Categoria definida (principal)
			retorno.append(0)  #Quantidade de palavras-chaves encontradas (secundaria)
			retorno.append("") #Categoria definida (secundaria)
			retorno.append(0)  #Quantidade de palavras-chaves encontradas (terciaria)
			retorno.append("") #Categoria definida (terciaria)
			
			retorno.append(0)  #Quantidade de palavras mais encontrada (1)
			retorno.append("") #Palavra mais encontrada (1)
			retorno.append(0)  #Quantidade de palavras mais encontrada (2)
			retorno.append("") #Palavra mais encontrada (2)
			retorno.append(0)  #Quantidade de palavras mais encontrada (3)
			retorno.append("") #Palavra mais encontrada (3)
			
			for metas in soup.find_all('meta'):
				meta = metas.get('name')
				if meta == "keywords":
					meta_keywords_encontrado = True
					keywords = metas.get('content')
					retorno[0] = "Meta Tags"
					break
			
			if retorno[0] == "":
				retorno[0] = "Palavras-chaves"
				
			for categoria in lista_categorias:
				for palavras_chaves in categoria[2]:
					quant = 0
					
					if meta_keywords_encontrado == True:
						quant = keywords.count(palavras_chaves)
					else:
						quant = texto_html.count(palavras_chaves)
					categoria[1] += quant
				
					if quant > retorno[7]:
						if retorno[9] >= retorno[11]:
							retorno[11] = retorno[9]
							retorno[12] = retorno[10]
						if retorno[7] >= retorno[9]:
							retorno[9] = retorno[7]
							retorno[10] = retorno[8]
						retorno[7]  = quant
						retorno[8] = palavras_chaves
					elif meta_keywords_encontrado == True:
						if keywords.count(palavras_chaves) > retorno[9]:
							if retorno[9] >= retorno[11]:
								retorno[11] = retorno[9]
								retorno[12] = retorno[10]
							retorno[9]  = quant
							retorno[10] = palavras_chaves
						elif keywords.count(palavras_chaves) > retorno[11]:
							retorno[11]  = quant
							retorno[12] = palavras_chaves
					else:
						if texto_html.count(palavras_chaves) > retorno[9]:
							if retorno[9] >= retorno[11]:
								retorno[11] = retorno[9]
								retorno[12] = retorno[10]
							retorno[9]  = quant
							retorno[10] = palavras_chaves
						elif texto_html.count(palavras_chaves) > retorno[11]:
							retorno[11]  = quant
							retorno[12] = palavras_chaves
				
				#Verifica se ha outra categoria anterior com uma quantidade maior de palavras chaves encontradas
				if categoria[1] > quantidade_1:
					if retorno[3] >= retorno[5]:
						retorno[5] = retorno[3]
						retorno[6] = retorno[4]
					if retorno[1] >= retorno[3]:
						retorno[3] = retorno[1]
						retorno[4] = retorno[2]
					retorno[1]  = categoria[1]
					retorno[2] = categoria[0]
				elif categoria[1] > quantidade_2:
					if retorno[3] >= retorno[5]:
						retorno[5] = retorno[3]
						retorno[6] = retorno[4]
					retorno[3]  = categoria[1]
					retorno[4] = categoria[0]
				elif categoria[1] > quantidade_3:
					retorno[5]  = categoria[1]
					retorno[6] = categoria[0]
					
			return retorno
			
		def classificaLink(links, dominio, url, lista_categorias):
			validado = False
			link_interno = False
			link_retorno = ""
			categoria = ''
			# Obtem o "href" dos links
			link = links.get('href')
			# Verifica se o valor de link e nulo
			if link is not None:
				# Retira os espacos em branco antes e depois do link
				link = link.strip()
				if link.count(dominio) > 0:
					if link[:7] == "http://" or link[:8] == "https://":
						if link.find(dominio) < 15:
							link_interno = True
							link_retorno = link
							#link_site.append(link)
						else:
							link_retorno = link
							#link_externo.append(link)
					else:
						aux = trataUrlLink(url, link)
						#Verifica se com a URL, e possivel chegar a um caminho acessivel
						try:
							urllib.request.urlopen(aux)
							request = urllib.request.urlopen(link_retorno)
							html = request.read()
							html = html.decode("utf-8", "ignore")
							#Aplica o BeautifulSoup 4 no HTML
							soup = BeautifulSoup(html)
							categoria = categorizarPagina(soup, lista_categorias)
							validado = True
						#Caso nao seja possivel, utiliza o dominio para montar a URL
						except:
							aux = trataUrlLink("http://" + dominio, link)
						if aux != "":
							link_interno = True
							link_retorno = aux
							#link_site.append(aux)
				elif link.count(url) > 0:
					link_interno = True
					link_retorno = link
					#link_site.append(link)
				elif link[:7] == "http://" or link[:8] == "https://":
					link_retorno = link
					#link_externo.append(link)
				else:
					aux = trataUrlLink(url, link)
					#Verifica se com a URL, e possivel chegar a um caminho acessivel
					try:
						urllib.request.urlopen(aux)
						request = urllib.request.urlopen(link_retorno)
						html = request.read()
						html = html.decode("utf-8", "ignore")
						#Aplica o BeautifulSoup 4 no HTML
						soup = BeautifulSoup(html)
						categoria = categorizarPagina(soup, lista_categorias)
						validado = True
					#Caso nao seja possivel, utiliza o dominio para montar a URL
					except:
						aux = trataUrlLink("http://" + dominio, link)
					if aux != "":
						link_interno = True
						link_retorno = aux
						#link_site.append(aux)
			
			#Obtem a categoria do link
			if validado == False:
				try:
					request = urllib.request.urlopen(link_retorno)
					html = request.read()
					html = html.decode("utf-8", "ignore")
					#Aplica o BeautifulSoup 4 no HTML
					soup = BeautifulSoup(html)
					categoria = categorizarPagina(soup, lista_categorias)
					validado = True
				except:
					return ['']
			
			retorno = []
			retorno.append(link_retorno)
			retorno.append(link_interno)
			retorno.append(categoria[2])
			return retorno
			
		caminho_projeto = "c:/py/pi4/"
		caminho_projeto_fotos = caminho_projeto + "imagens_sites/"
		caminho_projeto_documentos = caminho_projeto + "documentos_sites/"
		caminho_aux_fotos = "imagens_sites/"
		caminho_aux_documentos = "documentos_sites/"
		pasta_site = ""
		
		diretorio_inicial = ""
		
		html = ""
		html_site = ""
		html_categoria = ""
		html_metodo = ""
		html_data_inicio = ""
		html_data_fim = ""
		html_link_internos = ""
		html_link_externos = ""
		html_palavras = ""

		texto_log_erros = ""
		texto_links = ""
			
		#URL do site
		url = hdnTxtPesquisa.strip()
		#Dominio extraido da URL do site (usado na classificacao de links)
		dominio = ""
		#Arquivo de erros
		arquivo_erros = 'log.txt'
		#Arquivo de links
		arquivo_links = 'links.txt'
		#Arquivo de conclusao
		arquivo_fim = 'fim.txt'
		#Arquivo contendo as categorias e palavras chaves
		arquivo_conf = caminho_projeto + 'crawler.conf'

		#Variavel que indica que o site possui meta tags com Keywords da pagina
		meta_keywords_encontrado = False	
		#Variavel que armazenara as keywords do site caso ele possua
		keywords = ""

		#Variavel que armazena a quantidade de palavras chaves encontradas
		quantidade_final = 0
		#O nome da categoria que teve mais palavras chaves presentes no html
		categoria_final = ""

		#Variavel que ira armazenar o HTML da pagina
		html = ""
		#Variavel que ira armazenar o texto do HTML da pagina
		texto_html = ""
		#Lista com os links internos encontrados no site
		link_site = []
		#Lista com os links externos encontrados no site
		link_externo = []
		#Lista com os caminhos de imagens
		caminhos_imagens = ""
		#Lista com os caminhos dos arquivos
		caminhos_arquivos = ""
		
		diretorio_inicial = url
		
		try:
			#Extrai todo o HTML da pagina
			request = urllib.request.urlopen(url)
			
			while url != request.geturl():
				url = request.geturl()
				request = urllib.request.urlopen(url)
			
			html = request.read()
			html = html.decode("utf-8", "ignore").lower()
		except:
			#RETORNO DE ERRO
			return "0"
		
		caminho_projeto = caminho_projeto + "sites/"
		
		#Encontra o dominio do site pela url digitada
		dominio = url.replace("http://www.", "").replace("https://www.", "").replace("/", "@").replace("http://", "").replace("https://", "")
		if dominio.find("@") != -1:
			dominio = dominio[:dominio.find("@")]
		
		#Aplica o BeautifulSoup 4 no HTML
		soup = BeautifulSoup(html)
		#Pega todo o texto da pagina
		texto_html = soup.get_text()
		
		pasta_site = diretorio_inicial.replace("http://", "").replace("/", "_") + "/"
	
		caminho_projeto = caminho_projeto + pasta_site
		arquivo_erros = caminho_projeto + arquivo_erros
		arquivo_links = caminho_projeto + arquivo_links
		
		if os.path.isfile(caminho_projeto + arquivo_fim):
			arq = open(caminho_projeto + arquivo_fim, 'r')
			retorno = arq.read()
			arq.close()
			#RETORNO CRAWLER JÁ FEITO
			return retorno
		
		lista_categorias = leituraConf(arquivo_conf)
		
		if not os.path.isdir(caminho_projeto):
			os.mkdir(caminho_projeto)

		html_site = url
		html_data_inicio = strftime("%d/%m/%Y %H:%M:%S")

		# ------ CATEGORIZAÇÃO DO SITE ------
		retorno = categorizarPagina(soup, lista_categorias)

		html_metodo = retorno[0]
		
		categoria_quant_1 = retorno[1]
		categoria_1 = retorno[2]
		categoria_quant_2 = retorno[3]
		categoria_2 = retorno[4]
		categoria_quant_3 = retorno[5]
		categoria_3 = retorno[6]
		
		if categoria_quant_1 > 0 and categoria_quant_2 > 0 and categoria_quant_3 > 0:
			categoria_quant_total = int(categoria_quant_1) + int(categoria_quant_2) + int(categoria_quant_3)
			
			perc_1 = int(categoria_quant_1) / int(categoria_quant_total) * 100
			perc_2 = int(categoria_quant_2) / int(categoria_quant_total) * 100
			perc_3 = int(categoria_quant_3) / int(categoria_quant_total) * 100
			
			palavra_quant_1 = retorno[7]
			palavra_1 = retorno[8]
			palavra_quant_2 = retorno[9]
			palavra_2 = retorno[10]
			palavra_quant_3 = retorno[11]
			palavra_3 = retorno[12]
			
			html_palavras = palavra_1 + " (" + str(palavra_quant_1) + " caso(s))"
			if palavra_quant_2 > 0:
				html_palavras = html_palavras + " - " + palavra_2 + " (" + str(palavra_quant_2) + " caso(s))"
			if palavra_quant_3 > 0:
				html_palavras = html_palavras + " - " + palavra_3 + " (" + str(palavra_quant_3) + " caso(s))"
			
			if categoria_1 == "":
				html_categoria = 'Nao foi possivel classificar o site em uma categoria'
			else:
				html_categoria = categoria_1 + "(" + str(perc_1) + "%)"
				
			if categoria_quant_2 > 0:
				html_categoria = html_categoria + " - " + categoria_2 + "(" + str(perc_2) + "%)"
			if categoria_quant_3 > 0:
				html_categoria = html_categoria + " - " + categoria_3 + "(" + str(perc_3) + "%)"
		else:
			html_categoria = 'Nao foi possivel classificar o site em uma categoria'
			html_palavras = 'Nao foi encontrado palavras-chaves'
		# -----------------------------------

		# ------ OBTENÇÃO DE LINKS ------
		contador = 1
		total_links = len(soup.find_all('a'))
		
		#Obtem todos os links do HTML
		for links in soup.find_all('a'):
			print("Link "+str(contador)+"/"+str(total_links))
			contador = contador + 1
			
			# ---- OBTENÇÃO DE DOCUMENTOS -----
			link = links.get('href')
			if link is not None:
				if link[-4:] == ".csv" or link[-4:] == ".pdf" or link[-4:] == ".doc" or link[-4:] == ".zip" or link[-4:] == ".rar" or link[-5:] == ".docx" or link[-4:] == ".xls" or link[-4:] == ".xlsx" or link[-3:] == ".7z":
					link = trataUrlLink("http://" + dominio, link)
					try:
						for cont in range(len(link) + 1):
							if link[-cont - 1] == "/":
								nome = link[-cont:]
								break
						local = caminho_projeto_documentos + nome
						urllib.request.urlretrieve(link, local)
						# Adiciona o documento na lista
						if caminhos_arquivos != "":
							caminhos_arquivos = caminhos_arquivos + "<#>"
						caminhos_arquivos = caminhos_arquivos + caminho_aux_documentos + nome + "<##>" + nome
					except:
						texto_log_erros += strftime("%d/%m/%Y %H:%M:%S") + " - Erro ao baixar arquivo: " + link + "\n"
				# ---------------------------------
				else:
					retorno = classificaLink(links, dominio, diretorio_inicial, lista_categorias)
					if retorno[0] != "":
						if retorno[1] == True:
							link_site.append(retorno[0] + "<#>" + retorno[2])
						else:
							link_externo.append(retorno[0] + "<#>" + retorno[2])
		# -------------------------------
		
		#Organiza a lista de links encontrados
		link_site = trataArray(link_site)
		link_externo = trataArray(link_externo)

		lista_links_internos = ""
		for link in link_site:
			if lista_links_internos != "":
				lista_links_internos = lista_links_internos + "<##>"
			lista_links_internos = lista_links_internos + link
			
		lista_links_externos = ""
		for link in link_externo:
			if lista_links_externos != "":
				lista_links_externos = lista_links_externos + "<##>"
			lista_links_externos = lista_links_externos + link
		
		# ------ OBTENÇÃO DE IMAGENS ------
		contador = 1
		total_imagens = len(soup.find_all('img'))
		for imagens in soup.find_all('img'):
			print("Imagem "+str(contador)+"/"+str(total_imagens))
			imagem = imagens.get('src')
			imagem = trataUrlLink("http://" + dominio, imagem)
			extensao = extraiExtensao(imagem)
			
			if extensao.count("jpg") == 0 and extensao.count("jpeg") == 0 and extensao.count("bmp") == 0 and extensao.count("gif") == 0 and extensao.count("png") == 0:
				texto_log_erros += strftime("%d/%m/%Y %H:%M:%S") + " - Extens\xe3o de imagem desconhecida: " + extensao + "\n"
				contador = contador + 1
				continue
			
			local = caminho_projeto_fotos + numeroImagem() + "." + extensao
			if imagem is not None:
				try:
					urllib.request.urlretrieve(imagem, local)
				except:
					texto_log_erros += strftime("%d/%m/%Y %H:%M:%S") + " - Erro ao baixar imagem: " + imagem + "\n"
					contador = contador + 1
					continue
				
				obj = os.stat(local)
				if obj.st_size < 1024:
					try:
						os.remove(local)
					except:
						texto_log_erros += strftime("%d/%m/%Y %H:%M:%S") + " - Erro ao remover imagem muito pequena: " + local + "\n"
				else:
					# Adiciona a imagem na lista
					if caminhos_imagens != "":
						caminhos_imagens = caminhos_imagens + "<#>"
						
					nome = ""
					for cont in range(len(local) + 1):
						if local[-cont - 1] == "/":
							nome = local[-cont:]
							break
					
					caminhos_imagens = caminhos_imagens + caminho_aux_fotos + nome
				contador = contador + 1
		# ---------------------------------
		
		html_data_fim = strftime("%d/%m/%Y %H:%M:%S")
		
		retorno = url + "|" + html_data_inicio + "|" + html_data_fim + "|" + html_metodo + "|" + html_categoria + "|" + lista_links_internos + "|" + lista_links_externos + "|" + caminhos_imagens + "|" + caminhos_arquivos + "|" + html_palavras
		
		arq = open(caminho_projeto + arquivo_fim, 'w')
		arq.write(retorno)
		arq.close()
		
		return retorno
	inicio.exposed = True

import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'htyhon.conf')

if __name__ == '__main__':
    cherrypy.quickstart(WelcomePage(), config=tutconf)
else:
    cherrypy.tree.mount(WelcomePage(), config=tutconf)

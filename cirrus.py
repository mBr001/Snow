import sys
import os.path
import re
import snow

#: The Cirrus tagset
cirrus=snow.TagSet({
	"doc":snow.TagDef([
		snow.Attribute("title",snow.Text("Cirrus")),
		snow.Attribute("...")
	]),
	"bold":snow.TagDef([
		snow.Attribute("...")
	]),
	"italic":snow.TagDef([
		snow.Attribute("...")
	]),
	"underline":snow.TagDef([
		snow.Attribute("...")
	]),
	"link":snow.TagDef([
		snow.Attribute("url",snow.Text("")),
		snow.Attribute("...")
	]),
	"line":snow.TagDef(),
	"image":snow.TagDef([
		snow.Attribute("url",snow.Text(""))
	]),
	"list":snow.TagDef(),
	"center":snow.TagDef([
		snow.Attribute("...")
	]),
	"heading":snow.TagDef([
		snow.Attribute("...")
	]),
	"color":snow.TagDef([
		snow.Attribute("with",snow.Text("#000")),
		snow.Attribute("...")
	])
})

#utility function for indenting code
_NEWLINE=re.compile(r"(\r\n|\n|\r)")
def indent(text,by=1,c="\t"):
	return c*by+_NEWLINE.sub(r"\1"+c*by,text)

class Element:
	'''
	A parsed element to be converted to HTML.
	'''
	def __init__(self,name,space=False,attrs=None,content=None,atomic=True):
		self.name=name
		self.parent=None
		self.attrs=attrs or {}
		self.content=content or []
		self.atomic=atomic
		self.space=space
	
	def __getitem__(self,x):
		return self.attrs[x]
	
	def __setitem__(self,x,val):
		self.attrs[x]=val
	
	def append(self,x):
		'''
		Add an element to the content of this element.
		'''
		self.content.append(x)
		x.parent=self
		return x
	
	def solidify(self):
		'''
		Convert the element into textual HTML code.
		'''
		attrs=" ".join('{}="{}"'.format(x,y) for x,y in self.attrs.items())
		if attrs:
			attrs=" "+attrs
		if len(self.content)>0:
			def gen():
				for x in self.content:
					c=x.solidify()
					if c==" ":
						continue
					yield c
			if self.space:
				return "<{0}{1}>\n{2}\n</{0}>".format(self.name,attrs,indent('\n'.join(gen())))
			return "<{0}{1}>{2}</{0}>".format(self.name,attrs,' '.join(gen()))
		if self.atomic:
			return "<{}{}/>".format(self.name,attrs)
		else:
			return "<{0}{1}></{0}>".format(self.name,attrs)

class TextElement(Element):
	'''
	An "element" which represents text in an HTML document.
	'''
	def __init__(self,text):
		Element.__init__(self,"",False,None,[text])
	
	def solidify(self):
		return self.content[0]

class Attr:
	'''
	An attribute class used to convert Cirrus attributes to HTML attributes.
	'''
	def __init__(self,name,convert=None):
		self.name=name
		if convert is None:
			self.convert=lambda attr,visitor:(name,attr)
		else:
			self.convert=convert

class ElementDef:
	'''
	A basic Tag -> Element conversion definition.
	'''
	def __init__(self,name,attrs=None,space=False,atomic=False):
		self.name=name
		self.attrs=attrs or {}
		self.space=space
		self.atomic=atomic
	
	def build_attrs(self,tag,visitor):
		for x in tag:
			try:
				v=self.attrs[x.toText().value].convert(tag[x],visitor)
				if v is not None:
					yield v
			except KeyError:
				pass
	
	def build(self,tag,visitor):
		'''
		Build an element out of the tag.
		'''
		visitor.cur=visitor.cur.append(Element(self.name,self.space,dict(self.build_attrs(tag,visitor)),None,self.atomic))

class ContentElementDef(ElementDef):
	'''
	Defines a conversion for an element that should have content.
	'''
	def build(self,tag,visitor):
		ElementDef.build(self,tag,visitor)
		tag["..."].visit(visitor)

class DocumentElementDef(ElementDef):
	'''
	The definition for the doc tag.
	'''
	def __init__(self):
		def add_title(attr,visitor):
			visitor.head.append(Element("title",None,False,[TextElement(attr.toText().value)]))
			return None
		
		ContentElementDef.__init__(self,"doc",{
			"title":Attr("",add_title)
		})
	
	def build(self,tag,visitor):
		if visitor.cur.parent is not None:
			print("A doc tag should only be at the root of the document")
			exit()
		dict(self.build_attrs(tag,visitor))
		tag["..."].visit(visitor)

class ListElementDef(ElementDef):
	def __init__(self):
		def build_type(attr,visitor):
			attr=attr.toText().value
			try:
				return "style","list-style-type:{}".format({"*":"disc","o":"circle","a":"lower-latin","A":"upper-alpha","i":"lower-roman","I":"upper-roman","1":"decimal"}[attr])
			except KeyError:
				return "style","list-style-type:{}".format(attr)
		
		ElementDef.__init__(self,"ol/ul",{
			"type":Attr("style",build_type)
		},True,False)
	
	def build(self,tag,visitor):
		try:
			if tag["type"] in {"*","disc","o","circle","square"}:
				self.name="ul"
			else:
				self.name="ol"
		except KeyError:
			self.name="ul"
		ElementDef.build(self,tag,visitor)
		cur=visitor.cur
		for x in tag.extra:
			visitor.cur=visitor.cur.append(Element("li"))
			x.visit(visitor)
			visitor.cur=cur

class Heading(ContentElementDef):
	def __init__(self):
		ContentElementDef.__init__(self,"heading",{
			"size":Attr("",lambda attr,visitor:None)
		},False,False)
	
	def build(self,tag,visitor):
		try:
			size=int(tag["size"].toNumber())
		except KeyError:
			if len(tag.extra)>0:
				size=int(tag["..."].toNumber())
				tag["..."]=tag.extra[0]
			else:
				size=1
		if 0<size<6:
			self.name="h"+str(size)
		else:
			self.name="h1"
		ContentElementDef.build(self,tag,visitor)

#: A dictionary of element conversion definitions.
elements={
	"doc":DocumentElementDef(),
	"bold":ContentElementDef("b"),
	"italic":ContentElementDef("i"),
	"underline":ContentElementDef("u"),
	"link":ContentElementDef("a",{
		"url":Attr("href")
	}),
	"line":ElementDef("br"),
	"image":ElementDef("img",{
		"url":Attr("src")
	}),
	"list":ListElementDef(),
	"center":ContentElementDef("center"),
	"heading":Heading(),
	"color":ContentElementDef("span",{
		"with":Attr("style",lambda attr,visitor:("style","color:"+attr.toText().value))
	})
}

class HTMLVisitor:
	'''
	The core class for the interpretation of Cirrus code.
	'''
	def __init__(self):
		self.head=Element("head",True)
		self.body=Element("body",True)
		self.cur=self.body
	
	def visit(self,which):
		'''
		Visit the given Snow value.
		'''
		which.visit(self)
	
	def accept(self,which):
		'''
		Accept a Snow value's visitation and reinterpret it as an HTML element.
		'''
		cur=self.cur
		if which.isDocument():
			#only visit the first element
			for x in which:
				if x.isTag():
					x.visit(self)
					return
			print("The Cirrus document has no readable content")
			exit()
		elif which.isTag():
			name=which.name.toText().value
			try:
				elements[name].build(which,self)
			except KeyError:
				print('Unexpected tag "{}"'.format(name))
				self.cur.append(Element("div"))
		elif which.isSection():
			for x in which:
				x.visit(self)
		else:
			self.cur.append(TextElement(which.value))
		self.cur=cur
	
	def solidify(self):
		'''
		Convert the entire document to HTML.
		'''
		return "<html>\n{}\n{}\n</html>".format(indent(self.head.solidify()),indent(self.body.solidify()))

if len(sys.argv)>2:
	src=sys.argv[1]
	dst=sys.argv[2]
elif len(sys.argv)>1:
	src=sys.argv[1]
	dst=os.path.splitext(src)[0]+".html"
else:
	print("""Usage: python cirrus.py src [dst]
  src   The source file.
  dst   The destination file.""")
	exit()

doc=snow.load(cirrus,open(src))
visitor=HTMLVisitor()
visitor.visit(doc)

open(dst,"w").write(visitor.solidify())
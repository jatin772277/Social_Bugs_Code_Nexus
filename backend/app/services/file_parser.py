import os,pymupdf,docx
from PIL import Image

def parse_document(file_path:str)->dict:
    ext=os.path.splitext(file_path)[1].lower()
    if ext=='.txt':
        with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
            return {'text':f.read(),'type':'text','meta':{}}
    elif ext=='.pdf':
        doc=pymupdf.open(file_path)
        pages=[]
        for i,page in enumerate(doc):
            pages.append(page.get_text())
        doc.close()
        return {'text':'\n'.join(pages),'type':'pdf','meta':{'page_count':len(pages)}}
    elif ext in ('.docx','.doc'):
        d=docx.Document(file_path)
        text='\n'.join([p.text for p in d.paragraphs if p.text.strip()])
        return {'text':text,'type':'docx','meta':{'paragraphs':len(d.paragraphs)}}
    elif ext in ('.png','.jpg','.jpeg','.webp'):
        try:
            im=Image.open(file_path).convert('RGB')
            w,h=im.size
            small=im.resize((50,50))
            colors=small.getcolors(2500)
            dominant=sorted(colors,key=lambda x:x[0],reverse=True)[:5] if colors else []
            hex_colors=['#{:02x}{:02x}{:02x}'.format(*c[1]) for c in dominant]
            return {'text':f'[Image file: {os.path.basename(file_path)} | Size: {w}x{h} | Dominant colors: {", ".join(hex_colors)}]','type':'image','meta':{'width':w,'height':h,'palette':hex_colors}}
        except Exception:
            return {'text':'[Image uploaded]','type':'image','meta':{}}
    return {'text':'','type':'unknown','meta':{}}

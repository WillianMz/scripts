from fpdf import FPDF

class PDFChecklist(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Checklist: Publicar Aplicação Angular no Apache", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0)
        self.cell(0, 8, title, ln=True)
        self.ln(1)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, body)
        self.ln()

pdf = PDFChecklist()
pdf.add_page()

content = [
    ("1. Build da Aplicação Angular", 
     "ng build --configuration production\n\n"
     "Se estiver em subdiretório:\n"
     "ng build --configuration production --base-href /nomedapasta/"),

    ("2. Copiar arquivos para o Apache",
     "Copie a pasta dist/seu-projeto/browser para:\n"
     "C:/xampp/htdocs/nomedapasta/"),

    ("3. Criar .htaccess para rotas Angular",
     "<IfModule mod_rewrite.c>\n"
     "  RewriteEngine On\n"
     "  RewriteBase /nomedapasta/\n"
     "  RewriteCond %{REQUEST_FILENAME} !-f\n"
     "  RewriteCond %{REQUEST_FILENAME} !-d\n"
     "  RewriteRule ^ index.html [L]\n"
     "</IfModule>"),

    ("4. Habilitar mod_rewrite e .htaccess no Apache",
     "Em httpd.conf:\n- Descomente: LoadModule rewrite_module modules/mod_rewrite.so\n"
     "- Em <Directory \"C:/xampp/htdocs\">, coloque:\n"
     "  AllowOverride All\n"
     "  Require all granted"),

    ("5. Acessar a aplicação",
     "Acesse via:\nhttp://localhost/nomedapasta/\n"
     "E teste rotas diretas como /login"),

    ("6. Verificar CORS",
     "O backend deve aceitar origem do frontend:\n"
     "Access-Control-Allow-Origin: http://localhost\n"
     "Access-Control-Allow-Methods: GET, POST, etc.\n"
     "Access-Control-Allow-Headers: Content-Type, Authorization"),

    ("7. Testar com HTTPS (opcional)",
     "Configure certificados SSL no Apache e use porta 443.")
]

for title, body in content:
    pdf.chapter_title(title)
    pdf.chapter_body(body)

pdf.output("Checklist_Publicar_Angular_Apache.pdf")

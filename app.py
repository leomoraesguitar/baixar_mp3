from flask import Flask, request, jsonify, render_template
# from baixar_youtube import BaixarDoYoutube
import yt_dlp



class BaixarDoYoutube:
    def __init__(self,print,diretorio = None ):
        self.converter_para_mp3 = True
        self.output = print
        self.arquiv = self.ler_json('config_baixar_youtube', default={
                    "pasta_donwloads": r'D:\baixados\tjse\mandados\2014',
                    "state_select":True
                })  
        self._diretorio = self.arquiv["pasta_donwloads"]
        if diretorio:
             self._diretorio =  diretorio 
             self.escrever_json({
                    "pasta_donwloads": diretorio,
                    "state_select":True
                }, 'config_baixar_youtube')
        self.nomes = []
        self.bitrate = '320'
        self.ffmpeg_path = r'D:\baixados\programas_python\ffmpeg-2024-07-10-git-1a86a7a48d-essentials_build\ffmpeg-2024-07-10-git-1a86a7a48d-essentials_build\bin'  # Altere para o caminho correto do seu ffmpeg
         # Opções de download
        self.ydl_opts = {
            'format': 'bestaudio/best',  # Seleciona o melhor formato de áudio
            'outtmpl': os.path.join(self._diretorio, '%(title)s.%(ext)s'),  # Nome do arquivo de saída

            'ffmpeg_location': self.ffmpeg_path,  # Especifica o caminho para o ffmpeg
        }



    def remove_invalid_characters(self, filename):
        forbidden_characters = ['\\', '/', ':', '*', '?', '¿','[', ']', '{', '}' '"', '<', '>', '|', ')', '(','|' ]
        clean_filenames = []
        for character in forbidden_characters:
            filename = filename.replace(character, '')
        return filename


    # def Convert_to_mp32(self, stem):
    #     if stem.mime_type in ["audio/mp4"]:
    #         nome = stem.title +'.mp4'
    #         audio = AudioSegment.from_file(nome, format="mp4")


    #     elif stem.mime_type in ["audio/webm"]:
    #         nome = stem.title +'.webm'
    #         audio = AudioSegment.from_file(nome, format="webm")

    #     saida = stem.title +'.mp3'
    #     audio.export(saida, format="mp3")
    #     self.output(f"'{saida}' convertido com sucesso")


    # def Convert_to_mp3(self):
    #     self.output(f"convertendo para mp3....")

    #     audio = AudioSegment.from_file(self.nome_save, format= self.extencao[1:])
    #     saida = self.nome +'.mp3'
    #     saida = os.path.join(self._diretorio, saida)

    #     audio.export(saida, format="mp3", bitrate = self.bitrate)
    #     self.output(f"'{saida}' convertido para mp3 com sucesso\n")
    #     os.remove(self.nome_save) #deletar o arquivo não convertido
                

    def Download(self, url):
        if self.converter_para_mp3:
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Formato de saída (por exemplo, mp3)
                'preferredquality': self.bitrate,  # Qualidade do áudio
            }]
        else:
            self.ydl_opts['postprocessors'] = []

        def progress_hook(d):
            if d['status'] == 'finished':
                self.title = d['info_dict']['title']

        self.ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])

        self.output(f' "{self.title}" foi baixado com sucesso para a pasta {self._diretorio} ')
        
                


    def BaixarAudio(self, url):
        self.Download(url)
    

    def Baixar(self, link):
        self.output(f"Iniciando donwload dos arquivos...")

        self.BaixarAudio(link)

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}

    @property
    def diretorio(self):
        return self._diretorio
    @diretorio.setter
    def diretorio(self,valor):
        if valor not in ['', None]:
            self._diretorio = valor
            self.arquiv["pasta_donwloads"] = valor
            self.escrever_json(self.arquiv, 'config_baixar_youtube')





app = Flask(__name__)

# Rota para renderizar a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o download
@app.route('/baixar', methods=['POST'])
def baixar_musica():
    try:
        data = request.json
        link = data.get('link')
        
        if not link:
            return jsonify({"error": "Link não fornecido"}), 400
        
        baixar = BaixarDoYoutube(print=print, diretorio="downloads")
        baixar.Baixar(link)

        return jsonify({"message": "Download concluído com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

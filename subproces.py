import subprocess

class Utils:
    @staticmethod
    def get_neuz():
        cmd = ['tasklist', '/FI', f"IMAGENAME eq MiniA.exe", '/V', "/FO", "CSV"]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        windows = []
        print(resultado.stdout)
        for line in resultado.stdout.splitlines()[1:]:  # Pula a primeira linha (cabeçalho)
            fields = line.split(',')
            windows.append([fields[8], int(fields[1].replace('"',""))])
        return windows




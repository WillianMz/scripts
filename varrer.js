const fs = require('fs');
const path = require('path');

// Caminho da pasta a ser varrida
const pasta = './sua-pasta';

// Caminho do arquivo de saída
const arquivoSaida = 'console-logs-encontrados.txt';

// Regex para capturar qualquer console.log(...)
const regexConsoleLog = /console\.log\s*\(.*?\)\s*;?/;

// Extensões aceitas
const extensoesAceitas = /\.(js|ts|jsx|tsx)$/i;

// Limpa o conteúdo anterior (se houver)
fs.writeFileSync(arquivoSaida, 'Console.log encontrados:\n\n');

// Função para ler arquivos recursivamente
function lerArquivos(dir) {
  const arquivos = fs.readdirSync(dir);
  arquivos.forEach((arquivo) => {
    const caminhoCompleto = path.join(dir, arquivo);
    const stats = fs.statSync(caminhoCompleto);

    if (stats.isDirectory()) {
      lerArquivos(caminhoCompleto); // recursivamente
    } else if (stats.isFile() && extensoesAceitas.test(caminhoCompleto)) {
      verificarConsoleLog(caminhoCompleto);
    }
  });
}

// Função para verificar linhas com console.log(...)
function verificarConsoleLog(caminhoArquivo) {
  const conteudo = fs.readFileSync(caminhoArquivo, 'utf-8');
  const linhas = conteudo.split('\n');

  linhas.forEach((linha, index) => {
    if (regexConsoleLog.test(linha)) {
      const resultado = `${caminhoArquivo} - Linha ${index + 1}: ${linha.trim()}\n`;
      fs.appendFileSync(arquivoSaida, resultado); // salva no arquivo
      console.log(resultado.trim()); // também mostra no console
    }
  });
}

// Iniciar varredura
lerArquivos(pasta);

console.log(`\n✅ Resultado salvo em: ${arquivoSaida}`);
